# utils/web_search.py

# SERPAPI is not being used, so we avoid any import errors

def live_search(query):
    try:
        # Stubbed response for now
        return f"(Live search is currently disabled. You searched for: '{query}')"
    except Exception as e:
        return f"Live search error: {str(e)}"
