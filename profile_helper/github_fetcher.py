import requests
import json
import time
from typing import List, Dict, Optional
from config import Config

class GitHubFetcher:
    """Fetches and analyzes GitHub repositories for profile generation"""
    
    def __init__(self, github_token: Optional[str] = None):
        self.token = github_token or Config.GITHUB_TOKEN
        self.base_url = Config.GITHUB_API_BASE_URL
        self.headers = {
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'Upwork-Assistant/1.0'
        }
        
        if self.token:
            self.headers['Authorization'] = f'token {self.token}'
        
        # Rate limiting
        self.last_request_time = 0
        self.min_request_interval = 0.1  # 100ms between requests
    
    def _rate_limit_request(self):
        """Ensure we don't exceed rate limits"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < self.min_request_interval:
            time.sleep(self.min_request_interval - time_since_last)
        
        self.last_request_time = time.time()
    
    def _make_request(self, url: str, params: Dict = None) -> requests.Response:
        """Make a rate-limited request with error handling"""
        self._rate_limit_request()
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            
            # Check for rate limiting
            if response.status_code == 403 and 'rate limit' in response.text.lower():
                raise Exception("GitHub API rate limit exceeded. Please add a GitHub token or wait an hour.")
            
            return response
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Network error: {str(e)}")
    
    def get_user_repos(self, username: str, max_repos: int = 10) -> List[Dict]:
        """Fetch user repositories from GitHub API"""
        try:
            # Use different endpoints based on authentication
            if self.token:
                # With token: get both public and private repos
                url = f"{self.base_url}/user/repos"
                params = {
                    'sort': 'updated',
                    'per_page': max_repos * 2,  # Get more to account for filtering
                    'type': 'owner'
                }
            else:
                # Without token: only public repos
                url = f"{self.base_url}/users/{username}/repos"
                params = {
                    'sort': 'updated',
                    'per_page': max_repos,
                    'type': 'owner'
                }
            
            response = self._make_request(url, params)
            response.raise_for_status()
            
            repos = response.json()
            
            # Filter out forks and get additional details
            filtered_repos = []
            for repo in repos:
                # When using token, filter by username to get only user's repos
                if self.token and repo['owner']['login'] != username:
                    continue
                    
                if not repo.get('fork', False):  # Skip forked repositories
                    repo_details = self._get_repo_details(repo)
                    filtered_repos.append(repo_details)
                    
                    if len(filtered_repos) >= max_repos:
                        break
            return filtered_repos
            
        except Exception as e:
            raise Exception(f"Failed to fetch GitHub repositories: {str(e)}")
    
    def _get_repo_details(self, repo: Dict) -> Dict:
        """Get detailed information about a repository"""
        try:
            # Get README content
            readme_content = self._get_readme_content(repo['owner']['login'], repo['name'])
            
            # Get languages used
            languages = self._get_repo_languages(repo['owner']['login'], repo['name'])
            
            return {
                'name': repo['name'],
                'full_name': repo['full_name'],
                'description': repo.get('description', ''),
                'html_url': repo['html_url'],
                'language': repo.get('language', ''),
                'languages': languages,
                'stars': repo.get('stargazers_count', 0),
                'forks': repo.get('forks_count', 0),
                'created_at': repo['created_at'],
                'updated_at': repo['updated_at'],
                'readme_content': readme_content,
                'topics': repo.get('topics', []),
                'size': repo.get('size', 0),
                'open_issues': repo.get('open_issues_count', 0),
                'private': repo.get('private', False)
            }
            
        except Exception as e:
            # Return basic info if detailed fetch fails
            return {
                'name': repo['name'],
                'full_name': repo['full_name'],
                'description': repo.get('description', ''),
                'html_url': repo['html_url'],
                'language': repo.get('language', ''),
                'languages': {},
                'stars': repo.get('stargazers_count', 0),
                'forks': repo.get('forks_count', 0),
                'created_at': repo['created_at'],
                'updated_at': repo['updated_at'],
                'readme_content': '',
                'topics': repo.get('topics', []),
                'size': repo.get('size', 0),
                'open_issues': repo.get('open_issues_count', 0)
            }
    
    def _get_readme_content(self, owner: str, repo: str) -> str:
        """Get README content from repository"""
        try:
            url = f"{self.base_url}/repos/{owner}/{repo}/readme"
            response = self._make_request(url)
            
            if response.status_code == 200:
                readme_data = response.json()
                import base64
                content = base64.b64decode(readme_data['content']).decode('utf-8')
                return content
            else:
                return ""
                
        except Exception:
            return ""
    
    def _get_repo_languages(self, owner: str, repo: str) -> Dict[str, int]:
        """Get programming languages used in repository"""
        try:
            url = f"{self.base_url}/repos/{owner}/{repo}/languages"
            response = self._make_request(url)
            
            if response.status_code == 200:
                return response.json()
            else:
                return {}
                
        except Exception:
            return {}
    
    def get_user_info(self, username: str) -> Dict:
        """Get basic user information"""
        try:
            # Always use the users/{username} endpoint for specific user info
            # The token will still be used for authentication if available
            url = f"{self.base_url}/users/{username}"
            
            response = self._make_request(url)
            response.raise_for_status()
            
            user_data = response.json()
            return {
                'username': user_data['login'],
                'name': user_data.get('name', ''),
                'bio': user_data.get('bio', ''),
                'location': user_data.get('location', ''),
                'public_repos': user_data.get('public_repos', 0),
                'followers': user_data.get('followers', 0),
                'following': user_data.get('following', 0),
                'created_at': user_data.get('created_at', ''),
                'avatar_url': user_data.get('avatar_url', '')
            }
            
        except Exception as e:
            raise Exception(f"Failed to fetch user information: {str(e)}")
    
    def analyze_repos(self, repos: List[Dict]) -> Dict:
        """Analyze repositories to extract skills and patterns"""
        analysis = {
            'languages': {},
            'technologies': set(),
            'project_types': [],
            'total_stars': 0,
            'total_forks': 0,
            'avg_repo_size': 0,
            'recent_projects': [],
            'top_projects': []
        }
        
        if not repos:
            return analysis
        
        # Analyze each repository
        for repo in repos:
            # Count languages
            if repo['language']:
                analysis['languages'][repo['language']] = analysis['languages'].get(repo['language'], 0) + 1
            
            # Add languages from detailed analysis
            for lang in repo['languages']:
                analysis['languages'][lang] = analysis['languages'].get(lang, 0) + repo['languages'][lang]
            
            # Extract technologies from topics and descriptions
            self._extract_technologies(repo, analysis['technologies'])
            
            # Categorize project type
            project_type = self._categorize_project(repo)
            if project_type:
                analysis['project_types'].append(project_type)
            
            # Sum up stats
            analysis['total_stars'] += repo['stars']
            analysis['total_forks'] += repo['forks']
        
        # Calculate averages
        analysis['avg_repo_size'] = sum(repo['size'] for repo in repos) / len(repos)
        
        # Get recent projects (last 6 months)
        from datetime import datetime, timedelta
        six_months_ago = datetime.now() - timedelta(days=180)
        
        analysis['recent_projects'] = []
        for repo in repos:
            try:
                # Handle GitHub's ISO format with 'Z' timezone
                updated_at_str = repo['updated_at']
                if updated_at_str.endswith('Z'):
                    updated_at_str = updated_at_str[:-1] + '+00:00'
                
                repo_date = datetime.fromisoformat(updated_at_str)
                if repo_date > six_months_ago:
                    analysis['recent_projects'].append(repo)
            except Exception:
                # Skip repos with invalid dates
                continue
        
        # Get top projects by stars
        analysis['top_projects'] = sorted(repos, key=lambda x: x['stars'], reverse=True)[:5]
        
        # Convert set to list for JSON serialization
        analysis['technologies'] = list(analysis['technologies'])
        
        return analysis
    
    def _extract_technologies(self, repo: Dict, technologies: set):
        """Extract technology names from repository data"""
        # From topics
        for topic in repo['topics']:
            technologies.add(topic.lower())
        
        # From description
        description = repo['description'].lower() if repo['description'] else ''
        common_techs = [
            'react', 'vue', 'angular', 'node.js', 'express', 'django', 'flask',
            'python', 'javascript', 'typescript', 'java', 'c#', 'php', 'ruby',
            'mongodb', 'postgresql', 'mysql', 'redis', 'docker', 'kubernetes',
            'aws', 'azure', 'gcp', 'firebase', 'heroku', 'netlify'
        ]
        
        for tech in common_techs:
            if tech in description:
                technologies.add(tech)
    
    def _categorize_project(self, repo: Dict) -> str:
        """Categorize project based on name, description, and topics"""
        name = repo['name'].lower()
        description = repo['description'].lower() if repo['description'] else ''
        topics = [topic.lower() for topic in repo['topics']]
        
        # Web applications
        if any(word in name or word in description for word in ['web', 'app', 'website', 'dashboard']):
            return 'Web Application'
        
        # API projects
        if any(word in name or word in description for word in ['api', 'backend', 'server']):
            return 'API/Backend'
        
        # Mobile apps
        if any(word in name or word in description for word in ['mobile', 'android', 'ios', 'react-native']):
            return 'Mobile Application'
        
        # Data science
        if any(word in name or word in description for word in ['ml', 'ai', 'data', 'analysis', 'jupyter']):
            return 'Data Science'
        
        # Tools/Utilities
        if any(word in name or word in description for word in ['tool', 'utility', 'cli', 'script']):
            return 'Tool/Utility'
        
        return 'Other' 