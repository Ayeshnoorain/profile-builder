# GitHub Profile Generator

A powerful Flask web application that automatically generates professional developer profiles and portfolios using GitHub data and AI-powered content generation.

## 🚀 Features

### Profile Generation
- **GitHub Integration**: Automatically fetches user repositories, languages, and project data
- **AI-Powered Transcription**: Generates personalized 2-minute self-introduction scripts using OpenAI
- **Professional Overview**: Creates compelling profile overviews based on actual project data
- **Skills Analysis**: Organizes and categorizes technical skills from GitHub repositories
- **Portfolio Projects**: Highlights notable projects with detailed descriptions
- **Private Repository Support**: Access private repositories with GitHub tokens

### Portfolio Generation (Coming Soon)
- AI-powered portfolio content generation based on project descriptions
- Multiple style options (professional, creative, minimalist)
- Customizable content length and presentation

## 🛠️ Technology Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **AI Integration**: OpenAI GPT-3.5-turbo
- **GitHub API**: RESTful API integration
- **Environment Management**: python-dotenv

## 📋 Prerequisites

- Python 3.8+
- GitHub account (for repository access)
- OpenAI API key (for AI-powered features)

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd github-profile-generator
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   
   **Option A (Recommended):** Copy `user_config.env` and add your actual API keys:
   ```bash
   cp user_config.env my_config.env
   # Edit my_config.env and add your actual API keys
   ```
   
   **Option B:** Create a `config.env` file in the project root:
   ```env
   # Flask Configuration
   SECRET_KEY=your-secret-key-here
   FLASK_DEBUG=True
   
   # OpenAI API Configuration
   OPENAI_API_KEY=your-openai-api-key-here
   OPENAI_MODEL=gpt-3.5-turbo
   
   # Application Settings
   MAX_REPOS_TO_FETCH=10
   MAX_PROPOSAL_LENGTH=2000
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Access the application**
   Open your browser and go to: `http://localhost:5001`

## 📖 Usage

### Profile Generation

1. **Navigate to Profile Generator**
   - Go to `http://localhost:5001/profile`

2. **Enter GitHub Information**
   - **GitHub Username**: Your GitHub username
   - **GitHub Token** (Optional): For access to private repositories
   - **Max Repositories**: Number of repositories to analyze (default: 10)

3. **Generate Profile**
   - Click "Generate Profile"
   - The system will analyze your GitHub repositories and generate:
     - Professional title
     - Overview section
     - Skills breakdown
     - Portfolio projects
     - AI-generated 2-minute self-introduction transcription

4. **Copy Content**
   - Use the "Copy All" button to copy all generated content
   - Or copy individual sections as needed

### GitHub Token Setup (Optional)

For access to private repositories:

1. **Create GitHub Token**
   - Go to GitHub Settings → Developer settings → Personal access tokens
   - Generate a new token with `repo` scope
   - Copy the token

2. **Use in Application**
   - Paste the token in the "GitHub Token" field
   - The system will now access both public and private repositories

## 🏗️ Project Structure

```
github-profile-generator/
├── app.py                      # Main Flask application
├── config.py                   # Configuration settings
├── config.env                  # Environment variables
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
├── profile_helper/             # Profile generation modules
│   ├── __init__.py
│   ├── github_fetcher.py      # GitHub API integration
│   └── profile_generator.py   # Profile content generation
├── proposal_helper/            # Portfolio generation modules (future)
├── templates/                  # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── profile.html
│   └── proposal.html
└── venv/                       # Virtual environment
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key for AI features | Required |
| `OPENAI_MODEL` | OpenAI model to use | `gpt-3.5-turbo` |
| `MAX_REPOS_TO_FETCH` | Maximum repositories to analyze | `10` |
| `MAX_PROPOSAL_LENGTH` | Maximum portfolio content length | `2000` |
| `SECRET_KEY` | Flask secret key | Auto-generated |
| `FLASK_DEBUG` | Enable debug mode | `True` |

## 🎯 Features in Detail

### GitHub Integration
- Fetches user information and repository data
- Analyzes programming languages and technologies
- Categorizes projects by type (Web App, API, Mobile, etc.)
- Supports both public and private repositories
- Implements rate limiting to respect GitHub API limits

### AI-Powered Transcription
- Generates natural, conversational self-introductions
- Includes speaking tips for recording
- Personalized based on actual GitHub data
- Optimized for 2-minute delivery
- Professional tone suitable for recruiters

### Skills Analysis
- Automatically categorizes skills by type:
  - Programming Languages
  - Frontend Technologies
  - Backend Frameworks
  - Databases
  - DevOps Tools
- Provides skill summaries and detailed breakdowns

## 🔒 Security

- Environment variables for sensitive data
- GitHub tokens are not stored permanently
- API keys are kept secure in environment files
- `.gitignore` prevents sensitive files from being committed

## 🚧 Future Enhancements

### Phase 2: Portfolio Generation
- AI-powered portfolio content generation
- Project description analysis
- Multiple style and presentation options
- Portfolio templates and customization

### Phase 3: Advanced Features
- User authentication and profiles
- Portfolio history and management
- Advanced analytics and insights
- Integration with portfolio platforms

### Phase 4: Enterprise Features
- Team collaboration tools
- Advanced portfolio analytics
- Custom branding options
- API endpoints for external integrations

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the GitHub repository
- Check the documentation in this README
- Review the code comments for implementation details

## 🎉 Acknowledgments

- OpenAI for AI-powered content generation
- GitHub for repository data access
- Flask community for the web framework
- Bootstrap for the responsive UI components 