from ddgs import DDGS
import logging
import time
from functools import lru_cache

# 設定小型日誌
logger = logging.getLogger(__name__)

@lru_cache(maxsize=20)
def web_search_data(query: str) -> str:
    """即時搜尋網路資訊（搜尋景點、美食、天氣等）。
    當使用者需要最新的旅遊動態、在地美食評論或各國景點資訊時使用。
    """
    # 刻意延遲 2 秒，防止 Gemini API 因過快回傳結果而頻繁觸發 429 RPM 限制
    time.sleep(2)
    
    try:
        results = []
        # 使用 DDGS 進行網路搜尋
        with DDGS() as ddgs:
            # max_results=2 取得前 2 筆結果，降低 Token 消耗
            for r in ddgs.text(query, max_results=2):
                title = r.get('title', '無標題')
                href = r.get('href', '#')
                body = r.get('body', '無摘要內容')
                
                # 限制摘要長度為 300 字
                body_truncated = (body[:300] + '...') if len(body) > 300 else body
                
                results.append(
                    f"🔗 [{title}]({href})\n"
                    f"📝 {body_truncated}\n"
                )
        
        if not results:
            return f"🔍 搜尋結果：找不到關於「{query}」的相關內容。請嘗試更換關鍵字再試一次。"

        content = "\n---\n".join(results)
        return (
            f"🔍 【網路搜尋結果：{query}】\n\n"
            f"{content}\n\n"
            f"---\n"
            f"*資訊來自 DuckDuckGo 搜尋 (已進行速率優化)*"
        )
        
    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg or "Ratelimit" in error_msg:
            return "⚠️ 搜尋服務目前過於繁忙（Rate Limit），請稍候片刻再試。"
        logger.error(f"Web search error: {error_msg}")
        return f"⚠️ 搜尋時發生錯誤，請稍後再試。 (詳細資訊: {error_msg})"