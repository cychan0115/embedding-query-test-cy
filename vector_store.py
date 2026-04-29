"""
Vector store module using Elasticsearch / 使用 Elasticsearch 的向量存储模块
Handles index creation, document indexing, and vector similarity search
处理索引创建、文档索引和向量相似度搜索

Bilingual docstrings: Chinese first, English second
双语言文档字符串：中文优先，英文第二
"""

import logging
from typing import List, Dict, Any, Optional

from elasticsearch import Elasticsearch, NotFoundError
from elasticsearch.helpers import bulk

from config import Config, get_config

logger = logging.getLogger(__name__)


class VectorStore:
    """
    Elasticsearch vector store for intent classification / 用于意图分类的 Elasticsearch 向量存储

    Provides methods for creating indices, indexing documents with embeddings,
    and performing vector similarity searches.

    提供用于创建索引、用嵌入索引文档和执行向量相似度搜索的方法。

    Attributes:
        config: Configuration object / 配置对象
        client: Elasticsearch client / Elasticsearch 客户端
        index_name: Name of the index / 索引名称
    """

    def __init__(self, config: Optional[Config] = None):
        """
        Initialize the vector store / 初始化向量存储

        Args:
            config: Configuration object. If None, uses default config.
                    配置对象。如果为 None，使用默认配置。
        """
        self.config = config or get_config()
        self._client: Optional[Elasticsearch] = None
        self.index_name = self.config.es_index
        logger.info(f"VectorStore initialized for index: {self.index_name}")

    @property
    def client(self) -> Elasticsearch:
        """
        Lazy loading of Elasticsearch client / Elasticsearch 客户端的惰性加载

        Returns:
            Elasticsearch client instance / Elasticsearch 客户端实例
        """
        if self._client is None:
            logger.info(f"Connecting to Elasticsearch at {self.config.es_scheme}://{self.config.es_host}:{self.config.es_port}")

            # Build connection arguments / 构建连接参数
            es_kwargs = {
                "hosts": [f"{self.config.es_scheme}://{self.config.es_host}:{self.config.es_port}"],
            }

            # Add authentication if provided / 如果提供了认证则添加
            if self.config.es_user and self.config.es_password:
                es_kwargs["basic_auth"] = (self.config.es_user, self.config.es_password)
                logger.debug("Using basic authentication for Elasticsearch")

            self._client = Elasticsearch(**es_kwargs)

            # Verify connection / 验证连接
            if not self._client.ping():
                raise ConnectionError("Failed to connect to Elasticsearch / 无法连接到 Elasticsearch")

            logger.info("Successfully connected to Elasticsearch")

        return self._client

    @property
    def index_mapping(self) -> Dict[str, Any]:
        """
        Get the Elasticsearch index mapping definition / 获取 Elasticsearch 索引映射定义

        Returns:
            Dictionary containing the index mapping / 包含索引映射的字典
        """
        return {
            "mappings": {
                "properties": {
                    "text": {"type": "text"},
                    "category": {"type": "keyword"},
                    "sub_category": {"type": "keyword"},
                    "embedding": {
                        "type": "dense_vector",
                        "dims": self.config.dimensions,
                        "index": True,
                        "similarity": "cosine"
                    },
                    "metadata": {"type": "object", "enabled": True}
                }
            },
            "settings": {
                "number_of_shards": 1,
                "number_of_replicas": 0,
                "index": {
                    "knn": True  # Enable k-NN search / 启用 k-NN 搜索
                }
            }
        }

    def create_index(self, recreate: bool = False) -> bool:
        """
        Create the Elasticsearch index / 创建 Elasticsearch 索引

        Args:
            recreate: If True, delete existing index first.
                      如果为 True，先删除现有索引。

        Returns:
            True if index was created or already exists / 如果索引已创建或已存在则返回 True
        """
        try:
            if self.client.indices.exists(index=self.index_name):
                if recreate:
                    logger.info(f"Deleting existing index: {self.index_name}")
                    self.client.indices.delete(index=self.index_name)
                else:
                    logger.info(f"Index already exists: {self.index_name}")
                    return True

            logger.info(f"Creating index: {self.index_name}")
            self.client.indices.create(index=self.index_name, body=self.index_mapping)
            logger.info(f"Index created successfully: {self.index_name}")
            return True

        except Exception as e:
            logger.error(f"Failed to create index: {e}")
            raise

    def index_document(
        self,
        text: str,
        category: str,
        embedding: List[float],
        sub_category: Optional[str] = None,
        metadata: Optional[Dict] = None
    ) -> str:
        """
        Index a single document / 索引单个文档

        Args:
            text: The text content / 文本内容
            category: The category / 类别
            embedding: The embedding vector / 嵌入向量
            sub_category: Optional sub-category / 可选的子类别
            metadata: Optional metadata dictionary / 可选的元数据字典

        Returns:
            The document ID / 文档 ID
        """
        doc = {
            "text": text,
            "category": category,
            "sub_category": sub_category,
            "embedding": embedding,
            "metadata": metadata or {}
        }

        result = self.client.index(index=self.index_name, document=doc)
        doc_id = result["_id"]
        logger.debug(f"Indexed document: {doc_id} with category: {category}")
        return doc_id

    def bulk_index(self, documents: List[Dict[str, Any]]) -> Dict[str, int]:
        """
        Bulk index multiple documents / 批量索引多个文档

        Args:
            documents: List of document dictionaries with keys:
                       text, category, sub_category, embedding, metadata

        Returns:
            Dictionary with success and failure counts
            包含成功和失败计数的字典
        """
        actions = []
        for doc in documents:
            action = {
                "_index": self.index_name,
                "_source": {
                    "text": doc["text"],
                    "category": doc["category"],
                    "sub_category": doc.get("sub_category"),
                    "embedding": doc["embedding"],
                    "metadata": doc.get("metadata", {})
                }
            }
            actions.append(action)

        success, errors = bulk(self.client, actions, raise_on_error=False)
        logger.info(f"Bulk indexed {success} documents, {len(errors) if errors else 0} errors")

        return {"success": success, "failed": len(errors) if errors else 0, "errors": errors or []}

    def search(
        self,
        query_vector: List[float],
        top_k: int = 5,
        category_filter: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Search for similar documents using vector similarity / 使用向量相似度搜索相似文档

        Args:
            query_vector: The query embedding vector / 查询嵌入向量
            top_k: Number of results to return / 返回结果数量
            category_filter: Optional category to filter results
                             可选的类别过滤器

        Returns:
            List of matching documents with scores / 带分数的匹配文档列表
        """
        # Build the k-NN search query / 构建 k-NN 搜索查询
        query = {
            "knn": {
                "field": "embedding",
                "query_vector": query_vector,
                "k": top_k,
                "num_candidates": top_k * 2
            },
            "_source": ["text", "category", "sub_category", "metadata"]
        }

        # Add category filter if specified / 如果指定了类别过滤则添加
        if category_filter:
            query["query"] = {
                "term": {"category": category_filter}
            }
            query["post_filter"] = {
                "term": {"category": category_filter}
            }

        try:
            response = self.client.search(index=self.index_name, body=query)
            hits = response["hits"]["hits"]

            results = []
            for hit in hits:
                results.append({
                    "id": hit["_id"],
                    "text": hit["_source"]["text"],
                    "category": hit["_source"]["category"],
                    "sub_category": hit["_source"].get("sub_category"),
                    "score": hit["_score"],
                    "metadata": hit["_source"].get("metadata", {})
                })

            logger.debug(f"Search returned {len(results)} results")
            return results

        except NotFoundError:
            logger.warning(f"Index not found: {self.index_name}")
            return []
        except Exception as e:
            logger.error(f"Search failed: {e}")
            raise

    def search_by_text(
        self,
        text: str,
        embedding: List[float],
        top_k: int = 5,
        category_filter: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Search for similar documents by text / 通过文本搜索相似文档

        Args:
            text: The text to search for / 要搜索的文本
            embedding: The embedding vector / 嵌入向量
            top_k: Number of results to return / 返回结果数量
            category_filter: Optional category to filter results
                             可选的类别过滤器

        Returns:
            List of matching documents with scores / 带分数的匹配文档列表
        """
        results = self.search(embedding, top_k, category_filter)
        # Add the query text to results for reference / 将查询文本添加到结果中以供参考
        for result in results:
            result["query_text"] = text
        return results

    def delete_index(self) -> bool:
        """
        Delete the index / 删除索引

        Returns:
            True if deleted successfully / 如果删除成功则返回 True
        """
        try:
            if self.client.indices.exists(index=self.index_name):
                self.client.indices.delete(index=self.index_name)
                logger.info(f"Index deleted: {self.index_name}")
                return True
            else:
                logger.info(f"Index does not exist: {self.index_name}")
                return False
        except Exception as e:
            logger.error(f"Failed to delete index: {e}")
            raise

    def get_document_count(self) -> int:
        """
        Get the number of documents in the index / 获取索引中的文档数量

        Returns:
            Number of documents / 文档数量
        """
        try:
            response = self.client.count(index=self.index_name)
            return response["count"]
        except NotFoundError:
            return 0

    def close(self):
        """Close the Elasticsearch client / 关闭 Elasticsearch 客户端"""
        if self._client:
            self._client.close()
            self._client = None
            logger.info("Elasticsearch client closed")


# Singleton instance / 单例实例
_vector_store: Optional[VectorStore] = None


def get_vector_store(config: Optional[Config] = None) -> VectorStore:
    """
    Get the global vector store instance / 获取全局向量存储实例

    Args:
        config: Optional configuration override / 可选的配置覆盖

    Returns:
        VectorStore instance / 向量存储实例
    """
    global _vector_store
    if _vector_store is None or config is not None:
        _vector_store = VectorStore(config)
    return _vector_store