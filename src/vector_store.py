# -*- coding: utf-8 -*-
"""
Vector Store - Elasticsearch vector operations
Elasticsearch 向量存储操作

This module provides:
1. ES connection management
2. Index creation with vector mapping
3. Seed data indexing
4. Vector similarity search

本模块提供：
1. ES 连接管理
2. 带向量映射的索引创建
3. 种子数据索引
4. 向量相似度搜索
"""

import logging
from typing import List, Dict, Optional, Any
from elasticsearch import Elasticsearch, NotFoundError
import config

logger = logging.getLogger(__name__)


class VectorStore:
    """
    Elasticsearch vector store for intent classification.
    用于意图分类的 ES 向量存储。
    
    Handles:
    - Index creation with dense_vector mapping
    - Seed data indexing
    - Vector similarity search
    
    处理：
    - 创建带 dense_vector 映射的索引
    - 种子数据索引
    - 向量相似度搜索
    
    Attributes:
        es_client: Elasticsearch client / ES 客户端
        index_name: Index name for seed vectors / 种子向量索引名称
    """
    
    # ES Index mapping for intent classification
    # 用于意图分类的 ES 索引映射
    INDEX_MAPPING = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0,
            "analysis": {
                "analyzer": {
                    "default": {
                        "type": "standard"
                    }
                }
            }
        },
        "mappings": {
            "properties": {
                "text": {
                    "type": "text",
                    "analyzer": "standard"
                },
                "category": {
                    "type": "keyword"
                },
                "sub_category": {
                    "type": "keyword"
                },
                "embedding": {
                    "type": "dense_vector",
                    "dims": config.EMBEDDING_DIM,
                    "index": True,
                    "similarity": "cosine"
                },
                "metadata": {
                    "type": "object",
                    "properties": {
                        "source": {"type": "keyword"},
                        "lang": {"type": "keyword"},
                        "priority": {"type": "integer"}
                    }
                }
            }
        }
    }
    
    def __init__(self, es_host: Optional[str] = None, index_name: Optional[str] = None):
        """
        Initialize vector store with ES connection.
        初始化向量存储并连接 ES。
        
        Args:
            es_host: Elasticsearch host URL / ES 主机地址
            index_name: Index name / 索引名称
        """
        self.es_host = es_host or config.ES_HOST
        self.index_name = index_name or config.ES_INDEX
        self.es_client = None
        self._connect()
        logger.info(f"VectorStore initialized with index: {self.index_name}")
    
    def _connect(self):
        """Connect to Elasticsearch / 连接到 Elasticsearch"""
        try:
            self.es_client = Elasticsearch(
                [self.es_host],
                verify_certs=False,
                request_timeout=30
            )
            # Test connection / 测试连接
            if not self.es_client.ping():
                raise ConnectionError("Cannot connect to Elasticsearch")
            logger.info(f"Connected to Elasticsearch at {self.es_host}")
        except Exception as e:
            logger.error(f"Failed to connect to Elasticsearch: {e}")
            raise ConnectionError(f"ES connection failed: {str(e)}")
    
    def create_index(self, force: bool = False) -> bool:
        """
        Create the index with vector mapping.
        创建带向量映射的索引。
        
        Args:
            force: If True, delete existing index first / 是否强制重建
        
        Returns:
            bool: True if created, False if already exists / 是否创建成功
        """
        try:
            if self.es_client.indices.exists(index=self.index_name):
                if force:
                    self.es_client.indices.delete(index=self.index_name)
                    logger.info(f"Deleted existing index: {self.index_name}")
                else:
                    logger.info(f"Index already exists: {self.index_name}")
                    return False
            
            self.es_client.indices.create(
                index=self.index_name,
                body=self.INDEX_MAPPING
            )
            logger.info(f"Created index: {self.index_name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to create index: {e}")
            raise
    
    def index_document(self, doc_id: str, text: str, embedding: List[float],
                       category: str, sub_category: str, metadata: Optional[Dict] = None) -> bool:
        """
        Index a single document with embedding.
        索引单个带向量的文档。
        
        Args:
            doc_id: Document ID / 文档 ID
            text: Original text / 原始文本
            embedding: Vector embedding / 向量
            category: Category / 分类
            sub_category: Sub-category / 子分类
            metadata: Additional metadata / 额外元数据
        
        Returns:
            bool: True if indexed successfully / 是否索引成功
        """
        try:
            doc = {
                "text": text,
                "category": category,
                "sub_category": sub_category,
                "embedding": embedding,
                "metadata": metadata or {}
            }
            
            self.es_client.index(
                index=self.index_name,
                id=doc_id,
                document=doc
            )
            logger.debug(f"Indexed document: {doc_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to index document {doc_id}: {e}")
            return False
    
    def index_batch(self, documents: List[Dict]) -> int:
        """
        Batch index multiple documents.
        批量索引多个文档。
        
        Args:
            documents: List of documents, each with keys: text, embedding, category, sub_category
        
        Returns:
            int: Number of successfully indexed documents / 成功索引数量
        """
        success_count = 0
        for i, doc in enumerate(documents):
            try:
                doc_id = f"seed_{i}_{doc['category']}"
                self.index_document(
                    doc_id=doc_id,
                    text=doc["text"],
                    embedding=doc["embedding"],
                    category=doc["category"],
                    sub_category=doc.get("sub_category", ""),
                    metadata=doc.get("metadata", {})
                )
                success_count += 1
            except Exception as e:
                logger.warning(f"Failed to index doc {i}: {e}")
        
        # Refresh to make documents searchable / 刷新使文档可搜索
        self.es_client.indices.refresh(index=self.index_name)
        logger.info(f"Batch indexed {success_count}/{len(documents)} documents")
        return success_count
    
    def search_similar(self, embedding: List[float], top_k: int = 5) -> List[Dict]:
        """
        Search for similar vectors.
        搜索相似向量。
        
        Args:
            embedding: Query vector / 查询向量
            top_k: Number of results to return / 返回结果数量
        
        Returns:
            List[Dict]: List of matching documents with scores / 匹配文档列表(含分数)
        """
        try:
            query = {
                "size": top_k,
                "query": {
                    "script_score": {
                        "query": {"match_all": {}},
                        "script": {
                            "source": "cosineSimilarity(params.query_vector, 'embedding') + 1.0",
                            "params": {"query_vector": embedding}
                        }
                    }
                }
            }
            
            response = self.es_client.search(
                index=self.index_name,
                body=query
            )
            
            results = []
            for hit in response["hits"]["hits"]:
                results.append({
                    "doc_id": hit["_id"],
                    "text": hit["_source"].get("text", ""),
                    "category": hit["_source"].get("category", ""),
                    "sub_category": hit["_source"].get("sub_category", ""),
                    "score": hit["_score"] / 2.0,  # Normalize from 0-2 to 0-1
                    "metadata": hit["_source"].get("metadata", {})
                })
            
            return results
            
        except Exception as e:
            logger.error(f"Vector search failed: {e}")
            return []
    
    def delete_index(self) -> bool:
        """
        Delete the index.
        删除索引。
        
        Returns:
            bool: True if deleted / 是否删除成功
        """
        try:
            if self.es_client.indices.exists(index=self.index_name):
                self.es_client.indices.delete(index=self.index_name)
                logger.info(f"Deleted index: {self.index_name}")
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to delete index: {e}")
            return False
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get index statistics.
        获取索引统计信息。
        
        Returns:
            Dict: Index stats / 索引统计
        """
        try:
            stats = self.es_client.indices.stats(index=self.index_name)
            return {
                "doc_count": stats["_all"]["primaries"]["docs"]["count"],
                "size_bytes": stats["_all"]["primaries"]["store"]["size_in_bytes"]
            }
        except Exception as e:
            logger.error(f"Failed to get stats: {e}")
            return {"doc_count": 0, "size_bytes": 0}


if __name__ == "__main__":
    # Demo usage / 示例用法
    logging.basicConfig(level=logging.INFO)
    
    try:
        store = VectorStore()
        
        # Create index / 创建索引
        store.create_index(force=True)
        
        print("VectorStore is ready. Use seed_data.py to populate seed examples.")
        
    except ConnectionError as e:
        print(f"Cannot connect to ES: {e}")
        print("Please ensure Elasticsearch is running at", config.ES_HOST)