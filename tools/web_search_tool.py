import requests
from ddgs import DDGS
import logging

# 設定小型日誌
logger = logging.getLogger(__name__)

def web_search_data(query: str) -> str:
    """即時搜尋網路資訊（搜尋景點、美食、天氣等）。
    當使用者需要最新的旅遊動態、在地美食評論或各國景點資訊時使用。
    """
    try:
        results = []
        # 使用 DDGS 進行網路搜尋
        with DDGS() as ddgs:
            # max_results=5 取得前 5 筆結果
            # 可以根據需求設定 region，例如 'wt-wt' (全球) 或 'tw-tzh' (台灣)
            for r in ddgs.text(query, max_results=5):
                title = r.get('title', '無標題')
                href = r.get('href', '#')
                body = r.get('body', '無摘要內容')
                
                results.append(
                    f"🔗 [{title}]({href})\n"
                    f"📝 {body}\n"
                )
        
        if not results:
            return f"🔍 搜尋結果：找不到關於「{query}」的相關內容。請嘗試更換關鍵字再試一次。"

        content = "\n---\n".join(results)
        return (
            f"🔍 【網路搜尋結果：{query}】\n\n"
            f"{content}\n\n"
            f"---\n"
            f"*資訊來自 DuckDuckGo 搜尋*"
        )
        
    except Exception as e:
        logger.error(f"Web search error: {str(e)}")
        return f"⚠️ 搜尋時發生錯誤，請稍後再試。 (詳細資訊: {str(e)})"