# -*- coding: utf-8 -*-
"""
Embedding Client - 向量嵌入客户端
用于将文本转换为向量表示

This module provides:
1. Embedding generation via REST API
2. Support for batch embedding
3. Connection error handling

本模块提供：
1. 通过 REST API 生成向量
2. 批量向量生成支持
3. 连接错误处理
"""

import logging
import requests
from typing import List, Union, Optional
import config

logger = logging.getLogger(__name__)


class EmbeddingClient:
    """
    Embedding client for text-to-vector conversion.
    用于文本转向量的 Embedding 客户端。
    
    Attributes:
        api_url: Embedding service API endpoint / Embedding 服务 API 端点
        dimension: Vector dimension / 向量维度
    
    Example / 示例:
        >>> client = EmbeddingClient()
        >>> vector = client.embed("tell me about policy")
        >>> vectors = client.embed_batch(["hi", "hello"])
    """
    
    def __init__(self, api_url: Optional[str] = None, dimension: Optional[int] = None):
        """
        Initialize embedding client.
        初始化 Embedding 客户端。
        
        Args:
            api_url: Embedding API URL, defaults to config.EMBEDDING_API
            dimension: Vector dimension, defaults to config.EMBEDDING_DIM
        """
        self.api_url = api_url or config.EMBEDDING_API
        self.dimension = dimension or config.EMBEDDING_DIM
        self.timeout = 30  # Request timeout in seconds / 请求超时时间
        logger.info(f"EmbeddingClient initialized with API: {self.api_url}")
    
    def embed(self, text: str) -> List[float]:
        """
        Convert a single text to embedding vector.
        将单个文本转换为向量。
        
        Args:
            text: Input text / 输入文本
        
        Returns:
            List[float]: Embedding vector / 向量
        
        Raises:
            ConnectionError: If API is unreachable / API 无法连接
            ValueError: If API returns invalid response / API 返回无效响应
        """
        try:
            response = requests.post(
                self.api_url,
                json={"input": text},
                timeout=self.timeout,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            
            result = response.json()
            
            # Handle different response formats / 处理不同的响应格式
            if "data" in result and len(result["data"]) > 0:
                return result["data"][0].get("embedding", [])
            elif "embedding" in result:
                return result["embedding"]
            else:
                raise ValueError(f"Unexpected API response format: {result}")
                
        except requests.exceptions.Timeout:
            logger.error(f"Embedding API timeout for text: {text[:50]}...")
            raise ConnectionError("Embedding API timeout")
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Embedding API connection error: {e}")
            raise ConnectionError(f"Cannot connect to embedding API: {self.api_url}")
        except Exception as e:
            logger.error(f"Embedding error: {e}")
            raise
    
    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Convert multiple texts to embedding vectors in batch.
        批量将多个文本转换为向量。
        
        Args:
            texts: List of input texts / 输入文本列表
        
        Returns:
            List[List[float]]: List of embedding vectors / 向量列表
        
        Raises:
            ConnectionError: If API is unreachable / API 无法连接
        """
        try:
            response = requests.post(
                self.api_url,
                json={"input": texts},
                timeout=self.timeout * 2,  # Longer timeout for batch
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            
            result = response.json()
            
            if "data" in result:
                return [item.get("embedding", []) for item in result["data"]]
            elif "embeddings" in result:
                return result["embeddings"]
            else:
                raise ValueError(f"Unexpected batch API response format: {result}")
                
        except Exception as e:
            logger.error(f"Batch embedding error: {e}")
            raise ConnectionError(f"Batch embedding failed: {str(e)}")
    
    def embed_fake(self, text: str) -> List[float]:
        """
        Generate a fake embedding vector for testing.
        生成假的向量用于测试（当没有真实 API 时）。
        
        Args:
            text: Input text / 输入文本
        
        Returns:
            List[float]: Fake vector with consistent dimension / 假向量
        """
        # Simple hash-based fake vector for testing
        # 使用简单的哈希生成假向量用于测试
        import hashlib
        hash_bytes = hashlib.md5(text.encode()).digest()
        vector = [b / 255.0 * 2 - 1 for b in hash_bytes]
        # Pad to required dimension / 填充到所需维度
        while len(vector) < self.dimension:
            vector.extend(vector[:min(len(vector), self.dimension - len(vector))])
        return vector[:self.dimension]
    
    def get_dimension(self) -> int:
        """
        Get the embedding vector dimension.
        获取向量维度。
        
        Returns:
            int: Vector dimension / 向量维度
        """
        return self.dimension


if __name__ == "__main__":
    # Demo usage / 示例用法
    logging.basicConfig(level=logging.INFO)
    
    client = EmbeddingClient()
    
    # Test single embedding / 测试单个 embedding
    text = "tell me about the policy detail"
    try:
        vector = client.embed(text)
        print(f"Single embed dimension: {len(vector)}")
    except ConnectionError:
        # Fallback to fake embed / 回退到假 embedding
        vector = client.embed_fake(text)
        print(f"Using fake embed, dimension: {len(vector)}")