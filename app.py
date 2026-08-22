import streamlit as st
from agents import build_search_agent, build_reader_agent, writer_chain, critic_chain

st.set_page_config(page_title="Multi-Agent Research System", page_icon="🔎", layout="wide")

if "state" not in st.session_state:
    st.session_state.state = None
if "history" not in st.session_state:
    st.session_state.history = []

st.title("🔎 Multi-Agent Research System")
st.caption("Search agent → Reader agent → Writer chain → Critic chain")

with st.sidebar:
    st.header("History")
    if st.session_state.history:
        for i, past_topic in enumerate(reversed(st.session_state.history)):
            st.write(f"{len(st.session_state.history) - i}. {past_topic}")
    else:
        st.write("No runs yet.")
    st.divider()
    st.caption("Make sure OPENAI_API_KEY and TAVILY_API_KEY are set in your .env file.")

topic = st.text_input("Research topic", placeholder="e.g. The impact of quantum computing on cryptography")
run_clicked = st.button("Run research", type="primary", disabled=not topic.strip())

if run_clicked:
    topic = topic.strip()
    state = {}
    try:
        with st.status("Step 1/4 — Search agent is searching the web...", expanded=True) as status:
            search_agent = build_search_agent()
            search_result = search_agent.invoke({
                "messages": [("user", f"Find recent, reliable and detailed information about: {topic}")]
            })
            state["search_results"] = search_result["messages"][-1].content
            status.update(label="Step 1/4 — Search complete", state="complete")

        with st.status("Step 2/4 — Reader agent is scraping the top source...", expanded=True) as status:
            reader_agent = build_reader_agent()
            reader_result = reader_agent.invoke({
                "messages": [("user",
                    f"Based on the following search results about '{topic}', "
                    f"pick the most relevant URL and scrape it for deeper content.\n\n"
                    f"Search Results:\n{state['search_results'][:800]}"
                )]
            })
            state["scraped_content"] = reader_result["messages"][-1].content
            status.update(label="Step 2/4 — Scraping complete", state="complete")

        with st.status("Step 3/4 — Writer is drafting the report...", expanded=True) as status:
            research_combined = (
                f"SEARCH RESULTS:\n{state['search_results']}\n\n"
                f"DETAILED SCRAPED CONTENT:\n{state['scraped_content']}"
            )
            state["report"] = writer_chain.invoke({"topic": topic, "research": research_combined})
            status.update(label="Step 3/4 — Report drafted", state="complete")

        with st.status("Step 4/4 — Critic is reviewing the report...", expanded=True) as status:
            state["feedback"] = critic_chain.invoke({"report": state["report"]})
            status.update(label="Step 4/4 — Review complete", state="complete")

        state["topic"] = topic
        st.session_state.state = state
        st.session_state.history.append(topic)
        st.success("Research pipeline finished.")

    except Exception as e:
        st.error(f"Pipeline failed: {e}")

state = st.session_state.state
if state:
    st.divider()
    report_tab, critique_tab, sources_tab = st.tabs(["📄 Report", "🧐 Critic Feedback", "🔍 Raw Research"])

    with report_tab:
        st.markdown(f"### Research Report: {state['topic']}")
        st.markdown(state["report"])
        st.download_button(
            "Download report (.md)",
            data=state["report"],
            file_name=f"{state['topic'].replace(' ', '_')}_report.md",
            mime="text/markdown",
        )

    with critique_tab:
        st.markdown(state["feedback"])

    with sources_tab:
        st.markdown("**Search results**")
        st.text(state["search_results"])
        st.markdown("**Scraped content**")
        st.text(state["scraped_content"])