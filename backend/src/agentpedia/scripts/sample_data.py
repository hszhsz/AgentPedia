"""
示例数据脚本
用于初始化数据库中的示例Agent数据
"""
import asyncio
from datetime import datetime
from agentpedia.core.mongodb import mongodb_manager
from agentpedia.models.mongodb_models import (
    AgentModel, MultilingualText, MultilingualDescription, 
    DevelopmentTeam, TechnicalStack, BusinessInfo, FundingInfo, AgentStatus
)

async def init_mongodb():
    """初始化MongoDB连接"""
    await mongodb_manager.init_mongodb()

async def create_sample_agents():
    """创建示例Agent数据"""
    collection = mongodb_manager.get_collection("agents")
    
    # 清空现有数据
    collection.delete_many({})
    
    # 创建示例Agent 1 - ChatGPT
    chatgpt = AgentModel(
        name=MultilingualText(
            zh="ChatGPT",
            en="ChatGPT"
        ),
        slug="chatgpt",
        logo_url="https://example.com/logos/chatgpt.png",
        official_url="https://chat.openai.com",
        description=MultilingualDescription(
            short=MultilingualText(
                zh="OpenAI开发的对话式AI助手",
                en="OpenAI's conversational AI assistant"
            ),
            detailed=MultilingualText(
                zh="ChatGPT是由OpenAI开发的大型语言模型，能够进行自然语言对话，回答问题，协助创作等。",
                en="ChatGPT is a large language model developed by OpenAI that can engage in natural language conversations, answer questions, and assist with creative tasks."
            )
        ),
        development_team=DevelopmentTeam(
            name=MultilingualText(
                zh="OpenAI",
                en="OpenAI"
            ),
            location="San Francisco, USA",
            website="https://openai.com",
            description=MultilingualText(
                zh="人工智能研究实验室",
                en="AI research laboratory"
            )
        ),
        technical_stack=TechnicalStack(
            base_model=["GPT-4", "GPT-3.5"],
            frameworks=["Transformers"],
            programming_languages=["Python"],
            deployment=["Cloud"],
            description=MultilingualText(
                zh="基于Transformer架构的大语言模型",
                en="Large language model based on Transformer architecture"
            )
        ),
        features=[
            MultilingualText(
                zh="自然语言理解",
                en="Natural language understanding"
            ),
            MultilingualText(
                zh="代码生成",
                en="Code generation"
            ),
            MultilingualText(
                zh="多语言支持",
                en="Multilingual support"
            )
        ],
        business_info=BusinessInfo(
            funding=[
                FundingInfo(
                    round="B轮",
                    amount="10亿美元",
                    investors=["微软", "其他投资者"],
                    date="2019-07"
                ),
                FundingInfo(
                    round="C轮",
                    amount="100亿美元",
                    investors=["微软"],
                    date="2023-01"
                )
            ],
            business_model=MultilingualText(
                zh="API服务和订阅模式",
                en="API services and subscription model"
            ),
            user_scale={
                "registered_users": "1亿+",
                "active_users": "5000万+",
                "source": "官方数据",
                "updated_at": "2023-12-01"
            }
        ),
        status=AgentStatus.RELEASED,
        tags=["NLP", "对话", "代码生成", "多语言"],
        metrics={
            "stars": 100000,
            "forks": 20000,
            "contributors": 500
        },
        timeline=[
            {
                "event": "首次发布",
                "date": "2022-11-30"
            },
            {
                "event": "GPT-4版本发布",
                "date": "2023-03-14"
            }
        ],
        is_verified=True
    )
    
    # 创建示例Agent 2 - Claude
    claude = AgentModel(
        name=MultilingualText(
            zh="Claude",
            en="Claude"
        ),
        slug="claude",
        logo_url="https://example.com/logos/claude.png",
        official_url="https://claude.ai",
        description=MultilingualDescription(
            short=MultilingualText(
                zh="Anthropic开发的AI助手",
                en="Anthropic's AI assistant"
            ),
            detailed=MultilingualText(
                zh="Claude是由Anthropic开发的AI助手，专注于安全性和可控性。",
                en="Claude is an AI assistant developed by Anthropic, focusing on safety and controllability."
            )
        ),
        development_team=DevelopmentTeam(
            name=MultilingualText(
                zh="Anthropic",
                en="Anthropic"
            ),
            location="San Francisco, USA",
            website="https://anthropic.com",
            description=MultilingualText(
                zh="AI安全研究公司",
                en="AI safety research company"
            )
        ),
        technical_stack=TechnicalStack(
            base_model=["Claude"],
            frameworks=["Transformers"],
            programming_languages=["Python"],
            deployment=["Cloud"]
        ),
        features=[
            MultilingualText(
                zh="宪法AI训练",
                en="Constitutional AI training"
            ),
            MultilingualText(
                zh="长文本处理",
                en="Long text processing"
            )
        ],
        business_info=BusinessInfo(
            funding=[
                FundingInfo(
                    round="C轮",
                    amount="45亿美元",
                    investors=["亚马逊", "谷歌", "其他投资者"],
                    date="2023-09"
                )
            ],
            business_model=MultilingualText(
                zh="企业API服务",
                en="Enterprise API services"
            )
        ),
        status=AgentStatus.RELEASED,
        tags=["NLP", "安全", "长文本"],
        is_verified=True
    )
    
    # 保存到数据库
    collection.insert_one(chatgpt.model_dump())
    collection.insert_one(claude.model_dump())
    
    print("Sample agents created successfully!")

async def main():
    """主函数"""
    await init_mongodb()
    await create_sample_agents()
    await mongodb_manager.close_mongodb()

if __name__ == "__main__":
    asyncio.run(main())