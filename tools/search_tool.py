

from typing import List, Dict

# Try importing SerpAPI
try:
    from serpapi import GoogleSearch
    SERPAPI_AVAILABLE = True
except ImportError:
    SERPAPI_AVAILABLE = False
    GoogleSearch = None

# Try importing DuckDuckGo
try:
    from duckduckgo_search import DDGS
    DUCK_AVAILABLE = True
except ImportError:
    DUCK_AVAILABLE = False
    DDGS = None


class SearchTool:
    def __init__(self, api_key: str = None):
        self.api_key = api_key
        self.use_serpapi = bool(api_key and SERPAPI_AVAILABLE)
        self.use_duckduckgo = DUCK_AVAILABLE

        if self.use_serpapi:
            print("🔍 Using SerpAPI for search.")
        elif self.use_duckduckgo:
            print("🦆 Using DuckDuckGo as fallback.")
        else:
            print("⚠️ No search backend available! Please install `serpapi` or `duckduckgo-search`.")

    def search(self, query: str, num: int = 5) -> List[Dict]:
        """Perform a search using SerpAPI or DuckDuckGo."""
        results = []

        # --- Try SerpAPI first ---
        if self.use_serpapi:
            try:
                search = GoogleSearch({
                    "q": query,
                    "api_key": self.api_key,
                    "num": num
                })
                data = search.get_dict()
                for item in data.get("organic_results", []):
                    results.append({
                        "source": "SerpAPI",
                        "title": item.get("title"),
                        "link": item.get("link"),
                        "snippet": item.get("snippet")
                    })
                if results:
                    return results
            except Exception as e:
                print(f"⚠️ SerpAPI search failed: {e}")

        # --- Fallback: DuckDuckGo ---
        if self.use_duckduckgo:
            try:
                with DDGS() as ddgs:
                    for r in ddgs.text(query, max_results=num):
                        results.append({
                            "source": "DuckDuckGo",
                            "title": r.get("title"),
                            "link": r.get("href"),
                            "snippet": r.get("body")
                        })
                if results:
                    return results
            except Exception as e:
                print(f"⚠️ DuckDuckGo search failed: {e}")

        # --- If both fail ---
        return [{
            "source": "Search",
            "title": query,
            "snippet": "Search lookup failed: No backend available",
            "link": None
        }]
