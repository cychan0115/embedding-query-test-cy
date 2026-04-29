"""
Test cases for intent classifier / 意图分类器的测试用例

Bilingual docstrings: Chinese first, English second
双语言文档字符串：中文优先，英文第二
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import numpy as np

from config import Config
from intent_classifier import IntentClassifier


class TestConfig:
    """Test configuration validation / 测试配置验证"""

    def test_default_config(self):
        """Test default configuration can be created / 测试可以创建默认配置"""
        config = Config()
        assert config.es_host == "localhost"
        assert config.es_port == 9200
        assert config.similarity_threshold_high == 0.82
        assert config.similarity_threshold_low == 0.70

    def test_config_validation_invalid_port(self):
        """Test config rejects invalid port / 测试配置拒绝无效端口"""
        with pytest.raises(ValueError, match="Invalid ES port"):
            Config(es_port=70000)

    def test_config_validation_invalid_thresholds(self):
        """Test config rejects invalid thresholds / 测试配置拒绝无效阈值"""
        with pytest.raises(ValueError):
            Config(similarity_threshold_high=0.5, similarity_threshold_low=0.8)

    def test_config_validation_threshold_order(self):
        """Test high threshold must be greater than low / 测试高阈值必须大于低阈值"""
        with pytest.raises(ValueError, match="must be greater"):
            Config(similarity_threshold_high=0.6, similarity_threshold_low=0.8)


class TestPreFilter:
    """Test pre-filtering logic / 测试预过滤逻辑"""

    def setup_method(self):
        """Setup test fixtures / 设置测试fixtures"""
        self.config = Config()
        self.mock_embedding_client = Mock()
        self.mock_vector_store = Mock()

    @patch("intent_classifier.get_embedding_client")
    @patch("intent_classifier.get_vector_store")
    def test_empty_text_filtered(self, mock_vs, mock_ec):
        """Test empty text is filtered as noise / 测试空文本被过滤为噪声"""
        mock_ec.return_value = self.mock_embedding_client
        mock_vs.return_value = self.mock_vector_store

        classifier = IntentClassifier(self.config)

        result = classifier.classify("")
        assert result["category"] == "noise_or_empty"
        assert result["reason"] == "empty_input"

    @patch("intent_classifier.get_embedding_client")
    @patch("intent_classifier.get_vector_store")
    def test_whitespace_only_filtered(self, mock_vs, mock_ec):
        """Test whitespace-only text is filtered / 测试仅空白文本被过滤"""
        mock_ec.return_value = self.mock_embedding_client
        mock_vs.return_value = self.mock_vector_store

        classifier = IntentClassifier(self.config)

        result = classifier.classify("   ")
        assert result["category"] == "noise_or_empty"
        assert result["reason"] == "empty_input"

    @patch("intent_classifier.get_embedding_client")
    @patch("intent_classifier.get_vector_store")
    def test_too_short_filtered(self, mock_vs, mock_ec):
        """Test too short text is filtered / 测试太短的文本被过滤"""
        mock_ec.return_value = self.mock_embedding_client
        mock_vs.return_value = self.mock_vector_store

        classifier = IntentClassifier(self.config)

        result = classifier.classify("a")
        assert result["category"] == "noise_or_empty"
        assert result["reason"] == "too_short"

    @patch("intent_classifier.get_embedding_client")
    @patch("intent_classifier.get_vector_store")
    def test_noise_pattern_numbers(self, mock_vs, mock_ec):
        """Test numbers-only text matches noise pattern / 测试仅数字文本匹配噪声模式"""
        mock_ec.return_value = self.mock_embedding_client
        mock_vs.return_value = self.mock_vector_store

        classifier = IntentClassifier(self.config)

        result = classifier.classify("123456")
        assert result["category"] == "noise_or_empty"
        assert result["reason"] == "noise_pattern"

    @patch("intent_classifier.get_embedding_client")
    @patch("intent_classifier.get_vector_store")
    def test_noise_pattern_random_letters(self, mock_vs, mock_ec):
        """Test random letters match noise pattern / 测试随机字母匹配噪声模式"""
        mock_ec.return_value = self.mock_embedding_client
        mock_vs.return_value = self.mock_vector_store

        classifier = IntentClassifier(self.config)

        result = classifier.classify("asdfghjkl")
        assert result["category"] == "noise_or_empty"
        assert result["reason"] == "noise_pattern"


class TestKeywordClassification:
    """Test keyword-based classification / 测试基于关键词的分类"""

    def setup_method(self):
        """Setup test fixtures / 设置测试fixtures"""
        self.config = Config()
        self.mock_vector_store = Mock()

    @patch("intent_classifier.get_embedding_client")
    @patch("intent_classifier.get_vector_store")
    def test_meaningful_question_keywords(self, mock_vs, mock_ec):
        """Test meaningful question keywords detected / 测试检测到有意义问题关键词"""
        mock_embedding_client = Mock()
        mock_embedding_client.encode.return_value = np.array([0.1] * 384)
        mock_ec.return_value = mock_embedding_client
        mock_vs.return_value = self.mock_vector_store
        self.mock_vector_store.search.return_value = []

        classifier = IntentClassifier(self.config)

        # Question mark should trigger meaningful_question / 问号应触发 meaningful_question
        result = classifier.classify("How do I reset my password?")
        assert result["category"] == "meaningful_question"

    @patch("intent_classifier.get_embedding_client")
    @patch("intent_classifier.get_vector_store")
    def test_casual_chat_keywords(self, mock_vs, mock_ec):
        """Test casual chat keywords detected / 测试检测到闲聊关键词"""
        mock_embedding_client = Mock()
        mock_embedding_client.encode.return_value = np.array([0.1] * 384)
        mock_ec.return_value = mock_embedding_client
        mock_vs.return_value = self.mock_vector_store
        self.mock_vector_store.search.return_value = []

        classifier = IntentClassifier(self.config)

        result = classifier.classify("Hey there!")
        assert result["category"] == "casual_chat"

    @patch("intent_classifier.get_embedding_client")
    @patch("intent_classifier.get_vector_store")
    def test_time_weather_keywords(self, mock_vs, mock_ec):
        """Test time/weather keywords detected / 测试检测到时间/天气关键词"""
        mock_embedding_client = Mock()
        mock_embedding_client.encode.return_value = np.array([0.1] * 384)
        mock_ec.return_value = mock_embedding_client
        mock_vs.return_value = self.mock_vector_store
        self.mock_vector_store.search.return_value = []

        classifier = IntentClassifier(self.config)

        result = classifier.classify("What's the weather like today?")
        assert result["category"] == "time_weather_general"

    @patch("intent_classifier.get_embedding_client")
    @patch("intent_classifier.get_vector_store")
    def test_operation_command_keywords(self, mock_vs, mock_ec):
        """Test operation command keywords detected / 测试检测到操作指令关键词"""
        mock_embedding_client = Mock()
        mock_embedding_client.encode.return_value = np.array([0.1] * 384)
        mock_ec.return_value = mock_embedding_client
        mock_vs.return_value = self.mock_vector_store
        self.mock_vector_store.search.return_value = []

        classifier = IntentClassifier(self.config)

        result = classifier.classify("Book a table for two")
        assert result["category"] == "operation_command"


class TestVectorSearch:
    """Test vector similarity search / 测试向量相似度搜索"""

    def setup_method(self):
        """Setup test fixtures / 设置测试fixtures"""
        self.config = Config()

    @patch("intent_classifier.get_embedding_client")
    @patch("intent_classifier.get_vector_store")
    def test_high_confidence_uses_es_category(self, mock_vs, mock_ec):
        """Test high confidence score (>0.82) uses ES category / 测试高置信度(>0.82)使用ES类别"""
        mock_embedding_client = Mock()
        mock_embedding_client.encode.return_value = np.array([0.1] * 384)
        mock_ec.return_value = mock_embedding_client

        mock_vector_store = Mock()
        mock_vector_store.search.return_value = [
            {"text": "What's the weather?", "category": "time_weather_general", "score": 0.90}
        ]
        mock_vs.return_value = mock_vector_store

        classifier = IntentClassifier(self.config)
        result = classifier.classify("Is it sunny outside?")

        assert result["category"] == "time_weather_general"
        assert result["confidence"] == 0.90
        assert result["method"] == "vector"
        assert result["llm_review"] is False

    @patch("intent_classifier.get_embedding_client")
    @patch("intent_classifier.get_vector_store")
    def test_medium_confidence_flags_llm_review(self, mock_vs, mock_ec):
        """Test medium confidence (0.70-0.82) flags for LLM review / 测试中等置信度(0.70-0.82)标记为需LLM审核"""
        mock_embedding_client = Mock()
        mock_embedding_client.encode.return_value = np.array([0.1] * 384)
        mock_ec.return_value = mock_embedding_client

        mock_vector_store = Mock()
        mock_vector_store.search.return_value = [
            {"text": "Something", "category": "unknown", "score": 0.75}
        ]
        mock_vs.return_value = mock_vector_store

        classifier = IntentClassifier(self.config)
        result = classifier.classify("Some ambiguous text")

        assert result["category"] == "llm_review"
        assert result["llm_review"] is True

    @patch("intent_classifier.get_embedding_client")
    @patch("intent_classifier.get_vector_store")
    def test_low_confidence_returns_unknown(self, mock_vs, mock_ec):
        """Test low confidence (<0.70) returns unknown / 测试低置信度(<0.70)返回未知"""
        mock_embedding_client = Mock()
        mock_embedding_client.encode.return_value = np.array([0.1] * 384)
        mock_ec.return_value = mock_embedding_client

        mock_vector_store = Mock()
        mock_vector_store.search.return_value = [
            {"text": "Something else", "category": "unknown", "score": 0.50}
        ]
        mock_vs.return_value = mock_vector_store

        classifier = IntentClassifier(self.config)
        result = classifier.classify("Random gibberish text xyz")

        assert result["category"] == "unknown"
        assert result["llm_review"] is True


class TestBatchClassification:
    """Test batch classification / 测试批量分类"""

    def setup_method(self):
        """Setup test fixtures / 设置测试fixtures"""
        self.config = Config()

    @patch("intent_classifier.get_embedding_client")
    @patch("intent_classifier.get_vector_store")
    def test_batch_classify(self, mock_vs, mock_ec):
        """Test batch classification works / 测试批量分类工作正常"""
        mock_embedding_client = Mock()
        mock_embedding_client.encode.return_value = np.array([[0.1] * 384])
        mock_ec.return_value = mock_embedding_client

        mock_vector_store = Mock()
        mock_vector_store.search.return_value = []
        mock_vs.return_value = mock_vector_store

        classifier = IntentClassifier(self.config)

        texts = ["Hello!", "How are you?", "What's the time?"]
        results = classifier.batch_classify(texts)

        assert len(results) == 3
        assert all("category" in r for r in results)


class TestCategoryInfo:
    """Test category information retrieval / 测试类别信息获取"""

    def setup_method(self):
        """Setup test fixtures / 设置测试fixtures"""
        self.config = Config()

    @patch("intent_classifier.get_embedding_client")
    @patch("intent_classifier.get_vector_store")
    def test_get_category_info(self, mock_vs, mock_ec):
        """Test category info retrieval / 测试类别信息获取"""
        mock_ec.return_value = Mock()
        mock_vs.return_value = Mock()

        classifier = IntentClassifier(self.config)

        info = classifier.get_category_info("meaningful_question")

        assert info["name"] == "meaningful_question"
        assert "display_name" in info
        assert "description" in info
        assert "正式问题" in info["display_name"]


class TestThresholdApplication:
    """Test threshold application logic / 测试阈值应用逻辑"""

    def setup_method(self):
        """Setup test fixtures / 设置测试fixtures"""
        self.config = Config()

    @patch("intent_classifier.get_embedding_client")
    @patch("intent_classifier.get_vector_store")
    def test_threshold_boundary_high(self, mock_vs, mock_ec):
        """Test boundary at 0.82 threshold / 测试 0.82 阈值的边界"""
        mock_embedding_client = Mock()
        mock_embedding_client.encode.return_value = np.array([0.1] * 384)
        mock_ec.return_value = mock_embedding_client

        mock_vector_store = Mock()
        mock_vector_store.search.return_value = [
            {"text": "test", "category": "casual_chat", "score": 0.82}
        ]
        mock_vs.return_value = mock_vector_store

        classifier = IntentClassifier(self.config)
        result = classifier.classify("test")

        assert result["category"] == "casual_chat"
        assert result["llm_review"] is False

    @patch("intent_classifier.get_embedding_client")
    @patch("intent_classifier.get_vector_store")
    def test_threshold_boundary_low(self, mock_vs, mock_ec):
        """Test boundary at 0.70 threshold / 测试 0.70 阈值的边界"""
        mock_embedding_client = Mock()
        mock_embedding_client.encode.return_value = np.array([0.1] * 384)
        mock_ec.return_value = mock_embedding_client

        mock_vector_store = Mock()
        mock_vector_store.search.return_value = [
            {"text": "test", "category": "unknown", "score": 0.69}
        ]
        mock_vs.return_value = mock_vector_store

        classifier = IntentClassifier(self.config)
        result = classifier.classify("test")

        assert result["category"] == "unknown"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])