import wikipedia
from typing import Dict

class WikiTool:
    def __init__(self, lang: str = "en"):
        wikipedia.set_lang(lang)

    def search_summary(self, topic: str, sentences: int = 3) -> Dict:
        """Return a dict with title, summary, url or an error field."""
        try:
            # Try exact page first
            summary = wikipedia.summary(topic, sentences=sentences, auto_suggest=False, redirect=True)
            page = wikipedia.page(topic, auto_suggest=False, redirect=True)
            return {"title": page.title, "summary": summary, "url": page.url}
        except wikipedia.DisambiguationError as e:
            # Pick best option (first) — this can be improved later
            try:
                opt = e.options[0]
                summary = wikipedia.summary(opt, sentences=sentences)
                page = wikipedia.page(opt)
                return {"title": page.title, "summary": summary, "url": page.url}
            except Exception as ex:
                return {"error": str(ex)}
        except Exception as ex:
            return {"error": str(ex)}