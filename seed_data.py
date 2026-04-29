# -*- coding: utf-8 -*-
"""
Seed data for intent classification.
意图分类的种子数据 - 包含各类别的代表性示例句子。

This data is used to:
1. Generate embeddings for each seed example
2. Store in ES as reference vectors
3. Compare user input against these seeds for classification

此数据用于：
1. 为每个种子示例生成 embedding
2. 存储到 ES 作为参考向量
3. 将用户输入与这些种子对比进行分类
"""

# =============================================================================
# Category: meaningful_question (正式问题)
# Description: Business/knowledge questions that should enter RAG/Knowledge flow
# 描述: 应进入 RAG/知识库流程的业务/知识问题
# =============================================================================
MEANINGFUL_QUESTION_EXAMPLES = [
    # Policy related / 政策相关
    "tell me about the policy detail",
    "explain section 4.2 of the policy",
    "what are the requirements for this process",
    "what is the refund policy for returns",
    "how does the compliance policy work",
    "can you explain the travel expense policy",
    "what are the procurement guidelines",
    "detail the data protection regulation",
    
    # Procedure related / 流程相关
    "what is the correct procedure for approval",
    "how should I handle this exception case",
    "what is the workflow for vendor registration",
    "explain the onboarding process",
    "what are the steps for expense reimbursement",
    "how do I submit a leave request",
    "walk me through the contract signing process",
    
    # Document/Knowledge related / 文档/知识相关
    "what does this rule mean",
    "give me the details of the regulation",
    "summarize the key points of this document",
    "what is the difference between these two policies",
    "how do I apply this policy in practice",
    "what should I do if this exception happens",
    "which department is responsible for this process",
    "what documents are required for this application",
    
    # Analysis/Understanding related / 分析/理解相关
    "can you analyze this issue",
    "can you help me understand this document",
    "what is the meaning of this clause",
    "how is this calculation performed",
    "what are the compliance requirements",
    "what are the eligibility conditions",
    "explain the eligibility criteria for this benefit",
    "what are the key terms in this agreement",
    
    # Business inquiry / 业务咨询
    "what is the status of my leave request",
    "how much vacation time do I have left",
    "what is the deadline for this project",
    "who is the approver for this expense",
]

# =============================================================================
# Category: casual_chat (闲聊)
# Description: Casual greetings and simple responses that don't need knowledge base
# 描述: 闲聊和问候，不需要知识库处理
# =============================================================================
CASUAL_CHAT_EXAMPLES = [
    # Greetings / 问候
    "hello",
    "hi",
    "hey",
    "how are you",
    "how are u today",
    "good morning",
    "good afternoon",
    "good evening",
    "what is up",
    "how is it going",
    "nice to meet you",
    
    # Thanks/Confirmation / 感谢/确认
    "thanks",
    "thank you",
    "thank you so much",
    "appreciate your help",
    "ok",
    "okay",
    "alright",
    "sounds good",
    "got it",
    "understood",
    "I see",
    
    # Simple opinions / 简单表态
    "nice",
    "great",
    "awesome",
    "cool",
    "interesting",
    "makes sense",
    "I agree",
    "of course",
    "sure",
    "yes please",
    
    # Self-introduction / 自我介绍
    "who are you",
    "what can you do",
    "are you there",
    "can you hear me",
    "is anyone there",
    "help me",
]

# =============================================================================
# Category: time_weather_general (时间天气)
# Description: Time, weather, and general factual queries
# 描述: 时间、天气和一般事实查询
# =============================================================================
TIME_WEATHER_EXAMPLES = [
    # Time queries / 时间查询
    "what time is it now",
    "what time is now",
    "what is the current time",
    "what is today's date",
    "what day is today",
    "what is the date today",
    "when is the meeting",
    "when is the deadline",
    "what hour is it",
    "what date is it tomorrow",
    
    # Weather queries / 天气查询
    "how is the weather today",
    "what is the weather like",
    "is it raining now",
    "what is the temperature today",
    "will it rain tomorrow",
    "is it sunny outside",
    "do I need an umbrella",
    "how hot is it today",
    
    # General factual / 一般事实
    "what is 2+2",
    "who is the president",
    "what is the capital of china",
    "how many days in a year",
    "what year is it",
]

