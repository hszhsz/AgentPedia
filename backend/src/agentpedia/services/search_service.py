"""
智能搜索服务
集成了Elasticsearch的Agent搜索功能
"""
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_
from agentpedia.core.elasticsearch import elasticsearch_manager
from agentpedia.services.mongodb_agent_service import mongodb_agent_service
from agentpedia.models.mongodb_models import AgentStatus, AgentModel
from agentpedia.schemas.agent_prd import AgentFilterParams, AgentSearchQuery
from agentpedia.core.logging import get_logger

logger = get_logger(__name__)


class SearchType(str, Enum):
    """搜索类型"""
    KEYWORD = "keyword"
    SEMANTIC = "semantic"
    HYBRID = "hybrid"
    FUZZY = "fuzzy"


class SortType(str, Enum):
    """排序类型"""
    RELEVANCE = "relevance"
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"
    POPULARITY = "popularity"
    NAME = "name"


class SearchService:
    """智能搜索服务"""

    def __init__(self):
        self.elasticsearch_available = False

    async def initialize(self):
        """初始化搜索服务"""
        try:
            await elasticsearch_manager.init_elasticsearch()
            self.elasticsearch_available = True
            logger.info("Search service initialized with Elasticsearch")
        except Exception as e:
            logger.warning(f"Elasticsearch not available, falling back to MongoDB search: {e}")
            self.elasticsearch_available = False

    async def search_agents(
        self,
        query: str,
        search_type: SearchType = SearchType.HYBRID,
        filters: Optional[Dict[str, Any]] = None,
        sort_by: SortType = SortType.RELEVANCE,
        page: int = 1,
        size: int = 20,
        language: str = "zh"
    ) -> Dict[str, Any]:
        """搜索Agent"""
        if self.elasticsearch_available:
            return await self._search_with_elasticsearch(
                query, search_type, filters, sort_by, page, size, language
            )
        else:
            return await self._search_with_mongodb(
                query, filters, sort_by, page, size, language
            )

    async def _search_with_elasticsearch(
        self,
        query: str,
        search_type: SearchType,
        filters: Optional[Dict[str, Any]],
        sort_by: SortType,
        page: int,
        size: int,
        language: str
    ) -> Dict[str, Any]:
        """使用Elasticsearch搜索"""
        try:
            # 构建搜索查询
            search_query = await self._build_elasticsearch_query(
                query, search_type, filters, sort_by, page, size, language
            )

            # 执行搜索
            response = await elasticsearch_manager.search_agents(search_query)

            # 处理结果
            hits = response.get("hits", {})
            total = hits.get("total", {}).get("value", 0)
            items = [hit["_source"] for hit in hits.get("hits", [])]

            return {
                "items": items,
                "total": total,
                "page": page,
                "size": size,
                "pages": (total + size - 1) // size,
                "search_type": "elasticsearch",
                "query": query
            }

        except Exception as e:
            logger.error(f"Elasticsearch search failed: {e}")
            # 降级到MongoDB搜索
            return await self._search_with_mongodb(
                query, filters, sort_by, page, size, language
            )

    async def _build_elasticsearch_query(
        self,
        query: str,
        search_type: SearchType,
        filters: Optional[Dict[str, Any]],
        sort_by: SortType,
        page: int,
        size: int,
        language: str
    ) -> Dict[str, Any]:
        """构建Elasticsearch查询"""
        from_idx = (page - 1) * size

        # 基础查询结构
        search_query = {
            "from": from_idx,
            "size": size,
            "query": {
                "bool": {
                    "must": [],
                    "filter": []
                }
            }
        }

        # 构建搜索条件
        if search_type == SearchType.KEYWORD:
            # 关键词搜索
            search_query["query"]["bool"]["must"].append({
                "multi_match": {
                    "query": query,
                    "fields": [
                        f"name.{language}^3",
                        f"name.{language.split('_')[0] if '_' in language else language}^3",
                        f"description.short.{language}^2",
                        f"description.detailed.{language}",
                        f"features.{language}",
                        "tags^2"
                    ],
                    "type": "best_fields",
                    "fuzziness": "AUTO"
                }
            })

        elif search_type == SearchType.SEMANTIC:
            # 语义搜索（简化版本，实际需要向量嵌入）
            search_query["query"]["bool"]["must"].append({
                "multi_match": {
                    "query": query,
                    "fields": [
                        f"name.{language}^3",
                        f"description.short.{language}^2",
                        f"description.detailed.{language}",
                        f"features.{language}"
                    ],
                    "type": "cross_fields"
                }
            })

        elif search_type == SearchType.HYBRID:
            # 混合搜索
            search_query["query"]["bool"]["must"].extend([
                {
                    "multi_match": {
                        "query": query,
                        "fields": [
                            f"name.{language}^3",
                            f"description.short.{language}^2",
                            "tags^2"
                        ],
                        "type": "best_fields",
                        "boost": 2
                    }
                },
                {
                    "multi_match": {
                        "query": query,
                        "fields": [
                            f"description.detailed.{language}",
                            f"features.{language}"
                        ],
                        "type": "cross_fields"
                    }
                }
            ])

        elif search_type == SearchType.FUZZY:
            # 模糊搜索
            search_query["query"]["bool"]["must"].append({
                "multi_match": {
                    "query": query,
                    "fields": [
                        f"name.{language}",
                        f"description.short.{language}",
                        f"features.{language}",
                        "tags"
                    ],
                    "type": "best_fields",
                    "fuzziness": "AUTO",
                    "prefix_length": 2
                }
            })

        # 添加过滤条件
        if filters:
            if "status" in filters:
                search_query["query"]["bool"]["filter"].append({
                    "term": {"status": filters["status"]}
                })

            if "tags" in filters and filters["tags"]:
                search_query["query"]["bool"]["filter"].append({
                    "terms": {"tags": filters["tags"]}
                })

            if "technical_stack" in filters and filters["technical_stack"]:
                for tech in filters["technical_stack"]:
                    search_query["query"]["bool"]["filter"].append({
                        "term": {f"technical_stack.{tech}.keyword": tech}
                    })

        # 添加排序
        search_query["sort"] = self._build_elasticsearch_sort(sort_by)

        return search_query

    def _build_elasticsearch_sort(self, sort_by: SortType) -> List[Dict[str, Any]]:
        """构建Elasticsearch排序"""
        if sort_by == SortType.RELEVANCE:
            return ["_score"]
        elif sort_by == SortType.CREATED_AT:
            return [{"created_at": {"order": "desc"}}]
        elif sort_by == SortType.UPDATED_AT:
            return [{"updated_at": {"order": "desc"}}]
        elif sort_by == SortType.POPULARITY:
            return [{"popularity_score": {"order": "desc"}}]
        elif sort_by == SortType.NAME:
            return [{"name.zh.keyword": {"order": "asc"}}]
        else:
            return ["_score"]

    async def _search_with_mongodb(
        self,
        query: str,
        filters: Optional[Dict[str, Any]],
        sort_by: SortType,
        page: int,
        size: int,
        language: str
    ) -> Dict[str, Any]:
        """使用MongoDB搜索"""
        try:
            # 构建查询条件
            query_filter = await self._build_mongodb_query(query, filters, language)

            # 获取总数
            total = await mongodb_agent_service.count_agents(query_filter)

            # 获取分页数据
            agents = await mongodb_agent_service.get_agents(
                query_filter,
                sort_by=self._build_mongodb_sort(sort_by),
                page=page,
                size=size
            )

            return {
                "items": [agent.dict() for agent in agents],
                "total": total,
                "page": page,
                "size": size,
                "pages": (total + size - 1) // size,
                "search_type": "mongodb",
                "query": query
            }

        except Exception as e:
            logger.error(f"MongoDB search failed: {e}")
            return {
                "items": [],
                "total": 0,
                "page": page,
                "size": size,
                "pages": 0,
                "search_type": "error",
                "query": query
            }

    async def _build_mongodb_query(
        self,
        query: str,
        filters: Optional[Dict[str, Any]],
        language: str
    ) -> Dict[str, Any]:
        """构建MongoDB查询"""
        query_filter = {"$and": []}

        # 文本搜索条件
        text_conditions = []
        if query:
            # 搜索名称
            name_field = f"name.{language}" if language in ["zh", "en"] else "name.zh"
            text_conditions.append({name_field: {"$regex": query, "$options": "i"}})

            # 搜索描述
            desc_short_field = f"description.short.{language}" if language in ["zh", "en"] else "description.short.zh"
            desc_detailed_field = f"description.detailed.{language}" if language in ["zh", "en"] else "description.detailed.zh"
            text_conditions.append({desc_short_field: {"$regex": query, "$options": "i"}})
            text_conditions.append({desc_detailed_field: {"$regex": query, "$options": "i"}})

            # 搜索标签
            text_conditions.append({"tags": {"$regex": query, "$options": "i"}})

        if text_conditions:
            query_filter["$and"].append({"$or": text_conditions})

        # 添加过滤条件
        if filters:
            if "status" in filters:
                query_filter["$and"].append({"status": filters["status"]})

            if "tags" in filters and filters["tags"]:
                query_filter["$and"].append({"tags": {"$in": filters["tags"]}})

            if "technical_stack" in filters and filters["technical_stack"]:
                for tech in filters["technical_stack"]:
                    query_filter["$and"].append({f"technical_stack.{tech}": {"$in": [tech]}})

        # 如果没有条件，返回空查询
        if not query_filter["$and"]:
            return {}

        return query_filter

    def _build_mongodb_sort(self, sort_by: SortType) -> List[tuple]:
        """构建MongoDB排序"""
        if sort_by == SortType.RELEVANCE:
            return [("name.zh", 1)]  # MongoDB无法做相关性排序，使用名称排序
        elif sort_by == SortType.CREATED_AT:
            return [("created_at", -1)]
        elif sort_by == SortType.UPDATED_AT:
            return [("updated_at", -1)]
        elif sort_by == SortType.POPULARITY:
            return [("metrics.popularity_score", -1)]
        elif sort_by == SortType.NAME:
            return [("name.zh", 1)]
        else:
            return [("created_at", -1)]

    async def get_search_suggestions(
        self,
        query: str,
        size: int = 5,
        language: str = "zh"
    ) -> List[str]:
        """获取搜索建议"""
        if self.elasticsearch_available:
            try:
                return await elasticsearch_manager.get_agent_suggestions(query, size)
            except Exception as e:
                logger.error(f"Failed to get suggestions from Elasticsearch: {e}")

        # 使用MongoDB获取建议
        try:
            agents = await mongodb_agent_service.get_agents(
                {"name.zh": {"$regex": f"^{query}", "$options": "i"}},
                size=size
            )
            return [agent.name.zh for agent in agents if agent.name.zh]
        except Exception as e:
            logger.error(f"Failed to get suggestions from MongoDB: {e}")
            return []

    async def index_agent(self, agent_data: Dict[str, Any]):
        """索引Agent到Elasticsearch"""
        if self.elasticsearch_available:
            try:
                await elasticsearch_manager.index_agent(agent_data)
                logger.info(f"Successfully indexed agent {agent_data.get('id')}")
            except Exception as e:
                logger.error(f"Failed to index agent {agent_data.get('id')}: {e}")

    async def reindex_all_agents(self):
        """重新索引所有Agent"""
        if not self.elasticsearch_available:
            logger.warning("Elasticsearch not available, skipping reindex")
            return

        try:
            # 获取所有Agent
            agents = await mongodb_agent_service.get_agents({})

            # 批量索引
            indexed_count = 0
            for agent in agents:
                await self.index_agent(agent.dict())
                indexed_count += 1

            logger.info(f"Successfully reindexed {indexed_count} agents")
            return indexed_count

        except Exception as e:
            logger.error(f"Failed to reindex agents: {e}")
            return 0

    async def get_popular_agents(
        self,
        limit: int = 10,
        time_range: Optional[int] = None  # days
    ) -> List[Dict[str, Any]]:
        """获取热门Agent"""
        if self.elasticsearch_available:
            # 使用Elasticsearch聚合获取热门Agent
            try:
                query = {
                    "size": limit,
                    "sort": [{"popularity_score": {"order": "desc"}}],
                    "query": {"match_all": {}}
                }

                if time_range:
                    # 添加时间范围过滤
                    from datetime import datetime, timedelta
                    start_date = (datetime.now() - timedelta(days=time_range)).isoformat()
                    query["query"] = {
                        "range": {
                            "created_at": {"gte": start_date}
                        }
                    }

                response = await elasticsearch_manager.search_agents(query)
                return [hit["_source"] for hit in response.get("hits", {}).get("hits", [])]

            except Exception as e:
                logger.error(f"Failed to get popular agents from Elasticsearch: {e}")

        # 使用MongoDB获取热门Agent
        try:
            filter_query = {}
            if time_range:
                from datetime import datetime, timedelta
                start_date = datetime.now() - timedelta(days=time_range)
                filter_query["created_at"] = {"$gte": start_date}

            agents = await mongodb_agent_service.get_agents(
                filter_query,
                sort_by=[("metrics.popularity_score", -1)],
                size=limit
            )
            return [agent.dict() for agent in agents]

        except Exception as e:
            logger.error(f"Failed to get popular agents from MongoDB: {e}")
            return []


# 创建全局搜索服务实例
search_service = SearchService()