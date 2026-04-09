import requests

def get_fun_fact_data() -> str:
    """旅途趣味冷知識。"""
    try:
        url = "https://uselessfacts.jsph.pl/api/v2/facts/random"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return f"💡 旅途冷知識：\n{data['text']}"
    except Exception as e:
        return f"無法獲取冷知識：{str(e)}"
