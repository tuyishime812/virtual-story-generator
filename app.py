from flask import Flask, render_template, request, jsonify
import os
import requests
import json
from datetime import datetime
from prompt_generator import StoryPromptGenerator

app = Flask(__name__)

class GeminiStoryGenerator:
    def __init__(self):
        # Get the API key from environment variable
        self.api_key = os.getenv("GEMINI_API_KEY")  # Using Google's Gemini API
        self.api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={self.api_key}"

    def generate_story(self, prompt, max_tokens=1000, temperature=0.8, language='english'):
        """
        Generate a story using the Gemini API
        """
        if not self.api_key:
            # If no API key is provided, return a mock response for demonstration
            return f"Once upon a time, in a land far away, there was a story about: {prompt}. The end."

        headers = {
            "Content-Type": "application/json"
        }

        # Language-specific instructions
        language_instruction = {
            'english': 'in English',
            'swahili': 'in Swahili language',
            'chichewa': 'in Chichewa language',
            'zulu': 'in Zulu language',
            'yao': 'in Yao language',
            'french': 'in French language',
            'portuguese': 'in Portuguese language',
            'tumbuka': 'in Tumbuka language',
            'kinyarwanda': 'in Kinyarwanda language'
        }

        selected_language = language_instruction.get(language, 'in English')

        # Prepare the content for the API call
        system_instruction = {
            "parts": [{
                "text": (
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
            }]
        }

        contents = {
            "parts": [{
                "text": f"Write a comprehensive, engaging story based on this prompt: '{prompt}'. "
                    f"Create a full narrative with rich characters, vivid descriptions, and a complete plot arc. "
                    f"The story must be written {selected_language}."
            }]
        }

        data = {
            "contents": [contents],
            "system_instruction": system_instruction,
            "generationConfig": {
                "temperature": temperature,  # Higher temperature for more creative output
                "maxOutputTokens": max_tokens,
                "topP": 0.9,
                "topK": 40
            }
        }

        try:
            response = requests.post(self.api_url, headers=headers, json=data)
            response.raise_for_status()

            result = response.json()

            # Handle response format for Gemini API
            if 'candidates' in result and len(result['candidates']) > 0:
                candidate = result['candidates'][0]
                if 'content' in candidate and 'parts' in candidate['content']:
                    parts = candidate['content']['parts']
                    if len(parts) > 0:
                        return parts[0].get('text', 'Story generation failed.')
                    else:
                        return 'Story generation failed: No content parts found.'
                else:
                    return 'Story generation failed: No content found in candidate.'
            elif 'error' in result:
                return f"Error from Gemini API: {result['error']['message']}"
            else:
                return f"Error: Unexpected response format - {result}"

        except requests.exceptions.RequestException as e:
            return f"Error connecting to Gemini API: {str(e)}"
        except KeyError as e:
            return f"Error parsing API response: {str(e)}"
        except Exception as e:
            return f"Error generating story: {str(e)}"

# Initialize the generator
generator = GeminiStoryGenerator()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
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
    return jsonify({'story': story})

@app.route('/random_prompt', methods=['GET'])
def random_prompt():
    """
    Generate a random story prompt for users who need inspiration
    """
    try:
        prompt_generator = StoryPromptGenerator()
        random_prompt = prompt_generator.generate_random_prompt()
        return jsonify({'prompt': random_prompt})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Use port from environment variable or default to 5000
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)