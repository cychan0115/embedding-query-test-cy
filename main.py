# -*- coding: utf-8 -*-
"""
Main CLI Demo - 命令行演示
意图分类系统演示

This script demonstrates the intent classification system.
本脚本演示意图分类系统的使用方法。

Usage / 使用方法:
    python main.py

Author: Intent Classification Demo
"""

import sys
import logging
from src.embedding_client import EmbeddingClient
from src.vector_store import VectorStore
from src.intent_classifier import IntentClassifier
import config

# Configure logging / 配置日志
logging.basicConfig(
    level=logging.INFO,
    format=config.LOG_FORMAT
)
logger = logging.getLogger(__name__)


def demo_without_es():
    """
    Demo without Elasticsearch - using rule-based classification only.
    无 ES 演示 - 仅使用基于规则的分类。
    """
    print("\n" + "=" * 60)
    print("Intent Classification Demo (Rule-based Only)")
    print("意图分类演示 (仅基于规则)")
    print("=" * 60)
    
    classifier = IntentClassifier()
    
    test_cases = [
        # Meaningful questions / 正式问题
        ("tell me about the policy detail", "meaningful_question"),
        ("explain section 4.2 of the policy", "meaningful_question"),
        ("what are the requirements for this process", "meaningful_question"),
        ("how should I handle this exception case", "meaningful_question"),
        ("what is the refund policy", "meaningful_question"),
        
        # Casual chat / 闲聊
        ("hi", "casual_chat"),
        ("hello, how are you today", "casual_chat"),
        ("thanks for your help", "casual_chat"),
        ("ok, sounds good", "casual_chat"),
        ("who are you", "casual_chat"),
        
        # Time/Weather / 时间天气
        ("what time is it now", "time_weather_general"),
        ("what is today's date", "time_weather_general"),
        ("how is the weather today", "time_weather_general"),
        ("when is the meeting", "time_weather_general"),
        
        # Operation commands / 操作指令
        ("open the file", "operation_command"),
        ("click the submit button", "operation_command"),
        ("download the report", "operation_command"),
        ("refresh the page", "operation_command"),
        ("restart the service", "operation_command"),
        
        # Noise / 噪声
        ("test", "noise_or_empty"),
        ("123", "noise_or_empty"),
        ("!!!", "noise_or_empty"),
        ("", "noise_or_empty"),
        ("asdfasdf", "noise_or_empty"),
    ]
    
    print("\nRunning classification tests...\n")
    
    correct = 0
    total = len(test_cases)
    
    for text, expected in test_cases:
        result = classifier.classify(text, use_vector=False)
        status = "✓" if result["category"] == expected else "✗"
        
        if result["category"] == expected:
            correct += 1
        
        print(f"{status} Input: '{text[:40]:40}'")
        print(f"   Expected: {expected:25} Got: {result['category']:25} Score: {result['score']:.2f}")
        print()
    
    accuracy = correct / total * 100
    print("-" * 60)
    print(f"Accuracy: {correct}/{total} ({accuracy:.1f}%)")
    print("-" * 60)
    
    return accuracy


def demo_with_es():
    """
    Demo with Elasticsearch - full hybrid classification.
    带 ES 的演示 - 完整混合分类。
    """
    print("\n" + "=" * 60)
    print("Intent Classification Demo (With Elasticsearch)")
    print("意图分类演示 (带 Elasticsearch)")
    print("=" * 60)
    
    try:
        # Initialize components / 初始化组件
        embedding_client = EmbeddingClient()
        vector_store = VectorStore()
        
        classifier = IntentClassifier(
            embedding_client=embedding_client,
            vector_store=vector_store
        )
        
        # Test single input / 测试单个输入
        test_text = "tell me about the policy detail"
        print(f"\nClassifying: '{test_text}'")
        
        result = classifier.classify(test_text)
        
        print(f"  Category: {result['category']}")
        print(f"  Sub-category: {result['sub_category']}")
        print(f"  Score: {result['score']:.4f}")
        print(f"  Action: {result['action']}")
        print(f"  Method: {result['method']}")
        
        return True
        
    except Exception as e:
        logger.error(f"ES demo failed: {e}")
        print(f"\nError: Cannot connect to Elasticsearch at {config.ES_HOST}")
        print("Please ensure ES is running, or use the rule-based demo.")
        return False


def interactive_mode():
    """
    Interactive mode - let user type inputs.
    交互模式 - 让用户输入文本。
    """
    print("\n" + "=" * 60)
    print("Interactive Mode - Type 'quit' to exit")
    print("交互模式 - 输入 'quit' 退出")
    print("=" * 60)
    
    classifier = IntentClassifier()
    
    while True:
        try:
            text = input("\nEnter text to classify: ").strip()
            
            if text.lower() == "quit":
                print("Goodbye!")
                break
            
            if not text:
                print("Please enter some text.")
                continue
            
            result = classifier.classify(text, use_vector=False)
            
            print(f"\n  Category: {result['category']}")
            print(f"  Score: {result['score']:.2f}")
            print(f"  Action: {result['action']}")
            print(f"  Method: {result['method']}")
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")


def main():
    """
    Main entry point.
    主入口。
    """
    print("\n" + "=" * 60)
    print("Intent Classification System Demo")
    print("意图分类系统演示")
    print("=" * 60)
    
    # Check command line args / 检查命令行参数
    if len(sys.argv) > 1:
        if sys.argv[1] == "--interactive":
            interactive_mode()
        elif sys.argv[1] == "--es":
            demo_with_es()
        else:
            print(f"Unknown option: {sys.argv[1]}")
            print("Usage: python main.py [--interactive|--es]")
    else:
        # Default: run rule-based demo / 默认：运行基于规则的演示
        demo_without_es()
        
        # Ask if user wants ES demo / 询问是否需要 ES 演示
        print("\nNote: This demo uses rule-based classification only.")
        print("To use vector search with ES, ensure Elasticsearch is running.")
        print("\nOptions:")
        print("  --interactive : Interactive mode")
        print("  --es          : Test with Elasticsearch")


if __name__ == "__main__":
    main()