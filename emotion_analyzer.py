"""
情绪分析程序
支持6种情绪：平常、开心、伤心、生气、得意、害羞
"""

# 情绪关键词字典（按长度降序排列，优先匹配长词）
EMOTION_KEYWORDS = {
    "开心": [
        "好开心", "太开心", "真开心", "好高兴", "太高兴", "太好了", "好棒", "太棒了",
        "好极了", "超级棒", "太爽了", "真好",
        "哈哈哈", "哈哈", "开心", "高兴", "快乐", "棒", "爽", "赞",
        "幸福", "满足", "兴奋", "欢乐", "愉快", "美好",
        "耶", "嘿嘿", "哇", "欣喜"
    ],
    "伤心": [
        "好难过", "太难过", "好伤心", "太伤心", "好惨", "悲催",
        "伤心", "难过", "悲伤", "痛苦", "失望", "沮丧", "心碎", "绝望",
        "孤独", "寂寞", "郁闷", "抑郁", "忧伤", "惆怅", "呜呜", "可怜",
        "心痛", "呜", "崩溃", "无助", "心酸", "凄凉", "落寞", "想哭"
    ],
    "生气": [
        "气死了", "气死我", "太气人", "真烦", "好烦", "烦死了",
        "生气", "愤怒", "气死", "讨厌", "可恶",
        "火大", "暴怒", "气愤", "恼火", "烦躁", "受够了",
        "气人", "恼怒", "发火", "愤恨", "狂怒", "不爽",
        "可恨", "该死", "闭嘴", "怒了", "混蛋", "滚"
    ],
    "得意": [
        "就是这么强", "不在话下", "我最棒", "我厉害", "我赢了", "我成功",
        "太简单", "小意思", "哼哼",
        "得意", "骄傲", "厉害", "无敌", "最强", "完美", "优秀",
        "天才", "聪明", "成功", "胜利", "赢了", "搞定", "轻松",
        "没问题", "简单", "小case", "666", "牛"
        # 注意：已删除单独的"哈"，避免语气词误判
    ],
    "害羞": [
        "好害羞", "太害羞", "好尴尬", "太尴尬", "怪不好意思", "羞羞",
        "不好意思", "难为情",
        "害羞", "脸红", "尴尬", "羞涩", "腼腆", "扭捏",
        "羞愧", "惭愧", "羞耻", "丢人", "丢脸", "脸热",
        "嘤嘤", "捂脸", "///"
    ]
}

# 否定词列表
NEGATION_WORDS = ["不", "没", "没有", "别", "不是", "不会", "未", "无", "不太", "不怎么", "并不", "毫不"]

# 否定窗口大小（否定词后N个字符内的情绪词会被反转）
NEGATION_WINDOW = 6

# 情绪反转映射（被否定后变成什么情绪）
EMOTION_NEGATION_MAP = {
    "开心": "伤心",
    "伤心": "平常",
    "生气": "平常",
    "得意": "平常",
    "害羞": "平常",
}

# 需要排除的误伤词（包含情绪关键词但不表达该情绪）
EXCLUDE_WORDS = {
    "烦": ["烦恼", "麻烦", "烦请", "不厌其烦", "烦劳"],
    "恨": ["遗恨", "恨不得"],
    "哭": ["哭笑不得"],
    "爱": ["爱好", "可爱"],
    "笑": ["笑话", "笑柄", "笑料"],
    "牛": ["牛奶", "牛肉", "牛排", "蜗牛", "牛仔"],
}


def is_keyword_excluded(text: str, keyword: str) -> bool:
    """检查关键词是否应被排除（被更长的非情绪词包含）"""
    if keyword not in EXCLUDE_WORDS:
        return False
    for exclude_word in EXCLUDE_WORDS[keyword]:
        if exclude_word in text:
            return True
    return False


def find_all_occurrences(text: str, keyword: str) -> list:
    """找到关键词在文本中的所有位置"""
    positions = []
    start = 0
    while True:
        pos = text.find(keyword, start)
        if pos == -1:
            break
        positions.append((pos, pos + len(keyword)))
        start = pos + 1
    return positions


def find_negation_positions(text: str) -> list:
    """找到所有否定词的位置"""
    positions = []
    for neg_word in NEGATION_WORDS:
        start = 0
        while True:
            pos = text.find(neg_word, start)
            if pos == -1:
                break
            # 记录否定词结束位置（影响范围从这里开始）
            positions.append(pos + len(neg_word))
            start = pos + 1
    return sorted(positions)


