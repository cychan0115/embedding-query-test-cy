# -*- coding: utf-8 -*-
"""
Unit tests for IntentClassifier.
意图分类器单元测试

Tests cover:
1. Noise detection
2. Rule-based classification
3. Vector-based classification (mocked)
4. Batch classification

Author: Intent Classification Demo
"""

import unittest
import sys
import os

# Add parent directory to path / 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.intent_classifier import IntentClassifier, classify_intent


class TestNoiseDetection(unittest.TestCase):
    """Tests for noise detection / 噪声检测测试"""
    
    def setUp(self):
        self.classifier = IntentClassifier()
    
    def test_empty_string(self):
        """Test empty string is detected as noise / 测试空字符串检测为噪声"""
        self.assertEqual(self.classifier.classify("")["category"], "noise_or_empty")
    
    def test_whitespace_only(self):
        """Test whitespace-only is detected as noise / 测试仅空白字符检测为噪声"""
        self.assertEqual(self.classifier.classify("   ")["category"], "noise_or_empty")
    
    def test_very_short(self):
        """Test very short strings are detected as noise / 测试超短字符串检测为噪声"""
        self.assertEqual(self.classifier.classify("a")["category"], "noise_or_empty")
        self.assertEqual(self.classifier.classify("ab")["category"], "noise_or_empty")
    
    def test_random_characters(self):
        """Test random characters are detected as noise / 测试随机字符检测为噪声"""
        self.assertEqual(self.classifier.classify("asdf")["category"], "noise_or_empty")
        self.assertEqual(self.classifier.classify("123")["category"], "noise_or_empty")
        self.assertEqual(self.classifier.classify("!!!")["category"], "noise_or_empty")


class TestRuleBasedClassification(unittest.TestCase):
    """Tests for rule-based classification / 基于规则的分类测试"""
    
    def setUp(self):
        self.classifier = IntentClassifier()
    
    def test_casual_chat(self):
        """Test casual chat detection / 测试闲聊检测"""
        casual_inputs = [
            "hi",
            "hello",
            "how are you",
            "thanks",
            "ok",
            "nice",
        ]
        for text in casual_inputs:
            result = self.classifier.classify(text)
            self.assertEqual(result["category"], "casual_chat", f"Failed for: {text}")
    
    def test_time_queries(self):
        """Test time query detection / 测试时间查询检测"""
        time_inputs = [
            "what time is it now",
            "what is today's date",
            "what day is today",
            "when is the meeting",
        ]
        for text in time_inputs:
            result = self.classifier.classify(text)
            self.assertEqual(result["category"], "time_weather_general", f"Failed for: {text}")
    
    def test_operation_commands(self):
        """Test operation command detection / 测试操作指令检测"""
        operation_inputs = [
            "open the file",
            "click submit",
            "download the report",
            "refresh the page",
            "restart the service",
        ]
        for text in operation_inputs:
            result = self.classifier.classify(text)
            self.assertEqual(result["category"], "operation_command", f"Failed for: {text}")
    
    def test_meaningful_questions_not_matched_by_rules(self):
        """Test meaningful questions fall through to vector search / 测试正式问题会落到向量搜索"""
        # These should NOT be matched by rules (they need vector search)
        question = "tell me about the policy detail"
        result = self.classifier.classify(question, use_vector=False)
        # Without vector search, should return unknown
        self.assertEqual(result["category"], "unknown")


class TestConvenienceFunction(unittest.TestCase):
    """Tests for convenience function / 便捷函数测试"""
    
    def test_classify_intent(self):
        """Test the convenience function / 测试便捷函数"""
        result = classify_intent("hi")
        self.assertIn("category", result)
        self.assertIn("score", result)
        self.assertIn("action", result)


class TestClassificationResult(unittest.TestCase):
    """Tests for classification result format / 分类结果格式测试"""
    
    def setUp(self):
        self.classifier = IntentClassifier()
    
    def test_result_has_required_fields(self):
        """Test result contains all required fields / 测试结果包含所有必需字段"""
        result = self.classifier.classify("hi")
        
        required_fields = ["input", "category", "score", "action", "method"]
        for field in required_fields:
            self.assertIn(field, result, f"Missing field: {field}")
    
    def test_score_range(self):
        """Test score is in valid range / 测试分数在有效范围内"""
        result = self.classifier.classify("hi")
        self.assertGreaterEqual(result["score"], 0.0)
        self.assertLessEqual(result["score"], 1.0)
    
    def test_action_mapping(self):
        """Test action is correctly mapped / 测试动作正确映射"""
        result = self.classifier.classify("hi")
        self.assertIn(result["action"], ["small_talk_reply", "route_to_rag", 
                                          "route_to_agent", "ignore_or_reject",
                                          "fallback_to_llm", "unknown"])


class TestBatchClassification(unittest.TestCase):
    """Tests for batch classification / 批量分类测试"""
    
    def setUp(self):
        self.classifier = IntentClassifier()
    
    def test_batch_classify(self):
        """Test batch classification / 测试批量分类"""
        texts = ["hi", "what time is it", "open the file"]
        results = self.classifier.classify_batch(texts)
        
        self.assertEqual(len(results), len(texts))
        for result in results:
            self.assertIn("category", result)


if __name__ == "__main__":
    # Run tests with verbose output / 运行测试并输出详细信息
    unittest.main(verbosity=2)