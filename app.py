from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
from config import Config
from profile_helper.github_fetcher import GitHubFetcher
from profile_helper.profile_generator import ProfileGenerator
import os
import requests

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass

@app.route('/')
def index():
    """Main landing page"""
    return render_template('index.html')

@app.route('/profile')
def profile_assistant():
    """Profile generator page"""
    return render_template('profile.html')

@app.route('/proposal')
def proposal_assistant():
    """Portfolio builder page"""
    return render_template('proposal.html')

@app.route('/api/profile/generate', methods=['POST'])
def generate_profile():
    """API endpoint for profile generation"""
    try:
        data = request.get_json()
        github_username = data.get('github_username')
        github_token = data.get('github_token')
        max_repos = int(data.get('max_repos', 10))
        
        if not github_username:
            return jsonify({'error': 'GitHub username is required'}), 400
        
        # Initialize GitHub fetcher and profile generator
        github_fetcher = GitHubFetcher(github_token)
        profile_generator = ProfileGenerator()
        
        # Fetch user information and repositories
        user_info = github_fetcher.get_user_info(github_username)
        repos = github_fetcher.get_user_repos(github_username, max_repos)
        
        if not repos:
            return jsonify({'error': 'No repositories found or unable to access repositories'}), 404
        
        # Analyze repositories
        analysis = github_fetcher.analyze_repos(repos)
        
        # Generate profile content
        profile_content = profile_generator.generate_profile(user_info, repos, analysis)
        
        return jsonify({
            'success': True,
            'profile': profile_content,
            'user_info': user_info,
            'analysis': {
                'total_repos': len(repos),
                'languages': analysis.get('languages', {}),
                'technologies': analysis.get('technologies', []),
                'project_types': analysis.get('project_types', [])
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/proposal/generate', methods=['POST'])
def generate_proposal():
    """API endpoint for proposal generation"""
    try:
        data = request.get_json()
        job_description = data.get('job_description')
        tone = data.get('tone', 'professional')
        
        if not job_description:
            return jsonify({'error': 'Job description is required'}), 400
        
        # TODO: Implement proposal generation logic
        # This will be implemented in Phase 3
        
        return jsonify({
            'message': 'Proposal generation endpoint ready',
            'tone': tone,
            'job_description_length': len(job_description)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'config_loaded': bool(app.config.get('SECRET_KEY')),
        'github_token_set': bool(app.config.get('GITHUB_TOKEN')),
        'openai_key_set': bool(app.config.get('OPENAI_API_KEY'))
    })

@app.route('/api/github/rate-limit')
def check_rate_limit():
    """Check GitHub API rate limit status"""
    try:
        github_token = app.config.get('GITHUB_TOKEN')
        headers = {
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'Upwork-Assistant/1.0'
        }
        
        if github_token:
            headers['Authorization'] = f'token {github_token}'
        
        response = requests.get('https://api.github.com/rate_limit', headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            core_limit = data.get('resources', {}).get('core', {})
            
            return jsonify({
                'limit': core_limit.get('limit', 0),
                'remaining': core_limit.get('remaining', 0),
                'reset_time': core_limit.get('reset', 0),
                'authenticated': bool(github_token)
            })
        else:
            return jsonify({'error': 'Could not check rate limit'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'], host='0.0.0.0', port=5001) 