# =============================================================================
# Category: operation_command (操作指令)
# Description: UI/System operations that should be handled by Agent
# 描述: 应由 Agent 处理的 UI/系统操作
# =============================================================================
OPERATION_COMMAND_EXAMPLES = [
    # File operations / 文件操作
    "open the file",
    "close the file",
    "save this file",
    "download the report",
    "upload this document",
    "delete this item",
    "copy this text",
    "paste the content",
    "rename this file",
    "move this to trash",
    
    # UI operations / UI 操作
    "click the submit button",
    "click the next button",
    "scroll down",
    "scroll up",
    "refresh the page",
    "go back",
    "go to home page",
    "show me the dashboard",
    "open the menu",
    "minimize this window",
    
    # System operations / 系统操作
    "restart the service",
    "check the server status",
    "run this script",
    "stop the process",
    "start the backup",
    "sync the data",
    "clear the cache",
    "reboot the system",
    
    # Application operations / 应用操作
    "send this email",
    "create a new document",
    "print this page",
    "share this file",
    "export to pdf",
    "import the data",
    "merge these files",
]

# =============================================================================
# Category: noise_or_empty (噪声/无效)
# Description: Invalid, random, or empty inputs
# 描述: 无效、随机或空输入
# =============================================================================
NOISE_EXAMPLES = [
    # Empty / 空
    "",
    " ",
    "   ",
    
    # Random characters / 随机字符
    "asdf",
    "asdfasdf",
    "qwerty",
    "zxcv",
    "123456",
    "abcdef",
    "!!!",
    "???",
    "...",
    "---",
    "===",
    
    # Test inputs / 测试输入
    "test",
    "testing",
    "test message",
    "hello test",
    "123abc",
    "abc123",
    
    # Gibberish / 胡言乱语
    "asdfjkl;",
    "1234!@#$",
    "哈哈哈哈",
    "啦啦啦",
    "asdasd",
]

# =============================================================================
# All seed data combined / 所有种子数据汇总
# =============================================================================
SEED_DATA = [
    # Meaningful questions / 正式问题
    *[{"text": t, "category": "meaningful_question", "sub_category": "business_inquiry"} 
      for t in MEANINGFUL_QUESTION_EXAMPLES],
    
    # Casual chat / 闲聊
    *[{"text": t, "category": "casual_chat", "sub_category": "greeting"} 
      for t in CASUAL_CHAT_EXAMPLES[:15]],
    *[{"text": t, "category": "casual_chat", "sub_category": "acknowledgment"} 
      for t in CASUAL_CHAT_EXAMPLES[15:]],
    
    # Time/Weather / 时间天气
    *[{"text": t, "category": "time_weather_general", "sub_category": "time_query"} 
      for t in TIME_WEATHER_EXAMPLES[:10]],
    *[{"text": t, "category": "time_weather_general", "sub_category": "weather_query"} 
      for t in TIME_WEATHER_EXAMPLES[10:]],
    
    # Operation commands / 操作指令
    *[{"text": t, "category": "operation_command", "sub_category": "file_operation"} 
      for t in OPERATION_COMMAND_EXAMPLES[:10]],
    *[{"text": t, "category": "operation_command", "sub_category": "ui_operation"} 
      for t in OPERATION_COMMAND_EXAMPLES[10:20]],
    *[{"text": t, "category": "operation_command", "sub_category": "system_operation"} 
      for t in OPERATION_COMMAND_EXAMPLES[20:]],
    
    # Noise / 噪声
    *[{"text": t, "category": "noise_or_empty", "sub_category": "empty"} 
      for t in NOISE_EXAMPLES[:3]],
    *[{"text": t, "category": "noise_or_empty", "sub_category": "random_chars"} 
      for t in NOISE_EXAMPLES[3:13]],
    *[{"text": t, "category": "noise_or_empty", "sub_category": "test_input"} 
      for t in NOISE_EXAMPLES[13:16]],
    *[{"text": t, "category": "noise_or_empty", "sub_category": "gibberish"} 
      for t in NOISE_EXAMPLES[16:]],
]

# =============================================================================
# Helper functions / 辅助函数
# =============================================================================
def get_seed_count_by_category():
    """获取每个类别的种子数量 / Get seed count by category"""
    counts = {}
    for item in SEED_DATA:
        cat = item["category"]
        counts[cat] = counts.get(cat, 0) + 1
    return counts

def get_examples_by_category(category):
    """获取指定类别的所有示例 / Get all examples for a specific category"""
    return [item["text"] for item in SEED_DATA if item["category"] == category]

# Print summary / 打印摘要
if __name__ == "__main__":
    print("Seed Data Summary / 种子数据摘要")
    print("=" * 50)
    counts = get_seed_count_by_category()
    for cat, count in counts.items():
        print(f"{cat}: {count} examples")
    print(f"\nTotal: {len(SEED_DATA)} examples")