# AI Blog Generator

A Python-based tool that automates research and generates well-structured blog posts on any topic. It leverages Wikipedia, web search (SerpAPI or DuckDuckGo), and Google Gemini LLM to produce informative and coherent content.

---

## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Input and Output Samples](#input-and-output-samples)
- [Project Flow](#project-flow)
- [Challenges Encountered](#challenges-encountered)
- [Suggestions for Improvement](#suggestions-for-improvement)
- [Folder Structure](#folder-structure)
- [Conclusion](#conclusion)
---

## Project Overview

The AI Blog Generator is designed to reduce the time and effort required for researching and writing blog posts. Given a topic, it:

1. Fetches summaries from Wikipedia using `WikiTool`.
2. Fetches additional snippets from the web using `SearchTool` (SerpAPI with DuckDuckGo fallback).
3. Combines the research snippets into a structured prompt.
4. Sends the prompt to Google Gemini LLM to generate a coherent blog post.
5. Saves the generated blog in Markdown format.

---

## Features

- Multi-source research: Wikipedia + web search.
- Fallback mechanism: DuckDuckGo used if SerpAPI is unavailable.
- Template-driven prompt for consistent blog structure.
- Automatic Markdown output for easy publishing.
- Inline citations referencing research snippets.
- Error handling: Skips failed lookups to maintain content quality.

---

## Installation

1. **Clone the repository**
```bash
git clone <repo-url>
cd ai-blog-generator
```
2. **Create and activate a virtual environment**
```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```
3. **Install dependencies**
```bash
pip install -r requirements.txt
```
4. **Set up environment variables**
- Create a .env file in the project root:
```bash
GEMINI_API_KEY=<your_gemini_api_key>
SERPAPI_API_KEY=<your_serpapi_api_key>  # Optional, DuckDuckGo is fallback
```

## Usage
- Run the program with a topic as a command-line argument:
```bash
python main.py "The Future of AI in Healthcare"
```
## Input and Output Samples
### Input
```bash
python main.py "Impact of Renewable Energy"
```
### Output
```bash
# The Rise of Renewable Energy: Shaping a Sustainable Future

## Introduction
Renewable energy is transforming the global energy landscape...

## Solar Power Innovations
According to [1], solar panel efficiency has increased...

## Wind Energy Advances
Studies show wind turbines are becoming more cost-effective...

## Summary
- Renewable energy adoption is accelerating globally [1].
- Solar and wind are the fastest-growing sources [2].
- Investment in clean tech is critical for sustainability [3].
```

## Project Flow
1.**main.py orchestrates the workflow**:

- Accepts topic input.

- Runs WikiTool and SearchTool to gather research snippets.

- Builds a structured prompt using a template.

- Sends prompt to Google Gemini LLM.

- Saves the output as Markdown.

2.**tools/wiki_tool.py**

- Fetches Wikipedia summary and URL for a given topic.

- Handles disambiguation errors by picking the first suggestion.

3.**tools/search_tool.py**

- Searches the web using SerpAPI (preferred) or DuckDuckGo (fallback).

- Returns snippet, title, and link.

- Handles failed lookups gracefully.

## Challenges Encountered

- Handling Wikipedia disambiguation pages and ensuring relevant summaries.

- SerpAPI failures or missing API keys; implemented DuckDuckGo fallback.

- Constructing prompts that guide the LLM to produce structured blog content.

- Managing long text outputs and formatting for Markdown.

## Suggestions for Improvement

- Integrate a GUI or web app interface for real-time blog generation.

- Add multi-language support for research and generated blogs.

- Enhance snippet selection using relevance scoring or keyword extraction

## Folder Structure
```bash
ai-blog-generator/
├── main.py
├── requirements.txt
├── .gitignore
├── .env
├── tools/
│   ├── wiki_tool.py
│   └── search_tool.py
├── templates/
│   └── blog_prompt_template.txt
├── outputs/
│   └── blog_<topic>.md
└── samples/
    ├── input_example1.txt
    └── output_example_1.md
```
## Conclusion

The AI Blog Generator showcases how modern AI tools can streamline research and content creation, bridging the gap between information gathering and polished writing. 
By combining Wikipedia, web search, and Google Gemini LLM, the project demonstrates a practical, real-world application of AI while maintaining accuracy, structure, and readability.