def is_negated(keyword_start: int, negation_positions: list) -> bool:
    """检查关键词是否在否定窗口内"""
    for neg_end in negation_positions:
        # 关键词起始位置在否定词结束后的窗口内
        if 0 <= keyword_start - neg_end <= NEGATION_WINDOW:
            return True
    return False


def analyze_emotion(text: str) -> dict:
    """
    分析输入文本的情绪

    Args:
        text: 输入的文本

    Returns:
        包含情绪类型和置信度的字典
    """
    text = text.strip()

    # 统计各情绪的匹配分数
    scores = {
        "平常": 0,
        "开心": 0,
        "伤心": 0,
        "生气": 0,
        "得意": 0,
        "害羞": 0
    }

    # 记录已匹配的位置，避免重复计分
    matched_ranges = []

    # 找到所有否定词位置
    negation_positions = find_negation_positions(text)

    def is_position_matched(start: int, end: int) -> bool:
        """检查位置是否已被更长的词匹配"""
        for m_start, m_end in matched_ranges:
            if start >= m_start and end <= m_end:
                return True
        return False

    # 匹配情绪关键词（长词优先，已在列表中排序）
    for emotion, keywords in EMOTION_KEYWORDS.items():
        for keyword in keywords:
            # 检查是否应被排除
            if is_keyword_excluded(text, keyword):
                continue

            positions = find_all_occurrences(text, keyword)
            for start, end in positions:
                if not is_position_matched(start, end):
                    matched_ranges.append((start, end))
                    weight = len(keyword) * 0.5

                    # 检查是否被否定
                    if is_negated(start, negation_positions):
                        # 情绪反转
                        target_emotion = EMOTION_NEGATION_MAP.get(emotion, "平常")
                        scores[target_emotion] += weight
                    else:
                        scores[emotion] += weight

    # 找出最高分的情绪
    max_emotion = max(scores, key=scores.get)
    max_score = scores[max_emotion]

    # 如果没有明显情绪，返回"平常"
    if max_score == 0:
        return {
            "emotion": "平常",
            "confidence": 1.0,
            "scores": scores,
            "description": get_emotion_description("平常")
        }

    # 计算置信度（归一化）
    total_score = sum(scores.values())
    confidence = max_score / total_score if total_score > 0 else 0

    return {
        "emotion": max_emotion,
        "confidence": round(confidence, 2),
        "scores": scores,
        "description": get_emotion_description(max_emotion)
    }


def get_emotion_description(emotion: str) -> str:
    """获取情绪的描述"""
    descriptions = {
        "平常": "这句话表达的是平常的情绪，没有明显的情感倾向。",
        "开心": "这句话表达了开心、快乐的情绪！😊",
        "伤心": "这句话表达了伤心、难过的情绪... 😢",
        "生气": "这句话表达了生气、愤怒的情绪！😠",
        "得意": "这句话表达了得意、骄傲的情绪！😎",
        "害羞": "这句话表达了害羞、不好意思的情绪... 😳"
    }
    return descriptions.get(emotion, "")


def print_result(result: dict):
    """美化输出结果"""
    print("\n" + "=" * 50)
    print(f"  检测到的情绪: 【{result['emotion']}】")
    print(f"  置信度: {result['confidence'] * 100:.0f}%")
    print(f"  {result['description']}")
    print("=" * 50)

    # 显示各情绪分数
    print("\n  各情绪得分:")
    for emotion, score in result['scores'].items():
        bar_length = int(score * 2)
        bar = "█" * bar_length
        print(f"    {emotion}: {bar} ({score:.1f})")
    print()


def main():
    """主函数"""
    print("\n" + "=" * 50)
    print("  欢迎使用情绪分析程序")
    print("  支持的情绪: 平常、开心、伤心、生气、得意、害羞")
    print("  输入 'quit' 或 '退出' 结束程序")
    print("=" * 50)

    while True:
        try:
            text = input("\n请输入一句话: ").strip()

            if text.lower() in ['quit', 'exit', '退出', '结束']:
                print("\n感谢使用，再见！👋\n")
                break

            if not text:
                print("请输入有效的文本！")
                continue

            result = analyze_emotion(text)
            print_result(result)

        except KeyboardInterrupt:
            print("\n\n程序已退出。")
            break
        except Exception as e:
            print(f"发生错误: {e}")


if __name__ == "__main__":
    main()
