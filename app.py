from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import os
from datetime import datetime
from dotenv import load_dotenv
from groq import Groq
from models import db, User

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stories.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Create database tables
with app.app_context():
    db.create_all()


class GroqStoryGenerator:
    def __init__(self):
        # Get the API key from environment variable
        self.api_key = os.getenv("GROQ_API_KEY")
        self.client = None
        if self.api_key:
            self.client = Groq(api_key=self.api_key)

    def generate_story(self, prompt, max_tokens=1000, temperature=0.8, language='english'):
        """
        Generate a story using the GROQ API
        """
        if not self.api_key:
            # If no API key is provided, return a mock response for demonstration
            return f"Once upon a time, in a land far away, there was a story about: {prompt}. The end."

        # Language-specific instructions
        language_instruction = {
            'english': 'in English',
            'swahili': 'in Swahili language',
            'chichewa': 'in Chichewa language',
            'zulu': 'in Zulu language',
            'yao': 'in Yao language',
            'french': 'in French language',
            'portuguese': 'in Portuguese language',
            'kinyarwanda': 'in Kinyarwanda language'
        }

        selected_language = language_instruction.get(language, 'in English')

        # System instruction for the model
        system_content = (
            "You are an expert storyteller with exceptional skill in crafting rich, immersive narratives. "
            f"Generate a full, complete story {selected_language} with significant depth and detail based on the user's prompt. "
            "Create fully developed characters with distinct personalities, motivations, and backgrounds. "
            "Build a compelling plot with a clear beginning, middle, and end, including rising action, climax, and resolution. "
            "Use vivid, descriptive language to paint detailed scenes and settings that engage all the senses. "
            "Ensure the story has substantial length and complexity - aim for a minimum of 500 words for shorter requests, "
            "and up to 1500 words for longer requests. "
            "Vary your narrative style - use omniscient, first person, or second person perspective as appropriate. "
            "Include dialogue, internal thoughts, and detailed descriptions of emotions and environments. "
            "Make the story immersive, with unexpected plot developments, character growth, and thematic depth. "
            "The story should be appropriate for a general audience but rich enough for adults. "
            f"Don't end abruptly - develop the narrative fully to the requested length."
        )

        user_content = (
            f"Write a comprehensive, engaging story based on this prompt: '{prompt}'. "
            f"Create a full narrative with rich characters, vivid descriptions, and a complete plot arc. "
            f"The story must be written {selected_language}."
        )

        try:
            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": system_content},
                    {"role": "user", "content": user_content}
                ],
                max_tokens=max_tokens,
                temperature=temperature,
                top_p=0.9
            )

            # Handle response format for GROQ API
            if response.choices and len(response.choices) > 0:
                return response.choices[0].message.content
            else:
                return 'Story generation failed: No content found in response.'

        except Exception as e:
            return f"Error generating story: {str(e)}"


# Initialize the generator
generator = GroqStoryGenerator()


# ============== Authentication Routes ==============

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('generate_story_page'))
    
    if request.method == 'GET':
        return render_template('login.html')
    
    # Handle POST request for login
    data = request.get_json()
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')
    
    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400
    
    user = User.query.filter_by(email=email).first()
    
    if user and user.check_password(password):
        login_user(user)
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'error': 'Invalid email or password'}), 401


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('generate_story_page'))
    
    if request.method == 'GET':
        return render_template('register.html')
    
    # Handle POST request for registration
    data = request.get_json()
    username = data.get('username', '').strip()
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')
    
    # Validation
    if not username or not email or not password:
        return jsonify({'error': 'Username, email, and password are required'}), 400
    
    if len(username) < 3:
        return jsonify({'error': 'Username must be at least 3 characters'}), 400
    
    if len(password) < 6:
        return jsonify({'error': 'Password must be at least 6 characters'}), 400
    
    # Check if user already exists
    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already taken'}), 409
    
    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already registered'}), 409
    
    # Create new user
    user = User(username=username, email=email)
    user.set_password(password)
    
    try:
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'Registration successful'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'An error occurred. Please try again.'}), 500


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


# ============== Main Application Routes ==============

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('generate_story_page'))
    return redirect(url_for('login'))


@app.route('/generate')
@login_required
def generate_story_page():
    return render_template('index.html', user=current_user)


@app.route('/generate', methods=['POST'])
@login_required
def generate():
    data = request.get_json()
    prompt = data.get('prompt', '').strip()

    # Validate the prompt
    if not prompt:
        return jsonify({'error': 'Prompt is required'}), 400

    # Optional parameters
    max_tokens = data.get('max_tokens', 1000)
    temperature = data.get('temperature', 0.8)
    language = data.get('language', 'english').lower()

    # Validate parameters
    if max_tokens < 100 or max_tokens > 2000:
        max_tokens = 1000  # Set to default if out of range
    if temperature < 0.0 or temperature > 1.0:
        temperature = 0.8  # Set to default if out of range

    story = generator.generate_story(prompt, max_tokens, temperature, language)
    
    # Increment user's story count
    current_user.increment_stories_count()
    
    return jsonify({'story': story})


@app.route('/random_prompt', methods=['GET'])
@login_required
def random_prompt():
    """
    Generate a random story prompt for users who need inspiration
    """
    try:
        from prompt_generator import StoryPromptGenerator
        prompt_generator = StoryPromptGenerator()
        random_prompt = prompt_generator.generate_random_prompt()
        return jsonify({'prompt': random_prompt})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/profile')
@login_required
def profile():
    """User profile page showing stats"""
    return jsonify({
        'username': current_user.username,
        'email': current_user.email,
        'stories_generated': current_user.stories_generated,
        'member_since': current_user.created_at.strftime('%B %d, %Y')
    })


if __name__ == '__main__':
    # Use port from environment variable or default to 5000
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
