import asyncio
import os
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types
from mcp import ClientSession, StdioServerParameters
from mcp.client.sse import sse_client

# 讀取環境變數
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
SERVER_URL = "http://localhost:8000/sse"

if not GEMINI_API_KEY:
    print("❌ 錯誤：請在 .env 檔案中設定 GEMINI_API_KEY")
    exit(1)

# 初始化 Gemini Client
client = genai.Client(api_key=GEMINI_API_KEY)
MODEL_ID = "gemini-flash-latest"

async def run_agent():
    print(f"🚀 正在連接到 MCP Server: {SERVER_URL}...")
    
    try:
        async with sse_client(SERVER_URL) as (read, write):
            async with ClientSession(read, write) as session:
                # 初始化會話
                await session.initialize()
                print("✅ 已成功連接到 MCP Server")

                # 1. 取得工具清單
                tools_response = await session.list_tools()
                mcp_tools = tools_response.tools
                print(f"🔍 偵測到 {len(mcp_tools)} 個工具：{[t.name for t in mcp_tools]}")

                # 2. 轉換為 Gemini Tool 格式
                # google-genai SDK 接受字典格式的 function_declarations
                gemini_tools = []
                for tool in mcp_tools:
                    gemini_tools.append({
                        "name": tool.name,
                        "description": tool.description,
                        "parameters": tool.inputSchema
                    })
                
                # 包裝成 Gemini 預期的工具格式
                tool_config = types.Tool(function_declarations=gemini_tools)

                # 3. 對話迴圈
                chat = client.chats.create(model=MODEL_ID)
                
                print("\n🤖 Agent 已就緒！請輸入您的問題（輸入 'exit' 結束）：")
                
                while True:
                    user_input = input("👤 您：")
                    if user_input.lower() in ["exit", "quit", "離開", "結束"]:
                        break
                    
                    if not user_input.strip():
                        continue

                    # 呼叫 Gemini
                    # 注意：google-genai SDK 會自動處理某些部分，但我們需要手動處理 Tool Call 回傳
                    try:
                        response = chat.send_message(
                            user_input,
                            config=types.GenerateContentConfig(tools=[tool_config])
                        )

                        # 處理可能的工具呼叫 (Multi-turn Tool Use)
                        while response.candidates[0].content.parts and \
                              response.candidates[0].content.parts[0].function_call:
                            
                            for part in response.candidates[0].content.parts:
                                if part.function_call:
                                    func_name = part.function_call.name
                                    func_args = part.function_call.args
                                    
                                    print(f"⚙️ 執行工具：{func_name}({func_args})")
                                    
                                    # 透過 MCP 呼叫工具
                                    result = await session.call_tool(func_name, arguments=func_args)
                                    
                                    # 將結果送回 Gemini
                                    # 注意：這裡需要將結果包裝成 FunctionResponse
                                    # 在新版的 SDK 中，我們需要建立新的 Part
                                    response = chat.send_message(
                                        types.Part.from_function_response(
                                            name=func_name,
                                            response={"result": result.content[0].text if result.content else "無回傳結果"}
                                        )
                                    )
                        
                        # 最後顯示回答文字
                        if response.text:
                            print(f"🤖 AI：{response.text}")
                        else:
                            # 有時 response.text 會報錯如果沒有文字內容（只有 tool call）
                            # 但上面的 loop 應該已經處理完 tool call 了
                            pass

                    except Exception as e:
                        print(f"❌ 發生錯誤：{str(e)}")

    except Exception as e:
        print(f"🌐 連線失敗：{str(e)}")
        print("請確認 server.py 是否已經在執行中 (python server.py)")

if __name__ == "__main__":
    try:
        asyncio.run(run_agent())
    except KeyboardInterrupt:
        print("\n👋 已中止程式")
