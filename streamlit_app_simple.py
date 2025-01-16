import streamlit as st
    from agents.director_agent import BlogRequest, DirectorDependencies
    import asyncio

    st.title("Auto-Blogging Platform (WebContainer Demo)")

    # Simplified UI
    topic = st.text_input("Enter blog topic:", "AI in Healthcare")
    if st.button("Generate Content"):
        with st.spinner("Creating content..."):
            try:
                # Create test request
                request = BlogRequest(
                    user_id="webcontainer_user",
                    topic=topic,
                    keywords=["AI", "healthcare"],
                    content_type="blog post",
                    publish=False
                )

                # Create test dependencies
                deps = DirectorDependencies(
                    supabase_url="test_url",
                    supabase_key="test_key"
                )

                # Simulate result
                st.success("Demo content created successfully!")
                st.json({
                    "status": "success",
                    "message": "This is a demo result",
                    "content": {
                        "title": f"Exploring {topic}",
                        "sections": [
                            "Introduction to the topic",
                            "Current trends and developments",
                            "Future outlook"
                        ]
                    }
                })

            except Exception as e:
                st.error(f"Error: {str(e)}")
