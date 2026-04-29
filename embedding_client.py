"""
Embedding client module / 嵌入客户端模块
Handles text embedding generation using sentence transformers
使用句子转换器处理文本嵌入生成

Bilingual docstrings: Chinese first, English second
双语言文档字符串：中文优先，英文第二
"""

import logging
from typing import List, Union, Optional

import numpy as np
from sentence_transformers import SentenceTransformer

from config import Config, get_config

logger = logging.getLogger(__name__)


class EmbeddingClient:
    """
    Embedding client for text vectorization / 文本向量化的嵌入客户端

    使用 sentence-transformers 库将文本转换为密集向量表示。
    Uses the sentence-transformers library to convert text into dense vector representations.

    Attributes:
        config: Configuration object / 配置对象
        model: The sentence transformer model / 句子转换器模型
        dimensions: Embedding vector dimensions / 嵌入向量维度
    """

    def __init__(self, config: Optional[Config] = None):
        """
        Initialize the embedding client / 初始化嵌入客户端

        Args:
            config: Configuration object. If None, uses default config.
                    配置对象。如果为 None，使用默认配置。
        """
        self.config = config or get_config()
        self._model: Optional[SentenceTransformer] = None
        self._dimensions: Optional[int] = None
        logger.info(f"EmbeddingClient initialized with model: {self.config.embedding_model}")

    @property
    def model(self) -> SentenceTransformer:
        """
        Lazy loading of the sentence transformer model / 句子转换器模型的惰性加载

        Returns:
            The loaded SentenceTransformer model / 加载的 SentenceTransformer 模型
        """
        if self._model is None:
            logger.info(f"Loading embedding model: {self.config.embedding_model}")
            self._model = SentenceTransformer(self.config.embedding_model)
            self._dimensions = self._model.get_sentence_embedding_dimension()
            logger.info(f"Model loaded. Embedding dimensions: {self._dimensions}")
        return self._model

    def encode(self, texts: Union[str, List[str]]) -> np.ndarray:
        """
        Encode text(s) into embedding vectors / 将文本编码为嵌入向量

        Args:
            texts: Single text string or list of text strings.
                   单个文本字符串或文本字符串列表。

        Returns:
            numpy array of embeddings with shape (n_texts, dimensions)
            嵌入向量数组，形状为 (n_texts, dimensions)

        Example:
            >>> client = EmbeddingClient()
            >>> embedding = client.encode("Hello world")
            >>> embeddings = client.encode(["Hello", "World"])
        """
        if isinstance(texts, str):
            texts = [texts]

        if not texts:
            raise ValueError("Empty text list provided / 提供了空的文本列表")

        logger.debug(f"Encoding {len(texts)} text(s)")
        embeddings = self.model.encode(
            texts,
            batch_size=self.config.embedding_batch_size,
            show_progress_bar=len(texts) > 10,
            convert_to_numpy=True,
            normalize_embeddings=True,  # Normalize for cosine similarity / 归一化以计算余弦相似度
        )

        return embeddings

    def get_dimensions(self) -> int:
        """
        Get the embedding vector dimensions / 获取嵌入向量维度

        Returns:
            The number of dimensions in each embedding vector / 每个嵌入向量的维度数
        """
        if self._dimensions is None:
            # Trigger model loading to get dimensions / 触发模型加载以获取维度
            _ = self.model
        return self._dimensions or self.config.dimensions

    def similarity(self, text1: str, text2: str) -> float:
        """
        Calculate cosine similarity between two texts / 计算两个文本之间的余弦相似度

        Args:
            text1: First text / 第一个文本
            text2: Second text / 第二个文本

        Returns:
            Cosine similarity score between 0 and 1 / 0到1之间的余弦相似度分数
        """
        embeddings = self.encode([text1, text2])
        # Since embeddings are normalized, dot product = cosine similarity
        # 由于嵌入已归一化，点积 = 余弦相似度
        similarity = np.dot(embeddings[0], embeddings[1])
        return float(similarity)

    def encode_with_metadata(self, texts: List[str]) -> List[dict]:
        """
        Encode texts and return with metadata / 编码文本并返回元数据

        Args:
            texts: List of text strings / 文本字符串列表

        Returns:
            List of dictionaries containing text and embedding
            包含文本和嵌入的字典列表
        """
        embeddings = self.encode(texts)
        return [
            {"text": text, "embedding": embedding}
            for text, embedding in zip(texts, embeddings)
        ]


# Singleton instance / 单例实例
_embedding_client: Optional[EmbeddingClient] = None


def get_embedding_client(config: Optional[Config] = None) -> EmbeddingClient:
    """
    Get the global embedding client instance / 获取全局嵌入客户端实例

    Args:
        config: Optional configuration override / 可选的配置覆盖

    Returns:
        EmbeddingClient instance / 嵌入客户端实例
    """
    global _embedding_client
    if _embedding_client is None or config is not None:
        _embedding_client = EmbeddingClient(config)
    return _embedding_client