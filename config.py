# -*- coding: utf-8 -*-
"""
Configuration file for Intent Classification Demo.
意图分类演示项目的配置文件。

Configuration / 配置
- ES_HOST: Elasticsearch host URL / ES 主机地址
- ES_INDEX: Index name for seed vectors / 种子向量索引名称
- EMBEDDING_API: Embedding service API endpoint / Embedding 服务 API 端点
- EMBEDDING_DIM: Dimension of embedding vectors / 向量维度
"""

import os
from pathlib import Path

# Base directory / 基础目录
BASE_DIR = Path(__file__).parent

# Elasticsearch configuration / Elasticsearch 配置
ES_HOST = os.getenv("ES_HOST", "http://localhost:9200")
ES_INDEX = os.getenv("ES_INDEX", "intent_seed_vectors")

# Embedding service configuration / Embedding 服务配置
EMBEDDING_API = os.getenv("EMBEDDING_API", "http://localhost:8000/v1/embed")
EMBEDDING_DIM = int(os.getenv("EMBEDDING_DIM", "1536"))

# Classifier thresholds / 分类器阈值
# High confidence: use ES result directly / 高置信度：直接使用 ES 结果
HIGH_CONFIDENCE_THRESHOLD = 0.82

# Medium confidence: need LLM review / 中等置信度：需要 LLM 复审
MEDIUM_CONFIDENCE_THRESHOLD = 0.70

# Action mapping / 动作映射
ACTION_MAP = {
    "meaningful_question": "route_to_rag",
    "casual_chat": "small_talk_reply",
    "time_weather_general": "tool_or_direct_reply",
    "operation_command": "route_to_agent",
    "noise_or_empty": "ignore_or_reject",
    "unknown": "fallback_to_llm"
}

# Logging configuration / 日志配置
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"