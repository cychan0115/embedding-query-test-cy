# -*- coding: utf-8 -*-
"""
Intent Classifier - Main classification logic
意图分类器 - 主要分类逻辑

This module implements a hybrid intent classification system:
1. Rule-based pre-filtering
2. Pattern matching (keywords, time, casual, operation)
3. Vector similarity search in Elasticsearch
4. Confidence-based decision

本模块实现混合意图分类系统：
1. 基于规则的预过滤
2. 模式匹配（关键词、时间、闲聊、操作）
3. Elasticsearch 向量相似度搜索
4. 基于置信度的决策

Classifier Flow / 分类器流程:
    User Input
         ↓
    ┌─────────────────┐
    │  Step 1: Filter │
    │  empty, short   │
    └─────────────────┘
         ↓
    ┌─────────────────┐
    │  Step 2: Rules  │
    │  time, casual   │
    │  operation      │
    └─────────────────┘
         ↓
    ┌─────────────────┐
    │  Step 3: Vector │
    │  ES similarity  │
    └─────────────────┘
         ↓
    ┌─────────────────┐
    │  Step 4: Decide │
    │  score-based    │
    └─────────────────┘
"""

import logging
import re
from typing import Dict, List, Optional, Any
from .embedding_client import EmbeddingClient
from .vector_store import VectorStore
import config

logger = logging.getLogger(__name__)


# =============================================================================
# Rule Patterns / 规则模式
# =============================================================================

# Time-related patterns / 时间相关模式
TIME_PATTERNS = [
    r"what time is it",
    r"what time is now",
    r"current time",
    r"what.*date",
    r"what day is today",
    r"when.*meeting",
    r"when.*deadline",
    r"现在几点了",
    r"今天多少号",
    r"几点开会",
]

# Casual/Greeting patterns / 闲聊/问候模式
CASUAL_PATTERNS = [
    r"^(hi|hello|hey|yo|sup|hiya)\s*$",
    r"how are you",
    r"how are u",
    r"good morning",
    r"good afternoon",
    r"good evening",
    r"thanks?( you)?",
    r"thank you",
    r"(ok|okay|alright|sounds good|got it|understood)",
    r"^(nice|great|awesome|cool)\s*$",
    r"who are you",
    r"what can you do",
    r"are you there",
    r"你好|嗨|哈喽|早上好|下午好|晚上好",
]

# Operation command patterns / 操作指令模式
OPERATION_PATTERNS = [
    r"open (the|a|this)?\s*\w+",
    r"close (the|a|this)?\s*\w+",
    r"save (the|a|this)?\s*\w+",
    r"download",
    r"upload",
    r"delete",
    r"copy",
    r"paste",
    r"click",
    r"scroll",
    r"refresh",
    r"go back",
    r"show me",
    r"restart",
    r"run",
    r"stop",
    r"check (the|a|this)?\s*\w+ (status|state)",
    r"打开|关闭|保存|下载|上传|删除|复制|粘贴|点击|刷新",
]

# Noise patterns / 噪声模式
NOISE_PATTERNS = [
    r"^(?:\s|[!?.,;:'\"-])*$",  # Only whitespace and punctuation
    r"^[a-zA-Z0-9]{1,3}$",       # 1-3 character random strings
    r"^(test|testing|123|abc|asdf|qwerty|哈哈哈哈|啦啦啦)$",
]


# =============================================================================
# Intent Classifier / 意图分类器
# =============================================================================

