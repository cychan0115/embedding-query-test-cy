# Intent Classification Demo - 意图分类演示

[中文说明](#中文) | [English](#english)

---

## English

### Project Overview

This is a demo project for **intent classification** using embedding + Elasticsearch vector search. It determines whether a user's query is a meaningful question that should enter the RAG/Knowledge Base flow, or a casual/operactional query that should be handled differently.

### Architecture

```
User Input
    ↓
┌─────────────────────────────────────┐
│  Step 1: Pre-filter                 │
│  - Empty check                       │
│  - Length check (< 4 chars = noise) │
│  - Noise pattern check               │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│  Step 2: Rule-based Pattern Match    │
│  - Time patterns (what time, when)  │
│  - Casual patterns (hi, hello, thanks)│
│  - Operation patterns (open, click)  │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│  Step 3: Vector Similarity Search    │
│  - Embed user query                  │
│  - Search in ES seed vector index    │
│  - Get category + similarity score  │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│  Step 4: Score-based Decision       │
│  >= 0.82 → Use ES category           │
│  0.70-0.82 → LLM review needed      │
│  < 0.70 → Unknown                   │
└─────────────────────────────────────┘
```

### Categories

| Category | Description | Examples |
|----------|-------------|----------|
| `meaningful_question` | Formal business/knowledge questions | "tell me about policy detail", "explain section 4.2" |
| `casual_chat` | Casual greetings and闲聊 | "hi", "how are you", "thanks" |
| `time_weather_general` | Time/weather queries | "what time is it", "how is weather today" |
| `operation_command` | UI/System operations | "open file", "click submit", "refresh" |
| `noise_or_empty` | Invalid/random input | "", "test", "123", "???" |

### Installation

```bash
pip install -r requirements.txt
```

### Configuration

Edit `config.py` to set your ES host and embedding API:

```python
ES_HOST = "http://localhost:9200"
ES_INDEX = "intent_seed_vectors"
EMBEDDING_API = "http://your-embedding-service/v1/embed"
```

### Usage

```python
from src.intent_classifier import IntentClassifier

classifier = IntentClassifier()
result = classifier.classify("tell me about 4.2 policy detail")

print(result)
# {
#     "input": "tell me about 4.2 policy detail",
#     "category": "meaningful_question",
#     "sub_category": "policy_detail",
#     "score": 0.87,
#     "action": "route_to_rag"
# }
```

### CLI Demo

```bash
python main.py
```

### ES Index Mapping

```json
{
  "mappings": {
    "properties": {
      "text": {"type": "text"},
      "category": {"type": "keyword"},
      "sub_category": {"type": "keyword"},
      "embedding": {
        "type": "dense_vector",
        "dims": 1536,
        "index": true,
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
```

---

## 中文

### 项目概述

这是一个**意图分类**演示项目，使用 embedding + Elasticsearch 向量搜索来判断用户输入是有意义的业务/知识问题，还是闲聊/操作类查询。

### 系统架构

```
用户输入
    ↓
┌─────────────────────────────────────┐
│  步骤1: 预过滤                       │
│  - 空文本检查                         │
│  - 长度检查 (< 4字符 = 噪声)          │
│  - 噪声模式检查                       │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│  步骤2: 规则模式匹配                  │
│  - 时间模式 (what time, 几点)        │
│  - 闲聊模式 (hi, hello, 你好)        │
│  - 操作模式 (open, click, 打开)      │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│  步骤3: 向量相似度搜索                │
│  - 对用户输入进行 embedding           │
│  - 在 ES 种子向量索引中搜索           │
│  - 获取分类 + 相似度分数              │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│  步骤4: 基于分数的决策                │
│  >= 0.82 → 使用 ES 分类              │
│  0.70-0.82 → 需要 LLM 复审           │
│  < 0.70 → 未知类别                   │
└─────────────────────────────────────┘
```

### 分类类别

| 类别 | 说明 | 示例 |
|------|------|------|
| `meaningful_question` | 正式的业务/知识问题 | "tell me about policy detail", "解释4.2条款" |
| `casual_chat` | 闲聊和问候 | "hi", "你好", "谢谢" |
| `time_weather_general` | 时间/天气查询 | "现在几点", "今天天气如何" |
| `operation_command` | UI/系统操作指令 | "打开文件", "点击提交", "刷新" |
| `noise_or_empty` | 无效/随机输入 | "", "test", "123", "???" |

### 安装

```bash
pip install -r requirements.txt
```

### 配置

编辑 `config.py` 设置您的 ES 主机和 embedding API：

```python
ES_HOST = "http://localhost:9200"
ES_INDEX = "intent_seed_vectors"
EMBEDDING_API = "http://your-embedding-service/v1/embed"
```

### 使用方法

```python
from src.intent_classifier import IntentClassifier

classifier = IntentClassifier()
result = classifier.classify("tell me about 4.2 policy detail")

print(result)
# {
#     "input": "tell me about 4.2 policy detail",
#     "category": "meaningful_question",
#     "sub_category": "policy_detail",
#     "score": 0.87,
#     "action": "route_to_rag"
# }
```

### CLI 演示

```bash
python main.py
```

### ES 索引 Mapping

```json
{
  "mappings": {
    "properties": {
      "text": {"type": "text"},
      "category": {"type": "keyword"},
      "sub_category": {"type": "keyword"},
      "embedding": {
        "type": "dense_vector",
        "dims": 1536,
        "index": true,
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
```

---

## File Structure

```
embedding-query-test-cy/
├── README.md           # This file
├── requirements.txt    # Dependencies
├── config.py           # Configuration
├── seed_data.py        # Seed examples for each category
├── src/
│   ├── __init__.py
│   ├── embedding_client.py   # Embedding API client
│   ├── vector_store.py       # ES vector operations
│   └── intent_classifier.py  # Main classifier logic
├── tests/
│   └── test_classifier.py    # Unit tests
└── main.py             # CLI demo
```

## License

MIT