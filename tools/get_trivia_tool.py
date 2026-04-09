import requests

# Tool 資訊（給人看的，不影響 MCP）
TOOL_INFO = {
    "name": "get_trivia",
    "api": "https://opentdb.com/api.php?amount=1&category=22",
    "author": "黃柏豪",
}

def get_trivia_data() -> str:
    """旅途知識問答（從 OpenTDB 獲取真實題目）。
    當使用者想玩問答遊戲、測試旅遊或地理常識時使用。
    """
    import httpx
    import html
    import random

    # OpenTDB API, category 22 是地理 (Geography)，適合旅途主題
    url = "https://opentdb.com/api.php?amount=1&category=22"
    
    try:
        response = httpx.get(url, timeout=10.0)
        response.raise_for_status()
        data = response.json()

        if data.get("response_code") != 0:
            return "暫時找不到題目，請稍後再試。"

        result = data["results"][0]
        question = html.unescape(result["question"])
        correct_answer = html.unescape(result["correct_answer"])
        incorrect_answers = [html.unescape(ans) for ans in result["incorrect_answers"]]
        category = html.unescape(result["category"])
        difficulty = result["difficulty"].capitalize()

        # 組合所有選項並打散
        options = incorrect_answers + [correct_answer]
        random.shuffle(options)

        options_str = "\n".join([f"- {opt}" for opt in options])

        return (
            f"🌍【旅途知識問答 — {category}】\n"
            f"標籤：{difficulty}\n\n"
            f"❓ 問題：{question}\n\n"
            f"💡 選項：\n{options_str}\n\n"
            f"請想好答案後，問我正確解答！"
        )
    except Exception as e:
        return f"連線到題庫時發生錯誤：{str(e)}"