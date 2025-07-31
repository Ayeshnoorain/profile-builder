import json
from datetime import datetime
from typing import Dict, List
from config import Config

# Add OpenAI import
try:
    import openai
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    print("Warning: OpenAI package not installed. Install with: pip install openai")

class ProfileGenerator:
    """Generates professional Upwork profiles from GitHub data"""
    
    def __init__(self):
        self.language_categories = {
            'Programming Languages': ['Python', 'JavaScript', 'TypeScript', 'Java', 'C#', 'C++', 'C', 'Go', 'Rust', 'PHP', 'Ruby', 'Swift', 'Kotlin'],
            'Frontend': ['HTML', 'CSS', 'React', 'Vue', 'Angular', 'Svelte', 'Bootstrap', 'Tailwind', 'Sass', 'Less'],
            'Backend': ['Node.js', 'Express', 'Django', 'Flask', 'FastAPI', 'Spring', 'ASP.NET', 'Laravel', 'Rails'],
            'Database': ['PostgreSQL', 'MySQL', 'MongoDB', 'Redis', 'SQLite', 'Oracle', 'SQL Server'],
            'DevOps': ['Docker', 'Kubernetes', 'AWS', 'Azure', 'GCP', 'Heroku', 'Netlify', 'CI/CD', 'Git'],
            'Tools': ['Git', 'Docker', 'VS Code', 'IntelliJ', 'Postman', 'Jira', 'Slack']
        }
        self.openai_client = None
        if OPENAI_AVAILABLE and Config.OPENAI_API_KEY:
            self.openai_client = OpenAI(api_key=Config.OPENAI_API_KEY)
    
    def generate_profile(self, user_info: Dict, repos: List[Dict], analysis: Dict) -> Dict:
        """Generate complete profile content"""
        return {
            'title': self._generate_title(user_info, analysis),
            'overview': self._generate_overview(user_info, repos, analysis),
            'skills': self._generate_skills(analysis),
            'portfolio_projects': self._generate_portfolio_projects(repos, analysis),
            'transcription': self._generate_transcription(user_info, repos, analysis)
        }
    
    def _generate_title(self, user_info: Dict, analysis: Dict) -> str:
        """Generate professional profile title"""
        # Get top languages
        top_languages = sorted(analysis.get('languages', {}).items(), 
                             key=lambda x: x[1], reverse=True)[:3]
        
        if not top_languages:
            return "Software Developer"
        
        # Create title based on primary skills
        primary_lang = top_languages[0][0]
        
        # Determine role based on project types
        project_types = analysis.get('project_types', [])
        if 'Web Application' in project_types:
            role = "Full Stack Developer"
        elif 'API/Backend' in project_types:
            role = "Backend Developer"
        elif 'Mobile Application' in project_types:
            role = "Mobile Developer"
        elif 'Data Science' in project_types:
            role = "Data Scientist"
        else:
            role = "Software Developer"
        
        # Build title with top languages
        languages = [lang[0] for lang in top_languages[:2]]
        title = f"{role} | {' | '.join(languages)}"
        
        return title
    
    def _generate_overview(self, user_info: Dict, repos: List[Dict], analysis: Dict) -> str:
        """Generate professional overview section"""
        # Calculate experience years
        years_experience = 0
        if user_info.get('created_at'):
            try:
                # Handle GitHub's ISO format with 'Z' timezone
                created_at_str = user_info['created_at']
                if created_at_str.endswith('Z'):
                    created_at_str = created_at_str[:-1] + '+00:00'
                
                join_date = datetime.fromisoformat(created_at_str)
                years_experience = (datetime.now() - join_date).days // 365
            except Exception:
                # If date parsing fails, use 0 years
                years_experience = 0
        
        # Get project count and types
        total_projects = len(repos)
        project_types = analysis.get('project_types', [])
        unique_types = list(set(project_types))
        
        # Get top technologies
        technologies = analysis.get('technologies', [])
        top_techs = technologies[:5] if technologies else []
        
        # Build overview
        overview_parts = []
        
        # Introduction
        if user_info.get('name'):
            overview_parts.append(f"I'm {user_info['name']}, a passionate software developer")
        else:
            overview_parts.append("I'm a passionate software developer")
        
        # Experience
        if years_experience > 0:
            overview_parts.append(f"with {years_experience} years of experience")
        
        # Specialization
        if unique_types:
            if len(unique_types) == 1:
                overview_parts.append(f"specializing in {unique_types[0].lower()} development")
            else:
                overview_parts.append(f"specializing in {', '.join(unique_types[:-1]).lower()} and {unique_types[-1].lower()} development")
        
        # Technologies
        if top_techs:
            overview_parts.append(f"using modern technologies like {', '.join(top_techs)}")
        
        # Project count
        if total_projects > 0:
            overview_parts.append(f"I've successfully delivered {total_projects} projects")
        
        # Value proposition
        overview_parts.append("I'm committed to writing clean, maintainable code and delivering high-quality solutions that meet client requirements.")
        
        # Communication
        overview_parts.append("I believe in clear communication, timely delivery, and building long-term relationships with clients.")
        
        return " ".join(overview_parts)
    
    def _generate_skills(self, analysis: Dict) -> str:
        """Generate organized skills section"""
        skills_html = []
        
        # Get all languages and their counts
        languages = analysis.get('languages', {})
        technologies = set(analysis.get('technologies', []))
        
        # Organize skills by category
        categorized_skills = {}
        
        for lang, count in languages.items():
            category = self._categorize_language(lang)
            if category not in categorized_skills:
                categorized_skills[category] = []
            categorized_skills[category].append(lang)
        
        # Add technologies to appropriate categories
        for tech in technologies:
            category = self._categorize_technology(tech)
            if category not in categorized_skills:
                categorized_skills[category] = []
            if tech not in categorized_skills[category]:
                categorized_skills[category].append(tech)
        
        # Generate HTML for each category
        for category, skills in categorized_skills.items():
            if skills:
                skills_html.append(f"<strong>{category}:</strong> {', '.join(sorted(skills))}")
        
        return "<br>".join(skills_html)
    
    def _categorize_language(self, language: str) -> str:
        """Categorize programming language"""
        for category, langs in self.language_categories.items():
            if language in langs:
                return category
        return "Programming Languages"
    
    def _categorize_technology(self, technology: str) -> str:
        """Categorize technology"""
        tech_lower = technology.lower()
        
        if any(tech in tech_lower for tech in ['react', 'vue', 'angular', 'html', 'css', 'bootstrap']):
            return "Frontend"
        elif any(tech in tech_lower for tech in ['node', 'express', 'django', 'flask', 'spring']):
            return "Backend"
        elif any(tech in tech_lower for tech in ['postgres', 'mysql', 'mongo', 'redis']):
            return "Database"
        elif any(tech in tech_lower for tech in ['docker', 'kubernetes', 'aws', 'azure', 'heroku']):
            return "DevOps"
        else:
            return "Tools"
    
    def _generate_portfolio_projects(self, repos: List[Dict], analysis: Dict) -> str:
        """Generate portfolio projects section"""
        if not repos:
            return "No projects available"
        
        # Get top projects (by stars or recent activity)
        top_projects = analysis.get('top_projects', repos[:3])
        
        projects_html = []
        
        for i, repo in enumerate(top_projects[:3], 1):
            project_desc = self._generate_project_description(repo)
            projects_html.append(f"<strong>Project {i}:</strong> {project_desc}")
        
        return "<br>".join(projects_html)
    
    def _generate_project_description(self, repo: Dict) -> str:
        """Generate description for a single project"""
        name = repo['name']
        description = repo.get('description', '')
        language = repo.get('language', '')
        stars = repo.get('stars', 0)
        forks = repo.get('forks', 0)
        
        # Build description
        parts = []
        
        # Project name and type
        if description:
            parts.append(f"{name} - {description}")
        else:
            parts.append(name)
        
        # Technologies
        tech_parts = []
        if language:
            tech_parts.append(language)
        
        # Add other languages if available
        languages = repo.get('languages', {})
        if languages:
            other_langs = [lang for lang in languages.keys() if lang != language]
            if other_langs:
                tech_parts.extend(other_langs[:2])  # Limit to 2 additional languages
        
        if tech_parts:
            parts.append(f"({', '.join(tech_parts)})")
        
        # Stats (if significant)
        if stars > 0 or forks > 0:
            stats = []
            if stars > 0:
                stats.append(f"{stars} stars")
            if forks > 0:
                stats.append(f"{forks} forks")
            if stats:
                parts.append(f"[{', '.join(stats)}]")
        
        return " ".join(parts)
    
    def generate_skills_summary(self, analysis: Dict) -> str:
        """Generate a concise skills summary"""
        languages = analysis.get('languages', {})
        technologies = analysis.get('technologies', [])
        
        # Get top 5 languages
        top_languages = sorted(languages.items(), key=lambda x: x[1], reverse=True)[:5]
        lang_names = [lang[0] for lang in top_languages]
        
        # Get top technologies
        top_techs = technologies[:5] if technologies else []
        
        # Combine and format
        all_skills = lang_names + top_techs
        unique_skills = list(dict.fromkeys(all_skills))  # Remove duplicates while preserving order
        
        return ", ".join(unique_skills[:8])  # Limit to 8 skills
    
    def _generate_ai_transcription(self, user_info: Dict, repos: List[Dict], analysis: Dict) -> str:
        """Generate AI-powered transcription using OpenAI"""
        if not self.openai_client:
            # No fallback - require OpenAI to be available
            raise Exception("OpenAI client not available. Please set OPENAI_API_KEY environment variable.")
        
        try:
            # Prepare context for AI
            context = self._prepare_ai_context(user_info, repos, analysis)
            
            # Create the prompt with token limits
            prompt = f"""Generate a professional 2-minute self-introduction transcription for an Upwork profile. 

Context:
{context}

Requirements:
- Keep it under 200 words (approximately 2 minutes when spoken)
- Make it conversational and engaging
- Include key skills and notable projects
- End with enthusiasm about opportunities
- Make it sound natural and professional

Generate only the transcription text (no speaking tips or formatting):"""

            # Make API call with token limits
            response = self.openai_client.chat.completions.create(
                model=Config.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "You are a professional profile writer specializing in creating engaging self-introductions for freelancers."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,  # Limit to ~300 tokens for cost control
                temperature=0.7,  # Some creativity but not too random
                presence_penalty=0.1,  # Encourage mentioning key details
                frequency_penalty=0.1   # Reduce repetition
            )
            
            transcription = response.choices[0].message.content.strip()
            
            # Add speaking tips
            speaking_notes = [
                "💡 Speaking Tips:",
                "• Speak at a natural pace - this should take about 2 minutes",
                "• Pause briefly after each sentence for clarity",
                "• Emphasize your key skills and project achievements",
                "• End with enthusiasm about the opportunity"
            ]
            
            return f"{transcription}\n\n" + "\n".join(speaking_notes)
            
        except Exception as e:
            print(f"OpenAI API error: {e}")
            # No fallback - raise the error
            raise Exception(f"Failed to generate AI transcription: {str(e)}")
    
    def _prepare_ai_context(self, user_info: Dict, repos: List[Dict], analysis: Dict) -> str:
        """Prepare context data for AI prompt"""
        # Calculate experience years
        years_experience = 0
        if user_info.get('created_at'):
            try:
                created_at_str = user_info['created_at']
                if created_at_str.endswith('Z'):
                    created_at_str = created_at_str[:-1] + '+00:00'
                join_date = datetime.fromisoformat(created_at_str)
                years_experience = (datetime.now() - join_date).days // 365
            except Exception:
                years_experience = 0
        
        # Get key information
        name = user_info.get('name', 'Software Developer')
        username = user_info.get('username', '')
        total_projects = len(repos)
        
        # Get top skills
        languages = analysis.get('languages', {})
        top_languages = sorted(languages.items(), key=lambda x: x[1], reverse=True)[:3]
        lang_names = [lang[0] for lang in top_languages]
        
        # Get project types
        project_types = analysis.get('project_types', [])
        unique_types = list(set(project_types))
        
        # Get top projects
        top_projects = analysis.get('top_projects', repos[:2])
        
        context = f"""
Name: {name}
GitHub Username: {username}
Experience: {years_experience} years of coding
Total Projects: {total_projects}
Top Programming Languages: {', '.join(lang_names) if lang_names else 'Various'}
Project Types: {', '.join(unique_types) if unique_types else 'Various software projects'}
Notable Projects: {', '.join([p['name'] for p in top_projects[:2]]) if top_projects else 'Various projects'}
"""
        return context
    


    def _generate_transcription(self, user_info: Dict, repos: List[Dict], analysis: Dict) -> str:
        """Generate a 2-minute self-introduction transcription for recording"""
        # Try AI-powered transcription first, fallback to template-based
        return self._generate_ai_transcription(user_info, repos, analysis) 