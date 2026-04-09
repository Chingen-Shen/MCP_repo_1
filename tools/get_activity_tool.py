"""
Tool：取得當地活動

輸入地點的關鍵字後，會回傳一系列的活動建議。
"""

import httpx

TOOL_INFO = {
    "name": "get_activity",
    "api": "https://bored-api.appbrewery.com/random",
    "author": "黃柏豪",
}

def get_activity_data(city: str = None) -> str:
    """推薦活動（透過 Bored API 取得靈感）。
    當使用者覺得無聊、想找點事情做或需要活動建議時使用。
    """
    url = "https://bored-api.appbrewery.com/random"
    try:
        # 設定較短的 timeout 避免阻塞
        response = httpx.get(url, timeout=10.0)
        response.raise_for_status()
        data = response.json()

        activity = data.get("activity", "找不到活動內容")
        category = data.get("type", "其他")
        participants = data.get("participants", 1)
        price_range = data.get("price", 0)

        # 簡單的活動類別對應表
        type_map = {
            "education": "📚 教育學習",
            "recreational": "🎾 休閒娛樂",
            "social": "👯 社交活動",
            "diy": "🛠️ 手作 DIY",
            "charity": "💖 公益慈善",
            "cooking": "🍳 烹飪美食",
            "relaxation": "🧘 放鬆身心",
            "music": "🎵 音樂藝術",
            "busywork": "📋 規律事務",
        }
        category_zh = type_map.get(category, category)

        # 價格描述
        price_msg = "💎 免費" if price_range == 0 else "💳 付費活動" if price_range > 0.5 else "🪙 低花費"

        city_prefix = f"在 {city} " if city else ""
        return (
            f"🎯【活動推薦】\n\n"
            f"💡 建議：{city_prefix}{activity}\n"
            f"🏷️ 類型：{category_zh}\n"
            f"👥 人數：{participants} 人\n"
            f"💰 花費：{price_msg}\n\n"
            f"這是一個不錯的點子，試試看吧！✨"
        )
    except Exception as e:
        return f"暫時無法取得活動建議，請稍後再試。 (錯誤: {str(e)})"
