import os
import json
from datetime import datetime
from groq import Groq


class VirtualStoryGenerator:
    def __init__(self):
        # Get the API key from environment variable
        self.api_key = os.getenv("GROQ_API_KEY")
        self.client = None
        if self.api_key:
            self.client = Groq(api_key=self.api_key)

    def generate_story(self, prompt, max_tokens=1000, temperature=0.8, language='english'):
        """
        Generate a story based on the given prompt using the GROQ API
        """
        if not self.api_key:
            # If no API key is provided, return a more detailed mock response for demonstration
            print("API key not found. Using mock response for demonstration.")
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

    def save_story(self, prompt, story, filename=None):
        """
        Save the generated story to a file
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"story_{timestamp}.txt"

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"Prompt: {prompt}\n")
            f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("-" * 50 + "\n")
            f.write(story)

        print(f"Story saved to {filename}")

    def run(self):
        """
        Main loop for the story generator application
        """
        print("Welcome to the Virtual Story Generator!")
        print("Enter a prompt to generate a story, or 'quit' to exit.\n")

        while True:
            prompt = input("Enter your story prompt: ")

            if prompt.lower() in ['quit', 'exit', 'q']:
                print("Thank you for using the Virtual Story Generator!")
                break

            if not prompt.strip():
                print("Please enter a valid prompt.\n")
                continue

            print("\nGenerating your story...")
            # For command-line version, we'll use English by default
            story = self.generate_story(prompt, language='english')
            print("\nYour generated story:\n")
            print(story)
            print("\n" + "="*50 + "\n")

            save = input("Would you like to save this story? (y/n): ")
            if save.lower() in ['y', 'yes']:
                self.save_story(prompt, story)
            print()


if __name__ == "__main__":
    generator = VirtualStoryGenerator()
    generator.run()
