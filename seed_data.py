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

# =============================================================================
# Financial & Banking Domain - 金融银行领域增强数据
# 涵盖: 账户、贷款、信用卡、转账、理财、外汇、保险等业务场景
# =============================================================================
FINANCIAL_BANKING_EXAMPLES = [
    # =========================================================
    # 1. 账户管理 (Account Management)
    # =========================================================
    # 开户
    "how to open a bank account",
    "how do I open a new account",
    "what documents do I need to open an account",
    "can I open an account online",
    "what is the procedure for opening a corporate account",
    "开户需要什么材料",
    "如何开通银行账户",
    "个人开户怎么办理",
    "公司开户需要哪些证件",
    "网上可以开户吗",
    "我要开户需要准备什么",
    "如何办理储蓄卡",
    "贵宾户开户有什么条件",
    
    # 销户
    "how to close my bank account",
    "how do I cancel my account",
    "what is the process to close an account",
    "账户怎么注销",
    "银行卡不想用了怎么销户",
    "如何办理账户销户",
    "信用卡怎么注销",
    "不用了想销户怎么办",
    
    # 账户查询
    "what is my account balance",
    "how can I check my balance",
    "can you tell me my account balance",
    "查询余额怎么查",
    "怎么看看我卡里还有多少钱",
    "账户余额怎么查询",
    "怎么知道卡里剩多少钱",
    "余额查询方法",
    "我要查账怎么查",
    
    # 交易明细
    "show me my transaction history",
    "how to check my account statements",
    "can I see my recent transactions",
    "我要看最近的交易记录",
    "怎么查流水账",
    "交易明细哪里看",
    "怎么打印流水",
    "账单明细怎么查询",
    "最近一个月账单明细怎么拉",
    "历史交易记录怎么查",
    
    # 冻结/解冻
    "my account has been frozen what should I do",
    "how to unfreeze my account",
    "why is my account frozen",
    "账户被冻结了怎么办",
    "银行卡冻结怎么解冻",
    "为什么我的账户会被冻结",
    "账户冻结怎么处理",
    "怎么申请解冻",
    
    # 个人信息修改
    "how to update my personal information",
    "how to change my phone number linked to account",
    "how to change my address",
    "个人信息怎么修改",
    "绑定的手机号怎么换",
    "怎么更新身份证信息",
    "地址变了怎么改",
    "证件过期了怎么更新",
    
    # =========================================================
    # 2. 贷款业务 (Loan Services)
    # =========================================================
    # 贷款申请
    "how to apply for a personal loan",
    "what are the requirements for a mortgage",
    "can I get a loan without collateral",
    "how much loan can I apply for",
    "what is the loan application process",
    "如何申请个人贷款",
    "房贷申请条件是什么",
    "无抵押贷款怎么办理",
    "我能贷多少钱",
    "贷款申请流程是什么",
    "信用贷款需要什么材料",
    "商业贷款怎么办",
    "贷款审批要多久",
    
    # 贷款利率
    "what is the current interest rate for personal loans",
    "how is the loan interest rate calculated",
    "what is the prime rate now",
    "房贷利率是多少",
    "现在贷款利率多少",
    "利息怎么算",
    "年利率和月利率有什么区别",
    "怎么计算每月还款额",
    "LPR利率是多少",
    
    # 还款方式
    "what are the repayment options",
    "how to repay my loan",
    "can I make early repayment",
    "what is the minimum repayment amount",
    "等额本金和等额本息有什么区别",
    "怎么还款最划算",
    "提前还款怎么算",
    "每月最低还多少",
    "可以分期还款吗",
    "还款日期是哪天",
    
    # 提前还款
    "how to make early repayment",
    "is there a penalty for early repayment",
    "can I pay off my loan ahead of schedule",
    "提前还款收违约金吗",
    "怎么一次性还清贷款",
    "提前还款划算吗",
    "部分提前还款怎么办理",
    "提前还贷有什么条件",
    
    # 贷款展期
    "how to extend my loan term",
    "can I extend the repayment period",
    "贷款展期怎么办理",
    "还款期限可以延长吗",
    "怎么申请延期还款",
    
    # 逾期处理
    "what happens if I miss a payment",
    "how to handle overdue loan",
    "贷款逾期了会怎样",
    "逾期还款有什么后果",
    "怎么消除逾期记录",
    "信用卡逾期怎么办",
    
    # =========================================================
    # 3. 信用卡 (Credit Cards)
    # =========================================================
    # 信用卡申请
    "how to apply for a credit card",
    "what credit cards do you offer",
    "can I apply for a credit card online",
    "what is the income requirement for a credit card",
    "怎么申请信用卡",
    "有哪些信用卡可以办",
    "网上能申请信用卡吗",
    "申请信用卡需要什么条件",
    "白金卡申请条件是什么",
    "大学生能办信用卡吗",
    
    # 账单查询
    "what is my credit card bill this month",
    "how to check my credit card statement",
    "when is the billing date",
    "what are the transactions on my card",
    "本期账单是多少",
    "怎么查信用卡账单",
    "账单日是哪天",
    "还款日是哪天",
    "最近有什么消费",
    "账单明细怎么查",
    
    # 还款
    "how to repay my credit card",
    "what is the minimum payment",
    "can I pay more than the minimum",
    "how to set up automatic repayment",
    "信用卡怎么还款",
    "最低还款额是多少",
    "可以只还最低还款额吗",
    "怎么设置自动还款",
    "什么时候还款",
    "转账到信用卡算还款吗",
    
    # 分期
    "can I pay in installments",
    "how to apply for installment payments",
    "what are the installment fees",
    "账单分期怎么办理",
    "分期手续费多少",
    "可以分几期还",
    "消费分期和账单分期有什么区别",
    "单笔消费怎么分期",
    
    # 积分
    "how to earn credit card points",
    "what can I redeem with my points",
    "how many points do I have",
    "积分怎么算",
    "积分能换什么",
    "怎么查询积分",
    "积分会过期吗",
    "积分兑换怎么操作",
    
    # 额度
    "what is my credit limit",
    "how to increase my credit limit",
    "can I temporarily increase my limit",
    "信用额度是多少",
    "怎么提高额度",
    "可以临时提额吗",
    "额度不够用怎么办",
    "固额和临额有什么区别",
    
    # 挂失
    "how to report a lost credit card",
    "my card was stolen what should I do",
    "how to cancel a lost card",
    "信用卡丢了怎么办",
    "怎么挂失信用卡",
    "卡片被盗刷怎么办",
    "怎么补办新卡",
    
    # =========================================================
    # 4. 转账汇款 (Transfers)
    # =========================================================
    # 同行转账
    "how to transfer money within the same bank",
    "how to do an internal transfer",
    "is there a fee for internal transfers",
    "本行转账怎么转",
    "行内汇款手续费多少",
    "同一银行转账多久到账",
    "网银转账怎么操作",
    "手机银行转账限额多少",
    
    # 跨行转账
    "how to transfer to another bank",
    "what is the fee for interbank transfer",
    "how long does interbank transfer take",
    "跨行转账手续费怎么算",
    "跨行汇款多久到账",
    "怎么转钱到其他银行",
    "跨行转账有额度限制吗",
    "实时跨行汇款多久到",
    
    # 跨境汇款
    "how to send an international wire transfer",
    "what information do I need for overseas transfer",
    "what are the fees for international transfer",
    "how long does international transfer take",
    "境外汇款怎么操作",
    "跨境汇款需要什么信息",
    "电汇手续费多少",
    "国际汇款多久到账",
    "SWIFT code是什么",
    "汇款到国外需要什么",
    
    # 转账限额
    "what is the daily transfer limit",
    "how to increase my transfer limit",
    "can I transfer a large amount",
    "每日转账限额多少",
    "怎么提高转账额度",
    "单笔最高能转多少",
    "限额可以调整吗",
    
    # 到账时间
    "when will the transfer arrive",
    "how long does it take for the money to arrive",
    "is the transfer processed immediately",
    "转账多久能到",
    "什么时候到账",
    "为什么还没到",
    "汇款状态怎么查询",
    
    # =========================================================
    # 5. 理财投资 (Wealth Management & Investment)
    # =========================================================
    # 理财产品
    "what wealth management products do you offer",
    "how to buy financial products",
    "what is the return rate of your products",
    "what is the risk level of this product",
    "理财产品有哪些",
    "怎么购买理财产品",
    "理财产品的收益率是多少",
    "这款产品风险大吗",
    "有没有保本理财",
    "净值型和预期收益型有什么区别",
    "理财封闭期是多长",
    
    # 基金
    "how to buy funds",
    "what types of funds are available",
    "how to redeem funds",
    "基金怎么买",
    "有哪些基金产品",
    "基金赎回几天到账",
    "指数基金和股票基金有什么区别",
    "定投基金怎么操作",
    "基金净值怎么算",
    
    # 国债
    "how to buy government bonds",
    "what is the interest rate for savings bonds",
    "国债怎么购买",
    "电子式国债怎么买",
    "国债到期怎么办",
    
    # 贵金属
    "how to buy gold",
    "do you sell physical gold",
    "what is the price of gold today",
    "怎么投资黄金",
    "纸黄金和实物金有什么区别",
    "黄金价格多少",
    "可以买白银吗",
    
    # 收益查询
    "how to check my investment returns",
    "what is my current profit or loss",
    "怎么查看理财收益",
    "持有期间收益怎么算",
    "怎么看亏了还是赚了",
    "历史收益怎么查询",
    
    # =========================================================
    # 6. 定期存款 (Time Deposits)
    # =========================================================
    "how to open a time deposit",
    "what are the interest rates for fixed deposits",
    "what is the minimum deposit amount",
    "can I withdraw my deposit early",
    "how to renew a fixed deposit",
    "定期存款怎么存",
    "存款利率是多少",
    "起存金额多少",
    "可以提前支取吗",
    "定期到期了怎么办",
    "自动转存怎么设置",
    "大额存单怎么购买",
    "存三年和存五年哪个划算",
    "靠档计息是什么意思",
    
    # =========================================================
    # 7. 外汇业务 (Foreign Exchange)
    # =========================================================
    "how to buy foreign currency",
    "what is the exchange rate today",
    "how to exchange foreign currency",
    "can I exchange currency online",
    "what currencies can I exchange",
    "购汇是什么意思",
    "结汇怎么办理",
    "今天美元汇率多少",
    "哪里可以换外汇",
    "网上可以换汇吗",
    "外汇额度是多少",
    "购汇和结汇有什么区别",
    "现汇和现钞有什么区别",
    
    # =========================================================
    # 8. 保险 (Insurance)
    # =========================================================
    "what insurance products do you offer",
    "how to buy insurance",
    "how to file an insurance claim",
    "how to check my policy",
    "有哪些保险产品",
    "怎么投保",
    "怎么理赔",
    "保险怎么报案",
    "保单怎么查询",
    "分红险和万能险有什么区别",
    "车险怎么办理",
    "意外险怎么买",
    "医疗险能报销什么",
    
    # =========================================================
    # 9. 电子银行 (Digital Banking)
    # =========================================================
    # 网银开通
    "how to activate online banking",
    "how to register for internet banking",
    "怎么开通网上银行",
    "网银怎么注册",
    "手机银行怎么开通",
    "开通网银需要什么",
    
    # U盾/令牌
    "how to use the security token",
    "how to activate the USB key",
    "token丢了怎么办",
    "U盾怎么使用",
    "动态令牌怎么绑定",
    "网银登录密码忘了怎么办",
    
    # 登录问题
    "I cannot log in to online banking",
    "I forgot my online banking password",
    "why is my account locked",
    "网银登录不了怎么办",
    "忘记登录密码怎么找回",
    "网银密码忘了",
    "登录显示账号锁定",
    
    # =========================================================
    # 10. 密码与安全 (Password & Security)
    # =========================================================
    "how to change my password",
    "how to reset my password",
    "I forgot my password what should I do",
    "密码怎么改",
    "忘记密码怎么重置",
    "取款密码忘了怎么办",
    "网银密码怎么修改",
    "怎么设置交易密码",
    "密码被锁了怎么解锁",
    
    # =========================================================
    # 11. 挂失与补办 (Loss Reporting & Replacement)
    # =========================================================
    "how to report a lost card",
    "how to apply for a replacement card",
    "how long does it take to get a new card",
    "银行卡丢了怎么办",
    "怎么补办银行卡",
    "新卡多久能拿到",
    "存折丢了可以补吗",
    "挂失后怎么取钱",
    "挂失有效期多久",
    
    # =========================================================
    # 12. 手续费 (Fees & Charges)
    # =========================================================
    "what are the bank fees",
    "is there a monthly fee for this account",
    "what transactions are free of charge",
    "手续费怎么算",
    "账户有管理费吗",
    "哪些业务免手续费",
    "跨行取款手续费多少",
    "小额账户管理费怎么收",
    "短信通知费多少",
    
    # =========================================================
    # 13. 网点服务 (Branch Services)
    # =========================================================
    "where is the nearest bank branch",
    "what are the branch working hours",
    "can I make an appointment at the branch",
    "which branch can handle this service",
    "附近有网点吗",
    "网点几点开门",
    "周末上班吗",
    "可以预约网点办理吗",
    "什么业务需要到柜台办理",
    "哪个网点可以办信用卡",
    "网点排队怎么预约",
    
    # =========================================================
    # 14. 业务预约 (Appointments)
    # =========================================================
    "how to book an appointment",
    "can I make an appointment online",
    "what appointment slots are available",
    "怎么预约",
    "可以网上预约吗",
    "预约开户怎么操作",
    "面签需要预约吗",
    "预约了还用排队吗",
    
    # =========================================================
    # 15. 投诉与建议 (Complaints & Suggestions)
    # =========================================================
    "how to file a complaint",
    "what is the customer service number",
    "how to provide feedback",
    "怎么投诉",
    "客服电话是多少",
    "有问题找谁反映",
    "服务态度不好怎么投诉",
    "行长热线是多少",
    
    # =========================================================
    # 16. 银行卡种类 (Card Types)
    # =========================================================
    "what types of cards do you have",
    "what is the difference between debit and credit card",
    "借记卡和信用卡有什么区别",
    "有哪些卡种",
    "什么是储蓄卡",
    "社保卡怎么办理",
    "医保卡怎么激活",
    
    # =========================================================
    # 17. 业务咨询 (General Inquiries)
    # =========================================================
    "what services does your bank provide",
    "can I handle this business online",
    "what identification do I need",
    "how long does this process take",
    "你们银行有什么服务",
    "这个能网上办吗",
    "需要什么证件",
    "办理需要多久",
    "周末可以办理吗",
    "可以代办吗",
    "代办需要什么材料",
]

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
    # Meaningful questions / 正式问题 (通用 + 金融银行)
    *[{"text": t, "category": "meaningful_question", "sub_category": "business_inquiry"} 
      for t in MEANINGFUL_QUESTION_EXAMPLES],
    *[{"text": t, "category": "meaningful_question", "sub_category": "financial_banking"} 
      for t in FINANCIAL_BANKING_EXAMPLES],
    
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