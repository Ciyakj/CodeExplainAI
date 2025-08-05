
import requests
from config.config import SERPAPI_API_KEY

def live_search(query):
    try:
        params = {
            "q": query,
            "api_key": SERPAPI_API_KEY,
            "engine": "google"
        }
        res = requests.get("https://serpapi.com/search", params=params)
        data = res.json()
        return data["organic_results"][0]["snippet"]
    except:
        return "No results from live search."
