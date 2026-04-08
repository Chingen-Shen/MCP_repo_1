"""
Tool：提供旅途相關的知識問答（Trivia）

觸發條件：
- 當使用者詢問旅遊常識、旅行小知識、出國須知或想測試旅遊知識時使用。
"""

def get_trivia_data(topic: str = "隨機") -> str:
    """提供旅途相關的知識問答（Trivia）。
    當使用者詢問旅遊常識、旅行小知識、出國須知或想測試旅遊知識時使用。
    topic 可選：交通、安全、文化、美食、語言、隨機
    """
    valid_topics = ["交通", "安全", "文化", "美食", "語言"]
    topic_hint = topic if topic in valid_topics else "任意旅途相關"

    return (
        f"請你扮演一位旅遊達人，針對「{topic_hint}」主題，"
        f"自由發揮出一道有趣的旅途知識問答（Trivia）。\n\n"
        f"格式如下：\n"
        f"🌍【旅途知識問答 — {topic_hint}】\n\n"
        f"❓ 問題：（請自行設計一個有趣、實用的旅遊問題）\n\n"
        f"✅ 解答：（請提供清楚且知識性的解答）\n\n"
        f"請用繁體中文回答，內容要有趣、實用，讓旅人印象深刻。\n"
        f"（可選主題：{'、'.join(valid_topics)}、隨機）"
    )