class IntentClassifier:
    """
    Hybrid intent classifier combining rules + vector search.
    结合规则和向量搜索的混合意图分类器。
    
    Classification Categories / 分类类别:
    - meaningful_question: Formal business/knowledge questions
    - casual_chat: Casual greetings and simple responses
    - time_weather_general: Time, weather, and general facts
    - operation_command: UI/System operations
    - noise_or_empty: Invalid or random inputs
    - unknown: Cannot determine category
    
    Attributes:
        embedding_client: Client for text-to-vector conversion
        vector_store: ES vector store for similarity search
    
    Example / 示例:
        >>> classifier = IntentClassifier()
        >>> result = classifier.classify("tell me about policy")
        >>> print(result.category)  # "meaningful_question"
    """
    
    def __init__(self, embedding_client: Optional[EmbeddingClient] = None,
                 vector_store: Optional[VectorStore] = None):
        """
        Initialize the intent classifier.
        初始化意图分类器。
        
        Args:
            embedding_client: Custom embedding client, creates default if None
            vector_store: Custom vector store, creates default if None
        """
        self.embedding_client = embedding_client or EmbeddingClient()
        self.vector_store = vector_store
        logger.info("IntentClassifier initialized")
    
    def _is_noise(self, text: str) -> bool:
        """
        Check if input is noise/invalid.
        检查输入是否是噪声/无效。
        
        Args:
            text: Input text / 输入文本
        
        Returns:
            bool: True if noise / 是否是噪声
        """
        text = text.strip()
        
        # Empty check / 空检查
        if not text:
            return True
        
        # Too short / 太短
        if len(text) < 2:
            return True
        
        # Noise patterns / 噪声模式
        for pattern in NOISE_PATTERNS:
            if re.match(pattern, text, re.IGNORECASE):
                logger.debug(f"Matched noise pattern: {pattern}")
                return True
        
        return False
    
    def _match_pattern(self, text: str, patterns: List[str]) -> bool:
        """
        Match text against a list of patterns.
        检查文本是否匹配模式列表。
        
        Args:
            text: Input text / 输入文本
            patterns: List of regex patterns / 正则表达式列表
        
        Returns:
            bool: True if any pattern matches / 任意模式匹配则返回 True
        """
        text_lower = text.lower().strip()
        for pattern in patterns:
            if re.search(pattern, text_lower, re.IGNORECASE):
                return True
        return False
    
    def _classify_by_rules(self, text: str) -> Optional[str]:
        """
        Classify by rule-based pattern matching.
        基于规则模式匹配进行分类。
        
        Args:
            text: Input text / 输入文本
        
        Returns:
            Optional[str]: Category if matched by rules / 规则匹配则返回类别
        """
        # Check for noise first / 先检查噪声
        if self._is_noise(text):
            return "noise_or_empty"
        
        # Time patterns / 时间模式
        if self._match_pattern(text, TIME_PATTERNS):
            return "time_weather_general"
        
        # Casual patterns / 闲聊模式
        if self._match_pattern(text, CASUAL_PATTERNS):
            return "casual_chat"
        
        # Operation patterns / 操作模式
        if self._match_pattern(text, OPERATION_PATTERNS):
            return "operation_command"
        
        return None  # No rule match / 无规则匹配
    
    def _classify_by_vector(self, text: str) -> Optional[Dict[str, Any]]:
        """
        Classify by vector similarity search.
        通过向量相似度搜索进行分类。
        
        Args:
            text: Input text / 输入文本
        
        Returns:
            Optional[Dict]: Result with category, score if successful / 成功则返回包含类别和分数的结果
        """
        if not self.vector_store:
            logger.warning("Vector store not available, skipping vector classification")
            return None
        
        try:
            # Get embedding / 获取向量
            embedding = self.embedding_client.embed(text)
            
            # Search in ES / 在 ES 中搜索
            results = self.vector_store.search_similar(embedding, top_k=5)
            
            if not results:
                return None
            
            # Get top result / 获取最高分结果
            top_result = results[0]
            
            return {
                "category": top_result["category"],
                "sub_category": top_result["sub_category"],
                "score": top_result["score"],
                "matched_text": top_result["text"]
            }
            
        except Exception as e:
            logger.error(f"Vector classification failed: {e}")
            return None
    
    def classify(self, text: str, use_vector: bool = True) -> Dict[str, Any]:
        """
        Classify user input intent.
        分类用户输入的意图。
        
        Args:
            text: User input text / 用户输入文本
            use_vector: Whether to use vector search / 是否使用向量搜索
        
        Returns:
            Dict: Classification result with keys:
                - input: Original input / 原始输入
                - category: Detected category / 检测到的类别
                - sub_category: Sub-category / 子分类
                - score: Confidence score (0-1) / 置信度分数
                - action: Recommended action / 推荐动作
                - method: Classification method used / 使用的分类方法
        """
        logger.info(f"Classifying text: {text[:50]}...")
        
        result = {
            "input": text,
            "category": "unknown",
            "sub_category": "",
            "score": 0.0,
            "action": config.ACTION_MAP.get("unknown", "fallback_to_llm"),
            "method": "unknown"
        }
        
        # Step 1: Rule-based classification / 步骤1: 基于规则的分类
        rule_category = self._classify_by_rules(text)
        
        if rule_category:
            result["category"] = rule_category
            result["score"] = 1.0  # Rule match = high confidence / 规则匹配 = 高置信度
            result["action"] = config.ACTION_MAP.get(rule_category, "unknown")
            result["method"] = "rule"
            logger.info(f"Rule-based classification: {rule_category}")
            return result
        
        # Step 2: Vector-based classification / 步骤2: 基于向量的分类
        if use_vector and self.vector_store:
            vector_result = self._classify_by_vector(text)
            
            if vector_result:
                result["category"] = vector_result["category"]
                result["sub_category"] = vector_result["sub_category"]
                result["score"] = vector_result["score"]
                result["method"] = "vector"
                
                # Score-based decision / 基于分数的决策
                if vector_result["score"] >= config.HIGH_CONFIDENCE_THRESHOLD:
                    result["action"] = config.ACTION_MAP.get(vector_result["category"], "unknown")
                    logger.info(f"High confidence vector match: {vector_result['category']} (score: {vector_result['score']:.2f})")
                elif vector_result["score"] >= config.MEDIUM_CONFIDENCE_THRESHOLD:
                    result["action"] = "need_llm_review"
                    logger.info(f"Medium confidence, need LLM review (score: {vector_result['score']:.2f})")
                else:
                    result["action"] = "need_llm_review"
                    result["score"] = 0.5  # Default score for unknown
                    logger.info(f"Low confidence, need LLM review (score: {vector_result['score']:.2f})")
                
                return result
        
        # Step 3: Default to unknown / 步骤3: 默认未知
        result["action"] = "fallback_to_llm"
        logger.info("Classification result: unknown")
        return result
    
    def classify_batch(self, texts: List[str]) -> List[Dict[str, Any]]:
        """
        Classify multiple texts in batch.
        批量分类多个文本。
        
        Args:
            texts: List of input texts / 输入文本列表
        
        Returns:
            List[Dict]: List of classification results / 分类结果列表
        """
        return [self.classify(text) for text in texts]


# =============================================================================
# Convenience Functions / 便捷函数
# =============================================================================

def classify_intent(text: str) -> Dict[str, Any]:
    """
    Convenience function to classify a single text.
    便捷函数：对单个文本进行分类。
    
    Args:
        text: Input text / 输入文本
    
    Returns:
        Dict: Classification result / 分类结果
    """
    classifier = IntentClassifier()
    return classifier.classify(text)


if __name__ == "__main__":
    # Demo usage / 示例用法
    logging.basicConfig(level=logging.INFO)
    
    classifier = IntentClassifier()
    
    test_texts = [
        "tell me about the policy detail",
        "hi, how are you today",
        "what time is it now",
        "open the file",
        "test",
        "",
    ]
    
    print("\n" + "=" * 60)
    print("Intent Classification Demo")
    print("=" * 60)
    
    for text in test_texts:
        result = classifier.classify(text)
        print(f"\nInput: '{text}'")
        print(f"  Category: {result['category']}")
        print(f"  Score: {result['score']:.2f}")
        print(f"  Action: {result['action']}")
        print(f"  Method: {result['method']}")