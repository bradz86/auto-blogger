import streamlit as st
    from agents.director import director_agent, BlogOutline
    from agents.manager import research_agent
    from agents.sub_agents import drafting_agent
    from db import save_blog_post

    st.title("Auto-Blogging Platform")

    topic = st.text_input("Enter blog topic:")
    if topic:
        outline = director_agent.run_sync(f"Create outline for: {topic}")
        research = research_agent.run_sync(f"Research: {topic}")
        draft = drafting_agent.run_sync(f"Write blog post about: {topic}")

        st.write("## Blog Outline")
        st.json(outline.data.dict())

        st.write("## Research Data")
        st.json(research.data.dict())

        st.write("## Draft Content")
        st.json(draft.data.dict())

        if st.button("Publish"):
            save_blog_post({
                "title": outline.data.title,
                "content": draft.data.dict(),
                "research": research.data.dict()
            })
            st.success("Blog post published!")
