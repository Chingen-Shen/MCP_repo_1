import requests

def get_advice_data() -> str:
    """旅行前的人生建議。"""
    try:
        url = "https://api.adviceslip.com/advice"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return f"🌟 給您的旅行建議：\n{data['slip']['advice']}"
    except Exception as e:
        return f"無法獲取建議：{str(e)}"
