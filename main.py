

import os
import sys
from typing import List, Dict
from dotenv import load_dotenv

load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI
from tools.wiki_tool import WikiTool
from tools.search_tool import SearchTool  # Supports DuckDuckGo fallback

# ----------------------------
# Environment setup
# ----------------------------
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")

if not GEMINI_API_KEY:
    print(" Please set GEMINI_API_KEY in your environment (or in .env).")
    sys.exit(1)

# ----------------------------
# Configure Gemini LLM
# ----------------------------
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=GEMINI_API_KEY,
    temperature=0.7,
)

# ----------------------------
# Initialize Tools
# ----------------------------
wiki = WikiTool()
search = SearchTool(api_key=SERPAPI_API_KEY)  # Handles fallback internally

# ----------------------------
# Research + Blog Generation
# ----------------------------
def research_topic(topic: str, wiki_sentences: int = 3, search_num: int = 5) -> List[Dict]:
    """Run research tools and return a list of valid snippet dicts (skip failed lookups)."""
    snippets = []

    # 1) Wikipedia
    try:
        w = wiki.search_summary(topic, sentences=wiki_sentences)
        if w and not w.get("error"):
            snippets.append({
                "source": "Wikipedia",
                "title": w.get("title"),
                "summary": w.get("summary"),
                "url": w.get("url")
            })
    except Exception as e:
        print(f"⚠️ Wikipedia lookup failed: {e}")

    # 2) Web Search
    try:
        results = search.search(topic, num=search_num)
        for r in results:
            # Only add real results (skip failed lookups)
            snippet = r.get("snippet") or ""
            if snippet and "failed" not in snippet.lower():
                snippets.append({
                    "source": r.get("source", "Web"),
                    "title": r.get("title"),
                    "summary": snippet,
                    "url": r.get("link")
                })
    except Exception as e:
        print(f"⚠️ Web search failed: {e}")

    return snippets

def build_prompt(topic: str, snippets: List[Dict]) -> str:
    """Build the final prompt for the LLM using the template."""
    if not snippets:
        snippets_text = "(No research snippets available; insights are based on general knowledge.)"
    else:
        lines = []
        for i, s in enumerate(snippets, start=1):
            title = s.get("title") or "(no title)"
            summary = s.get("summary") or "(no summary)"
            url = s.get("url") or "(no url)"
            src = s.get("source") or "Web"
            lines.append(f"[{i}] {src}: {title} - {summary} (URL: {url})")
        snippets_text = "\n".join(lines)

    template_path = os.path.join(os.path.dirname(__file__), "templates", "blog_prompt_template.txt")
    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    return template.format(topic=topic, snippets=snippets_text)

def generate_blog(topic: str):
    snippets = research_topic(topic)
    prompt = build_prompt(topic, snippets)

    print("\n--- Prompt sent to LLM (truncated) ---\n")
    print(prompt[:1500])
    print("\n--- End prompt preview ---\n")

    response = llm.invoke(prompt)
    return response

def save_output(topic: str, output, out_dir: str = "outputs") -> str:
    os.makedirs(out_dir, exist_ok=True)
    safe_topic = topic.replace(" ", "_").lower()[:80]
    path = os.path.join(out_dir, f"blog_{safe_topic}.md")

    with open(path, "w", encoding="utf-8") as f:
        f.write(output.content if hasattr(output, "content") else str(output))

    return path

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py \"topic\"")
        sys.exit(1)

    topic = sys.argv[1]
    blog = generate_blog(topic)
    out_path = save_output(topic, blog)
    print(f"✅ Blog saved to: {out_path}")

if __name__ == "__main__":
    main()

