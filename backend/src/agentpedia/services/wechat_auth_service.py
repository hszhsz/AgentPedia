"""
微信扫码登录服务
"""
import uuid
import qrcode
import io
import base64
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import logging

from wechatpy import WeChatClient
from wechatpy.exceptions import WeChatClientException
from wechatpy.utils import random_string
from fastapi import HTTPException, status

from agentpedia.core.config import get_settings
from agentpedia.core.redis import redis_manager
from agentpedia.core.security import create_access_token, create_refresh_token
from agentpedia.models.user import User, UserRole, UserStatus, LoginMethod
from agentpedia.schemas.wechat import WechatLoginResponse, WechatCallbackRequest

logger = logging.getLogger(__name__)


class WechatAuthService:
    """微信认证服务"""

    def __init__(self):
        self.settings = get_settings()
        self.client: Optional[WeChatClient] = None

    def _get_client(self) -> WeChatClient:
        """获取微信客户端"""
        if not self.client:
            if not self.settings.WECHAT_APP_ID or not self.settings.WECHAT_APP_SECRET:
                raise ValueError("微信配置缺失")

            self.client = WeChatClient(
                self.settings.WECHAT_APP_ID,
                self.settings.WECHAT_APP_SECRET
            )
        return self.client

    async def generate_login_qr_code(self) -> WechatLoginResponse:
        """生成登录二维码"""
        try:
            # 生成唯一的会话ID
            session_id = str(uuid.uuid4())

            # 生成微信登录 ticket
            client = self._get_client()

            # 使用微信开放平台网站应用登录
            # 这里需要根据实际的微信开放平台API调整
            login_url = f"https://open.weixin.qq.com/connect/qrconnect?appid={self.settings.WECHAT_APP_ID}"
            login_url += f"&redirect_uri={self.settings.WECHAT_REDIRECT_URI}"
            login_url += f"&response_type=code&scope=snsapi_login&state={session_id}#wechat_redirect"

            # 生成二维码
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(login_url)
            qr.make(fit=True)

            # 将二维码转换为base64
            img = qr.make_image(fill_color="black", back_color="white")
            buffer = io.BytesIO()
            img.save(buffer, format="PNG")
            qr_code_base64 = base64.b64encode(buffer.getvalue()).decode()

            # 在Redis中存储会话信息，有效期5分钟
            await redis_manager.setex(
                f"wechat_login:{session_id}",
                300,  # 5分钟
                {
                    "status": "pending",
                    "created_at": datetime.utcnow().isoformat(),
                    "login_url": login_url
                }
            )

            return WechatLoginResponse(
                session_id=session_id,
                qr_code=qr_code_base64,
                login_url=login_url,
                expires_in=300
            )

        except Exception as e:
            logger.error(f"生成微信登录二维码失败: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="生成登录二维码失败"
            )

    async def check_login_status(self, session_id: str) -> Dict[str, Any]:
        """检查登录状态"""
        try:
            # 从Redis获取会话信息
            session_data = await redis_manager.get(f"wechat_login:{session_id}")
            if not session_data:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="登录会话不存在或已过期"
                )

            return {
                "session_id": session_id,
                "status": session_data.get("status", "pending"),
                "user_info": session_data.get("user_info"),
                "expires_at": session_data.get("expires_at")
            }

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"检查登录状态失败: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="检查登录状态失败"
            )

    async def handle_callback(self, request: WechatCallbackRequest) -> Dict[str, Any]:
        """处理微信回调"""
        try:
            # 验证state参数
            session_data = await redis_manager.get(f"wechat_login:{request.state}")
            if not session_data:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="无效的会话ID"
                )

            # 使用code获取access_token
            client = self._get_client()

            try:
                # 获取access_token
                token_data = client.oauth.fetch_access_token(
                    self.settings.WECHAT_REDIRECT_URI,
                    code=request.code
                )

                # 获取用户信息
                user_info = client.oauth.get_user_info(
                    access_token=token_data['access_token'],
                    openid=token_data['openid']
                )

            except WeChatClientException as e:
                logger.error(f"微信API调用失败: {e}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="微信授权失败"
                )

            # 在数据库中查找或创建用户
            user = await self._get_or_create_user(user_info)

            # 生成JWT令牌
            access_token = create_access_token(subject=user.id)
            refresh_token = create_refresh_token(subject=user.id)

            # 更新Redis中的会话信息
            session_data.update({
                "status": "success",
                "user_info": {
                    "id": user.id,
                    "username": user.username,
                    "nickname": user.nickname,
                    "avatar_url": user.avatar_url,
                    "role": user.role
                },
                "access_token": access_token,
                "refresh_token": refresh_token,
                "expires_at": (datetime.utcnow() + timedelta(minutes=30)).isoformat()
            })

            await redis_manager.setex(
                f"wechat_login:{request.state}",
                1800,  # 30分钟
                session_data
            )

            return {
                "session_id": request.state,
                "status": "success",
                "access_token": access_token,
                "refresh_token": refresh_token,
                "user_info": session_data["user_info"]
            }

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"处理微信回调失败: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="处理微信回调失败"
            )

    async def refresh_access_token(self, refresh_token: str) -> Dict[str, str]:
        """刷新访问令牌"""
        try:
            # 这里应该验证refresh_token的有效性
            # 简化实现，实际应该从数据库或Redis中验证

            # 解析refresh_token获取用户ID
            # 这里需要实现具体的解析逻辑

            # 生成新的access_token
            # access_token = create_access_token(subject=user_id)

            # 暂时返回模拟数据
            return {
                "access_token": "new_access_token_here",
                "expires_in": 1800
            }

        except Exception as e:
            logger.error(f"刷新访问令牌失败: {e}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="刷新令牌失败"
            )

    async def _get_or_create_user(self, user_info: Dict[str, Any]) -> User:
        """根据微信用户信息获取或创建用户"""
        from agentpedia.core.database import AsyncSessionLocal

        openid = user_info['openid']
        nickname = user_info.get('nickname', 'WeChat User')
        avatar_url = user_info.get('headimgurl', '')
        unionid = user_info.get('unionid')

        async with AsyncSessionLocal() as session:
            # 查找现有用户
            from sqlalchemy import select
            result = await session.execute(
                select(User).where(User.openid == openid)
            )
            user = result.scalar_one_or_none()

            if user:
                # 更新用户信息
                user.update_wechat_info(
                    openid=openid,
                    nickname=nickname,
                    avatar_url=avatar_url,
                    unionid=unionid
                )
                user.last_login_at = datetime.utcnow()
                await session.commit()
                await session.refresh(user)
                logger.info(f"更新微信用户信息: {user.id} - {nickname}")
            else:
                # 创建新用户
                user = User(
                    login_method=LoginMethod.WECHAT,
                    openid=openid,
                    unionid=unionid,
                    nickname=nickname,
                    avatar_url=avatar_url,
                    role=UserRole.USER,  # 新用户默认为普通用户
                    status=UserStatus.ACTIVE,
                    last_login_at=datetime.utcnow()
                )

                # 生成基于openid的用户名
                user.username = f"wx_{openid[:8]}"

                session.add(user)
                await session.commit()
                await session.refresh(user)

                logger.info(f"创建新微信用户: {user.id} - {nickname}")

            return user

    async def logout(self, user_id: int) -> bool:
        """用户登出"""
        try:
            # 将用户的refresh_token加入黑名单
            # 这里可以实现具体的黑名单逻辑

            logger.info(f"用户登出: {user_id}")
            return True

        except Exception as e:
            logger.error(f"用户登出失败: {e}")
            return False

    async def cleanup_expired_sessions(self):
        """清理过期会话"""
        try:
            # 这里可以实现清理逻辑
            # 例如定期清理Redis中过期的登录会话
            pass
        except Exception as e:
            logger.error(f"清理过期会话失败: {e}")


# 创建全局微信认证服务实例
wechat_auth_service = WechatAuthService()