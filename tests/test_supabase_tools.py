"""
    Integration tests for Supabase Tools
    """
    import unittest
    from unittest.mock import AsyncMock, patch
    from tools.supabase_tools import save_blog_post, BlogPost
    from pydantic_ai import RunContext

    class TestSupabaseTools(unittest.IsolatedAsyncioTestCase):
        async def test_save_blog_post(self):
            """Test saving blog post to Supabase"""
            test_post = BlogPost(
                title="Test Post",
                content="Test content",
                author="Test Author",
                tags=["test"]
            )

            test_deps = RunContext(deps={
                "url": "test_url",
                "key": "test_key"
            })

            # Mock Supabase client
            with patch('supabase.create_client', new_callable=AsyncMock) as mock_client:
                mock_instance = AsyncMock()
                mock_instance.table().insert().execute.return_value = {
                    "data": [{"id": "test_id"}]
                }
                mock_client.return_value = mock_instance

                result = await save_blog_post(test_deps, test_post)

                self.assertEqual(result["status"], "success")
                self.assertIn("id", result)

    if __name__ == "__main__":
        unittest.main()
