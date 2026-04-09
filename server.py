"""
W8 分組實作：MCP Server
主題：（填入你們選的主題）

分工說明：
- 各組員在 tools/ 建立自己的 Tool，import 到這裡用 @mcp.tool() 註冊
- 指定一位組員負責 @mcp.resource()
- 指定一位組員負責 @mcp.prompt()
"""

from mcp.server.fastmcp import FastMCP
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import Response
from tools.get_activity_tool import get_activity_data
from tools.get_trivia_tool import get_trivia_data
from tools.weather_tool import get_weather_data
from tools.fact_tool import get_fun_fact_data
from tools.advice_tool import get_advice_data
from tools.web_search_tool import web_search_data
from tools.weather_tool import get_weather_data
from tools.fact_tool import get_fun_fact_data
from tools.advice_tool import get_advice_data
from starlette.responses import Response
from tools.get_activity_tool import get_activity_data
from tools.get_trivia_tool import get_trivia_data



mcp = FastMCP("第1組-TravelAdvisor")


# ════════════════════════════════
#  Tools：各組員各自負責一個 Tool
# ════════════════════════════════

@mcp.tool()
def get_trivia() -> str:
    """旅途知識問答（從 OpenTDB 獲取真實題目）。
    當使用者想玩問答遊戲、測試旅遊或地理常識時使用。
    """
    return get_trivia_data()


def get_weather(city: str) -> str:
    """取得指定城市的即時天氣資訊。當使用者詢問天氣、溫度時使用。"""
    return get_weather_data(city)

@mcp.tool()
def get_fun_fact() -> str:
    """旅途趣味冷知識。"""
    return get_fun_fact_data()

@mcp.tool()
def get_advice() -> str:
    """旅行前的人生建議。"""
    return get_advice_data()

@mcp.tool()
def web_search(query: str) -> str:
    """即時搜尋網路資訊（搜尋景點、美食、天氣等）。
    當使用者需要最新的旅遊動態、在地美食評論或各國景點資訊時使用。
    """
    return web_search_data(query)


@mcp.tool()
def get_activity(city: str = None) -> str:
    """推薦旅行中的休閒活動內容。可指定城市。"""
    return get_activity_data(city)

# ════════════════════════════════
#  Resource：提供靜態參考資料
#  URI 格式：info://名稱 或 docs://名稱
# ════════════════════════════════

# 範例（替換成符合你們主題的內容）：
#
# @mcp.resource("info://tips")
# def get_tips() -> str:
#     """（主題）的實用小提示"""
#     return (
#         "實用小提示：\n"
#         "- 提示 1\n"
#         "- 提示 2\n"
#         "- 提示 3"
#     )


@mcp.resource("info://travel-tips")
def get_travel_tips() -> str:
    """旅行必帶物品與注意事項清單"""
    return (
        "旅行必帶物品：\n"
        "- 護照 / 身分證\n"
        "- 當地貨幣或信用卡\n"
        "- 備用藥品\n"
        "- 充電器與轉接頭\n\n"
        "出發前注意：\n"
        "- 確認當地天氣，準備適當衣物\n"
        "- 查詢當地緊急電話\n"
        "- 備份重要文件"
    )

@mcp.resource("info://prepare-for-travel")
def prepare_for_travel() -> str:
    """旅遊前必定檢查事項"""
    return (
        "1. 護照與簽證：確認護照效期（通常要求6個月以上），並檢查目的地是否需要簽證。\n"
        "2. 旅遊保險：購買涵蓋醫療、緊急撤離與行程取消的旅遊保險。\n"
        "3. 疫苗與健康：查詢目的地是否需要特定疫苗，並準備常用藥品。\n"
        "4. 貨幣與支付：了解當地貨幣，準備適量現金並告知銀行你的旅遊計畫。\n"
        "5. 交通與住宿：確認機票、住宿與當地交通安排。\n"
        "6. 聯絡資訊：記錄當地緊急電話、大使館與親友聯絡方式。\n"
    )


# ════════════════════════════════
#  Prompt：整合多個 Tool 的提示詞模板
#  使用者透過 /use <名稱> [參數] 呼叫
# ════════════════════════════════

# 範例（替換成符合你們主題的內容）：
#
# @mcp.prompt()
# def my_plan(topic: str) -> str:
#     """產生（主題）計畫的提示詞"""
#     return (
#         f"請幫我規劃關於 {topic} 的計畫：\n"
#         f"1. 先使用相關工具取得資訊\n"
#         f"2. 根據資訊提供 3 個具體建議\n"
#         f"3. 附上一則笑話或建議讓我開心\n"
#         f"請用繁體中文回答。"
#     )


@mcp.prompt()
def plan_trip(city: str) -> str:
    """產生旅遊行前簡報的提示詞"""
    return (
        f"我要去 {city} 旅行，請幫我準備一份完整的行前簡報：\n"
        f"1. 查詢 {city} 的天氣，判斷需要帶什麼衣物\n"
        f"2. 給我一則旅遊相關的冷知識或趣味資訊\n"
        f"3. 給我一則旅行前的人生建議\n"
        f"4. 推薦 2-3 個在 {city} 可以做的活動\n"
        f"請用繁體中文，語氣活潑。"
    )

@mcp.prompt()
def local_folklore(city: str) -> str:
    """查詢當地的風俗文化、禁忌與宗教習俗"""
    return (
        f"我想深入了解 {city} 的在地文化，請幫我進行以下研究：\n"
        f"1. 使用 web_search 查詢「{city} 旅遊禁忌」與「{city} 在地習俗」\n"
        f"2. 查詢當地的宗教信仰或特色節慶（如寺廟禮儀、傳統祭典等）\n"
        f"3. 整理出給旅人的 3 個重要文化建議，避免冒犯當地人\n"
        f"4. 根據搜尋結果，告訴我一個關於 {city} 的有趣民間傳說或歷史小故事\n"
        f"請以專業且尊重當地文化的語氣撰寫，並使用繁體中文。"
    )


if __name__ == "__main__":
    import uvicorn
    # 取得底層的 Starlette app 並加入 CORS 支援
    app = mcp.sse_app()
    
    # 手動處理 OPTIONS 請求，確保預檢（Preflight）能成功
    async def sse_options(request):
        return Response(
            status_code=200,
            headers={
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "*",
                "Access-Control-Allow-Headers": "*",
            }
        )
    app.add_route("/sse", sse_options, methods=["OPTIONS"])

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )
    # 使用手動啟動的方式，確保 CORS 介面生效
    uvicorn.run(app, host="0.0.0.0", port=8000)
