"""
    Streamlit UI for testing the multi-agent system
    """
    import streamlit as st
    from pydantic_ai import RunContext
    from agents.director_agent import director_agent, BlogRequest, DirectorDependencies
    from config import settings
    import asyncio

    # Page configuration
    st.set_page_config(page_title="Auto-Blogging Platform", layout="wide")
    st.title("Auto-Blogging Platform")

    # Sidebar for user input
    with st.sidebar:
        st.header("Content Parameters")
        user_id = st.text_input("User ID", "user_123")
        topic = st.text_input("Topic", "AI in Healthcare")
        keywords = st.text_input("Keywords (comma separated)", "AI, healthcare, machine learning")
        content_type = st.selectbox("Content Type", ["blog post", "article", "white paper"])
        publish = st.checkbox("Publish Content", value=False)

    # Main content area
    if st.button("Generate Content"):
        with st.spinner("Creating your content..."):
            try:
                # Prepare dependencies
                deps = DirectorDependencies(
                    supabase_url=settings.SUPABASE_URL,
                    supabase_key=settings.SUPABASE_KEY,
                    wordpress_url=settings.WORDPRESS_URL,
                    wordpress_creds={
                        "username": settings.WORDPRESS_USERNAME,
                        "password": settings.WORDPRESS_PASSWORD
                    }
                )

                # Create request
                request = BlogRequest(
                    user_id=user_id,
                    topic=topic,
                    keywords=[k.strip() for k in keywords.split(",")],
                    content_type=content_type,
                    publish=publish
                )

                # Run the Director Agent
                result = asyncio.run(director_agent.run_sync(
                    f"Create content for: {topic}",
                    deps=deps,
                    params=request.dict()
                ))

                # Display results
                st.success("Content generated successfully!")
                st.subheader("Results")
                st.json(result.data.dict())

                if result.data.content_url:
                    st.markdown(f"**Published URL:** [{result.data.content_url}]({result.data.content_url})")

            except Exception as e:
                st.error(f"Error generating content: {str(e)}")
                st.json({"status": "error", "message": str(e)})

    # Future authentication note
    st.markdown("""
    ### Future Authentication
    To add user authentication:
    1. Use Supabase auth in the sidebar
    2. Store user session in st.session_state
    3. Pass auth token to agents via dependencies
    """)

    # Error handling reference
    st.markdown("""
    ### Error Handling
    The UI handles errors by:
    1. Catching exceptions with try/except
    2. Displaying structured error messages
    3. Following PydanticAI's error handling patterns
    """)
