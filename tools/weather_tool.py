import requests

def get_weather_data(city: str) -> str:
    """取得指定城市的即時天氣資訊。"""
    try:
        url = f"https://wttr.in/{city}?format=j1"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        current = data['current_condition'][0]
        temp_c = current['temp_C']
        desc = current['weatherDesc'][0]['value']
        humidity = current['humidity']
        
        return f"📍 {city} 的當前天氣：\n🌡️ 溫度：{temp_c}°C\n🌤️ 況狀：{desc}\n💧 濕度：{humidity}%"
    except Exception as e:
        return f"無法取得天氣資訊：{str(e)}"
