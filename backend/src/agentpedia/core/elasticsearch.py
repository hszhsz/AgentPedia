"""
Elasticsearch 连接管理器
"""
from typing import Optional, Dict, Any, List
from elasticsearch import AsyncElasticsearch
from elasticsearch.exceptions import ConnectionError, NotFoundError
import logging

from agentpedia.core.config import get_settings

logger = logging.getLogger(__name__)


class ElasticsearchManager:
    """Elasticsearch 连接管理器"""

    def __init__(self):
        self.client: Optional[AsyncElasticsearch] = None
        self._initialized = False

    async def init_elasticsearch(self):
        """初始化 Elasticsearch 连接"""
        if self._initialized:
            return

        settings = get_settings()

        try:
            # 构建连接配置
            hosts = settings.ELASTICSEARCH_HOSTS.split(",")

            config = {
                "hosts": hosts,
                "request_timeout": 30,
                "max_retries": 3,
                "retry_on_timeout": True,
            }

            # SSL 配置
            if settings.ELASTICSEARCH_USE_SSL:
                config["use_ssl"] = True
                config["verify_certs"] = settings.ELASTICSEARCH_VERIFY_CERTS

            # 认证配置
            if settings.ELASTICSEARCH_USERNAME and settings.ELASTICSEARCH_PASSWORD:
                config["http_auth"] = (
                    settings.ELASTICSEARCH_USERNAME,
                    settings.ELASTICSEARCH_PASSWORD
                )

            # 创建客户端
            self.client = AsyncElasticsearch(**config)

            # 测试连接
            await self.client.ping()

            self._initialized = True
            logger.info("Elasticsearch connected successfully")

        except ConnectionError as e:
            logger.error(f"Failed to connect to Elasticsearch: {e}")
            raise
        except Exception as e:
            logger.error(f"Error initializing Elasticsearch: {e}")
            raise

    async def close_elasticsearch(self):
        """关闭 Elasticsearch 连接"""
        if self.client:
            await self.client.close()
            self._initialized = False
            logger.info("Elasticsearch connection closed")

    async def create_agent_index(self):
        """创建 Agent 索引"""
        if not self._initialized:
            raise RuntimeError("Elasticsearch not initialized")

        settings = get_settings()
        index_name = f"{settings.ELASTICSEARCH_INDEX_PREFIX}_agents"

        try:
            # 检查索引是否已存在
            if await self.client.indices.exists(index=index_name):
                logger.info(f"Index {index_name} already exists")
                return

            # 定义索引映射
            mapping = {
                "mappings": {
                    "properties": {
                        "name": {
                            "type": "object",
                            "properties": {
                                "zh": {
                                    "type": "text",
                                    "analyzer": "ik_max_word",
                                    "search_analyzer": "ik_smart"
                                },
                                "en": {
                                    "type": "text",
                                    "analyzer": "english"
                                }
                            }
                        },
                        "slug": {
                            "type": "keyword"
                        },
                        "description": {
                            "type": "object",
                            "properties": {
                                "short": {
                                    "type": "object",
                                    "properties": {
                                        "zh": {
                                            "type": "text",
                                            "analyzer": "ik_max_word",
                                            "search_analyzer": "ik_smart"
                                        },
                                        "en": {
                                            "type": "text",
                                            "analyzer": "english"
                                        }
                                    }
                                },
                                "detailed": {
                                    "type": "object",
                                    "properties": {
                                        "zh": {
                                            "type": "text",
                                            "analyzer": "ik_max_word",
                                            "search_analyzer": "ik_smart"
                                        },
                                        "en": {
                                            "type": "text",
                                            "analyzer": "english"
                                        }
                                    }
                                }
                            }
                        },
                        "features": {
                            "type": "object",
                            "properties": {
                                "zh": {
                                    "type": "text",
                                    "analyzer": "ik_max_word",
                                    "search_analyzer": "ik_smart"
                                },
                                "en": {
                                    "type": "text",
                                    "analyzer": "english"
                                }
                            }
                        },
                        "technical_stack": {
                            "type": "object",
                            "properties": {
                                "base_model": {"type": "keyword"},
                                "frameworks": {"type": "keyword"},
                                "programming_languages": {"type": "keyword"}
                            }
                        },
                        "tags": {"type": "keyword"},
                        "status": {"type": "keyword"},
                        "created_at": {"type": "date"},
                        "updated_at": {"type": "date"},
                        "popularity_score": {"type": "float"}
                    }
                },
                "settings": {
                    "number_of_shards": 1,
                    "number_of_replicas": 0,
                    "analysis": {
                        "analyzer": {
                            "ik_max_word": {
                                "type": "ik_max_word"
                            },
                            "ik_smart": {
                                "type": "ik_smart"
                            }
                        }
                    }
                }
            }

            # 创建索引
            await self.client.indices.create(index=index_name, body=mapping)
            logger.info(f"Created index: {index_name}")

        except Exception as e:
            logger.error(f"Failed to create agent index: {e}")
            raise

    async def index_agent(self, agent_data: Dict[str, Any]):
        """索引单个 Agent"""
        if not self._initialized:
            raise RuntimeError("Elasticsearch not initialized")

        settings = get_settings()
        index_name = f"{settings.ELASTICSEARCH_INDEX_PREFIX}_agents"

        try:
            await self.client.index(
                index=index_name,
                id=agent_data.get("id"),
                body=agent_data
            )
        except Exception as e:
            logger.error(f"Failed to index agent {agent_data.get('id')}: {e}")
            raise

    async def search_agents(self, query: Dict[str, Any]) -> Dict[str, Any]:
        """搜索 Agents"""
        if not self._initialized:
            raise RuntimeError("Elasticsearch not initialized")

        settings = get_settings()
        index_name = f"{settings.ELASTICSEARCH_INDEX_PREFIX}_agents"

        try:
            response = await self.client.search(index=index_name, body=query)
            return response
        except Exception as e:
            logger.error(f"Failed to search agents: {e}")
            raise

    async def delete_agent(self, agent_id: str):
        """删除 Agent 索引"""
        if not self._initialized:
            raise RuntimeError("Elasticsearch not initialized")

        settings = get_settings()
        index_name = f"{settings.ELASTICSEARCH_INDEX_PREFIX}_agents"

        try:
            await self.client.delete(index=index_name, id=agent_id)
        except NotFoundError:
            logger.warning(f"Agent {agent_id} not found in Elasticsearch")
        except Exception as e:
            logger.error(f"Failed to delete agent {agent_id}: {e}")
            raise

    async def get_agent_suggestions(self, query: str, size: int = 5) -> List[str]:
        """获取搜索建议"""
        if not self._initialized:
            raise RuntimeError("Elasticsearch not initialized")

        settings = get_settings()
        index_name = f"{settings.ELASTICSEARCH_INDEX_PREFIX}_agents"

        try:
            suggest_query = {
                "suggest": {
                    "name_suggest": {
                        "prefix": query,
                        "completion": {
                            "field": "name.zh",
                            "size": size
                        }
                    }
                }
            }

            response = await self.client.search(index=index_name, body=suggest_query)
            suggestions = [
                option["text"]
                for option in response["suggest"]["name_suggest"][0]["options"]
            ]
            return suggestions

        except Exception as e:
            logger.error(f"Failed to get suggestions: {e}")
            return []


# 创建全局 Elasticsearch 管理器实例
elasticsearch_manager = ElasticsearchManager()