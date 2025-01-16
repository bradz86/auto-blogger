"""
    Unit tests for agents
    """
    import unittest
    from unittest.mock import AsyncMock, patch
    from agents.director_agent import director_agent, BlogRequest, DirectorDependencies
    from agents.research_manager_agent import research_manager, ResearchRequest, ResearchDependencies

    class TestAgents(unittest.IsolatedAsyncioTestCase):
        async def test_director_agent_basic(self):
            """Test Director Agent with basic input"""
            test_request = BlogRequest(
                user_id="test_user",
                topic="Test Topic",
                keywords=["test"],
                content_type="blog post",
                publish=False
            )

            test_deps = DirectorDependencies(
                supabase_url="test_url",
                supabase_key="test_key"
            )

            # Mock the agent's run method
            with patch.object(director_agent, 'run', new_callable=AsyncMock) as mock_run:
                mock_run.return_value.data = {
                    "status": "success",
                    "message": "Test message"
                }

                result = await director_agent.run_sync(
                    "Test prompt",
                    deps=test_deps,
                    params=test_request.dict()
                )

                self.assertEqual(result.data["status"], "success")
                mock_run.assert_called_once()

        async def test_research_manager_with_fallback(self):
            """Test Research Manager with API fallback"""
            test_request = ResearchRequest(
                topic="Test Topic",
                keywords=["test"]
            )

            test_deps = ResearchDependencies(
                web_search_api_key=None,  # Force fallback
                supabase_url="test_url",
                supabase_key="test_key"
            )

            result = await research_manager.run_sync(
                "Test research",
                deps=test_deps,
                params=test_request.dict()
            )

            self.assertIn("results", result.data)
            self.assertTrue(len(result.data["results"]) > 0)

    if __name__ == "__main__":
        unittest.main()
