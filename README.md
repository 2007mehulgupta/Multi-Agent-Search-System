# 🔎 Multi-Agent Research System

A multi-agent AI research assistant that searches the web, reads the most relevant source in depth, writes a structured report, and then critiques its own work — all powered by Google Gemini and Tavily Search.

## How It Works

The system runs a 4-step pipeline:

1. **Search Agent** — Uses Tavily to search the web for recent, reliable information on the given topic.
2. **Reader Agent** — Picks the most relevant URL from the search results and scrapes it for deeper content using BeautifulSoup.
3. **Writer Chain** — Synthesizes the search results and scraped content into a structured research report (Introduction, Key Findings, Conclusion, Sources).
4. **Critic Chain** — Reviews the generated report, scores it out of 10, and gives strengths, areas to improve, and a one-line verdict.

## Features

- Multi-agent architecture built with LangChain's `create_agent`
- Web search via the Tavily API
- Web scraping/reading via BeautifulSoup
- Structured report generation and self-critique using Google Gemini (`gemini-3.6-flash`)
- Interactive Streamlit UI with step-by-step progress, tabs for report/critique/raw research, and a downloadable `.md` report
- CLI mode via `pipeline.py` for running the pipeline without the UI

## Requirements

- Python 3.10+
- API keys for:
  - [Tavily](https://tavily.com/)
  - [Google Gemini](https://aistudio.google.com/apikey)

## Setup

1. Clone the repository
   ```bash
   git clone https://github.com/2007mehulgupta-creator/Multi-Agent-Search-System.git
   cd Multi-Agent-Search-System
   ```

2. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root with your API keys:
   ```
   TAVILY_API_KEY=your_key_here
   GOOGLE_API_KEY=your_key_here
   ```

## Usage

### Streamlit UI (recommended)

```bash
streamlit run app.py
```

Enter a research topic in the text box and click **Run research**. The app will show live progress through each of the 4 pipeline steps, then display the final report, critic feedback, and raw research in separate tabs. The report can be downloaded as a Markdown file.

### Command line

```bash
python pipeline.py
```

You'll be prompted to enter a research topic, and the pipeline will print each step's output (search results, scraped content, report, and critique) to the console.

## Project Structure

```
Multi-Agent-Search-System/
├── agents.py           # Defines the search agent, reader agent, writer chain, and critic chain
├── app.py               # Streamlit UI — runs the full pipeline interactively
├── pipeline.py           # CLI version of the pipeline
├── tools.py              # Web search (Tavily) and URL scraping (BeautifulSoup) tools
├── requirements.txt
└── .env                  # API keys (not tracked in git)
```

## Notes

- The `.env` file is excluded from version control via `.gitignore` — never commit your API keys.
- Scraped content is truncated to 3000 characters per source to keep requests efficient.
