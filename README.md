# Auto-Blogging Platform

    ## Overview
    The Auto-Blogging Platform is a multi-agent system built using PydanticAI, Supabase, and Streamlit. It automates content creation workflows, from research to publishing, using a combination of AI agents and external services.

    ## Features
    - **Multi-Agent Architecture**: Director Agent orchestrates Manager Agents and Sub-Agents
    - **Structured Content Creation**: Uses Pydantic models for consistent data structures
    - **Database Integration**: Stores content and settings in Supabase
    - **Web Interface**: Streamlit-based UI for easy interaction
    - **Extensible Design**: Modular architecture for adding new agents and tools

    ## Architecture
    ```
    .
    ├── agents/               # AI agents
    │   ├── director_agent.py
    │   ├── research_manager_agent.py
    │   ├── content_brief_manager_agent.py
    │   ├── content_drafter_agent.py
    │   └── content_writer_agent.py
    ├── tools/                # Integration tools
    │   ├── supabase_tools.py
    │   ├── web_search_tools.py
    │   └── publishing_tools.py
    ├── tests/                # Unit and integration tests
    │   ├── test_agents.py
    │   ├── test_supabase_tools.py
    │   └── test_error_handling.py
    ├── config.py             # Configuration settings
    ├── main.py               # Main application entry point
    ├── streamlit_app.py      # Streamlit UI
    └── requirements.txt      # Python dependencies
    ```

    ## Getting Started

    ### Prerequisites
    - Python 3.8+
    - Node.js (for WebContainer environment)
    - Supabase account
    - OpenAI API key

    ### Installation
    1. Clone the repository:
       ```bash
       git clone https://github.com/yourusername/auto-blogging-platform.git
       cd auto-blogging-platform
       ```

    2. Install dependencies:
       ```bash
       npm install
       ```

    3. Set up environment variables:
       ```bash
       cp .env.example .env
       # Edit .env with your credentials
       ```

    ### Running the Application
    Start the Streamlit UI:
    ```bash
    npm run start
    ```

    ### Testing
    Run unit tests:
    ```bash
    python -m unittest discover tests
    ```

    ## Configuration
    Edit `.env` file with your credentials:
    ```env
    SUPABASE_URL=your-supabase-url
    SUPABASE_KEY=your-supabase-key
    OPENAI_API_KEY=your-openai-key
    WORDPRESS_URL=your-wordpress-url
    WORDPRESS_USERNAME=your-username
    WORDPRESS_PASSWORD=your-password
    ```

    ## Usage
    1. Open the Streamlit UI in your browser
    2. Enter content parameters
    3. Click "Generate Content"
    4. View results and published content

    ## Testing Guidelines
    ### Unit Testing
    - Test each agent independently
    - Use mocks for external services
    - Verify input/output contracts

    ### Integration Testing
    - Test tool integrations
    - Verify database operations
    - Test API interactions

    ### Error Handling
    - Use ModelRetry for recoverable errors
    - Implement fallback logic
    - Test error scenarios

    ## Contributing
    1. Fork the repository
    2. Create a new branch
    3. Make your changes
    4. Submit a pull request

    ## License
    This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

    ## Acknowledgments
    - PydanticAI for the agent framework
    - Supabase for database services
    - Streamlit for the web interface
