"""
Intent classifier module / 意图分类器模块
Main classifier combining pre-filtering, keyword rules, and vector similarity
结合预过滤、关键词规则和向量相似度的主分类器

Bilingual docstrings: Chinese first, English second
双语言文档字符串：中文优先，英文第二
"""

import logging
import re
from typing import Dict, Any, List, Optional

from config import Config, get_config
from embedding_client import EmbeddingClient, get_embedding_client
from vector_store import VectorStore, get_vector_store

logger = logging.getLogger(__name__)


class IntentClassifier:
    """
    Intent classifier using hybrid approach / 使用混合方法的意图分类器

    Classification Pipeline / 分类流程:
    1. Pre-filter: Empty, too short, or noise inputs / 预过滤：空、太短或噪声输入
    2. Keyword/Pattern rules: Fast classification using keywords / 关键词/模式规则：使用关键词快速分类
    3. Vector similarity: Semantic search in Elasticsearch / 向量相似度：在 Elasticsearch 中进行语义搜索
    4. Score thresholds: Determine final category / 分数阈值：确定最终类别

    Score Thresholds / 分数阈值:
    - >= 0.82: Use ES category / 使用 ES 类别
    - 0.70-0.82: Mark for LLM review / 标记为需 LLM 审核
    - < 0.70: Unknown / 未知
    """

    # Category display names / 类别显示名称
    CATEGORY_NAMES = {
        "meaningful_question": "meaningful_question (正式问题)",
        "casual_chat": "casual_chat (闲聊)",
        "time_weather_general": "time_weather_general (时间天气)",
        "operation_command": "operation_command (操作指令)",
        "noise_or_empty": "noise_or_empty (噪声)",
        "unknown": "unknown (未知)",
        "llm_review": "llm_review (需LLM审核)",
    }

    def __init__(self, config: Optional[Config] = None):
        """
        Initialize the intent classifier / 初始化意图分类器

        Args:
            config: Configuration object. If None, uses default config.
                    配置对象。如果为 None，使用默认配置。
        """
        self.config = config or get_config()
        self.embedding_client = get_embedding_client(self.config)
        self.vector_store = get_vector_store(self.config)
        logger.info("IntentClassifier initialized")

    def _prefilter(self, text: str) -> Optional[Dict[str, Any]]:
        """
        Pre-filter input text / 预过滤输入文本

        Checks for:
        - Empty or whitespace-only text / 空或仅空白文本
        - Text too short / 文本太短
        - Text too long / 文本太长
        - Noise patterns / 噪声模式

        Args:
            text: Input text / 输入文本

        Returns:
            Result dict if filtered, None if should proceed / 如果被过滤则返回结果字典，否则返回 None
        """
        # Check for empty or whitespace-only / 检查空或仅空白
        if not text or not text.strip():
            return {
                "category": "noise_or_empty",
                "confidence": 1.0,
                "method": "prefilter",
                "reason": "empty_input"
            }

        # Check text length / 检查文本长度
        text_stripped = text.strip()
        if len(text_stripped) < self.config.min_text_length:
            return {
                "category": "noise_or_empty",
                "confidence": 1.0,
                "method": "prefilter",
                "reason": "too_short"
            }

        if len(text_stripped) > self.config.max_text_length:
            return {
                "category": "noise_or_empty",
                "confidence": 1.0,
                "method": "prefilter",
                "reason": "too_long"
            }

        # Check noise patterns / 检查噪声模式
        for pattern in self.config.noise_patterns:
            if re.match(pattern, text_stripped):
                logger.debug(f"Text matched noise pattern: {pattern}")
                return {
                    "category": "noise_or_empty",
                    "confidence": 0.95,
                    "method": "prefilter",
                    "reason": "noise_pattern"
                }

        return None

    def _keyword_classify(self, text: str) -> Optional[Dict[str, Any]]:
        """
        Classify using keyword/pattern rules / 使用关键词/模式规则分类

        Fast classification using keyword matching without embedding search.

        Args:
            text: Input text (lowercase) / 输入文本（小写）

        Returns:
            Result dict if classified, None if no match / 如果分类则返回结果字典，否则返回 None
        """
        text_lower = text.lower()

        # Check each category's keywords / 检查每个类别的关键词
        category_scores = {}

        # meaningful_question keywords / 有意义问题关键词
        for keyword in self.config.keyword_weights.get("meaningful_question", []):
            if keyword in text_lower:
                category_scores["meaningful_question"] = category_scores.get("meaningful_question", 0) + 1

        # casual_chat keywords / 闲聊关键词
        for keyword in self.config.keyword_weights.get("casual_chat", []):
            if keyword in text_lower:
                category_scores["casual_chat"] = category_scores.get("casual_chat", 0) + 1

        # time_weather keywords / 时间天气关键词
        for keyword in self.config.keyword_weights.get("time_weather", []):
            if keyword in text_lower:
                category_scores["time_weather_general"] = category_scores.get("time_weather_general", 0) + 1

        # operation_command keywords / 操作指令关键词
        for keyword in self.config.keyword_weights.get("operation_command", []):
            if keyword in text_lower:
                category_scores["operation_command"] = category_scores.get("operation_command", 0) + 1

        # If we found keywords / 如果找到关键词
        if category_scores:
            # Get category with highest score / 获取分数最高的类别
            best_category = max(category_scores, key=category_scores.get)
            # Normalize confidence based on text length / 根据文本长度归一化置信度
            confidence = min(0.85, 0.5 + (category_scores[best_category] * 0.15))

            logger.debug(f"Keyword classification: {best_category} (score: {category_scores[best_category]})")

            return {
                "category": best_category,
                "confidence": confidence,
                "method": "keyword",
                "matched_keywords": category_scores
            }

        return None

    def _vector_search(self, text: str) -> Dict[str, Any]:
        """
        Classify using vector similarity search / 使用向量相似度搜索分类

        Args:
            text: Input text / 输入文本

        Returns:
            Search result with best match / 带最佳匹配结果的搜索结果
        """
        # Get embedding / 获取嵌入
        embedding = self.embedding_client.encode(text)

        # Search in Elasticsearch / 在 Elasticsearch 中搜索
        results = self.vector_store.search(
            query_vector=embedding.tolist(),
            top_k=self.config.default_top_k
        )

        if not results:
            return {
                "category": "unknown",
                "confidence": 0.0,
                "method": "vector",
                "reason": "no_results"
            }

        # Get best match / 获取最佳匹配
        best_match = results[0]

        return {
            "category": best_match["category"],
            "confidence": best_match["score"],
            "method": "vector",
            "best_match_text": best_match["text"],
            "best_match_sub_category": best_match.get("sub_category"),
            "all_results": results
        }

    def classify(self, text: str) -> Dict[str, Any]:
        """
        Classify the intent of input text / 分类输入文本的意图

        Pipeline / 流程:
        1. Pre-filter check / 预过滤检查
        2. Keyword-based quick classification / 基于关键词的快速分类
        3. Vector similarity search / 向量相似度搜索
        4. Score threshold application / 分数阈值应用

        Args:
            text: Input text to classify / 要分类的输入文本

        Returns:
            Dictionary containing classification result / 包含分类结果的字典
            {
                "category": str,        # Detected category / 检测到的类别
                "confidence": float,    # Confidence score (0-1) / 置信度分数 (0-1)
                "method": str,          # Classification method / 分类方法
                "sub_category": str,    # Sub-category if available / 子类别（如果有）
                "llm_review": bool,     # Whether LLM review is needed / 是否需要 LLM 审核
                "reason": str           # Reason for classification / 分类原因
            }
        """
        logger.info(f"Classifying text: {text[:50]}...")

        # Step 1: Pre-filter / 步骤 1：预过滤
        prefilter_result = self._prefilter(text)
        if prefilter_result:
            logger.info(f"Pre-filter result: {prefilter_result['reason']}")
            return prefilter_result

        # Step 2: Keyword classification / 步骤 2：关键词分类
        keyword_result = self._keyword_classify(text)
        if keyword_result and keyword_result["confidence"] >= 0.7:
            logger.info(f"Keyword classification: {keyword_result['category']}")
            return self._apply_threshold(keyword_result)

        # Step 3: Vector similarity search / 步骤 3：向量相似度搜索
        vector_result = self._vector_search(text)
        logger.info(f"Vector search result: category={vector_result['category']}, score={vector_result.get('confidence', 0):.3f}")

        # Step 4: Apply threshold / 步骤 4：应用阈值
        return self._apply_threshold(vector_result)

    def _apply_threshold(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Apply confidence threshold to determine final category / 应用置信度阈值确定最终类别

        Thresholds / 阈值:
        - >= 0.82: Use ES category / 使用 ES 类别
        - 0.70-0.82: Mark for LLM review / 标记为需 LLM 审核
        - < 0.70: Unknown / 未知

        Args:
            result: Classification result / 分类结果

        Returns:
            Result with threshold applied / 应用阈值后的结果
        """
        confidence = result.get("confidence", 0)

        if confidence >= self.config.similarity_threshold_high:
            result["llm_review"] = False
            result["reason"] = "high_confidence"
        elif confidence >= self.config.similarity_threshold_low:
            result["category"] = "llm_review"
            result["llm_review"] = True
            result["reason"] = "medium_confidence_ llm_review"
        else:
            result["category"] = "unknown"
            result["llm_review"] = True
            result["reason"] = "low_confidence"

        return result

    def batch_classify(self, texts: List[str]) -> List[Dict[str, Any]]:
        """
        Classify multiple texts / 分类多个文本

        Args:
            texts: List of input texts / 输入文本列表

        Returns:
            List of classification results / 分类结果列表
        """
        return [self.classify(text) for text in texts]

    def get_category_info(self, category: str) -> Dict[str, Any]:
        """
        Get information about a category / 获取类别信息

        Args:
            category: Category name / 类别名称

        Returns:
            Dictionary with category information / 包含类别信息的字典
        """
        descriptions = {
            "meaningful_question": "Formal questions seeking specific answers / 寻求具体答案的正式问题",
            "casual_chat": "Informal conversational exchanges / 非正式对话交流",
            "time_weather_general": "Queries about time, weather, or general info / 关于时间、天气或一般信息的查询",
            "operation_command": "Commands to perform operations / 执行操作的操作指令",
            "noise_or_empty": "Spam, gibberish, or empty inputs / 垃圾邮件、乱码或空输入",
            "unknown": "Unclassified or ambiguous inputs / 未分类或模糊的输入",
            "llm_review": "Needs LLM review for final classification / 需要 LLM 审核以进行最终分类",
        }

        return {
            "name": category,
            "display_name": self.CATEGORY_NAMES.get(category, category),
            "description": descriptions.get(category, "Unknown category / 未知类别"),
        }

    def initialize_index(self, recreate: bool = False) -> Dict[str, Any]:
        """
        Initialize the Elasticsearch index with seed data / 用种子数据初始化 Elasticsearch 索引

        Args:
            recreate: If True, delete and recreate the index.
                      如果为 True，删除并重新创建索引。

        Returns:
            Statistics about the initialization / 初始化的统计信息
        """
        from seed_data import get_all_seed_texts

        logger.info("Initializing index with seed data...")

        # Create index / 创建索引
        self.vector_store.create_index(recreate=recreate)

        # Get seed data / 获取种子数据
        seed_docs = get_all_seed_texts()

        # Generate embeddings for all seed data / 为所有种子数据生成嵌入
        texts = [doc["text"] for doc in seed_docs]
        embeddings = self.embedding_client.encode(texts)

        # Prepare documents for indexing / 准备索引文档
        documents = []
        for doc, embedding in zip(seed_docs, embeddings):
            documents.append({
                "text": doc["text"],
                "category": doc["category"],
                "sub_category": doc["sub_category"],
                "embedding": embedding.tolist(),
                "metadata": {
                    "source": "seed_data",
                    "indexed_at": str(__import__("datetime").datetime.utcnow())
                }
            })

        # Bulk index / 批量索引
        result = self.vector_store.bulk_index(documents)

        logger.info(f"Index initialization complete: {result}")

        return {
            "total_documents": len(documents),
            "success": result["success"],
            "failed": result["failed"],
        }