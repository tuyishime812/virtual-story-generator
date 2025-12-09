# Test the random prompt functionality
from prompt_generator import StoryPromptGenerator

def test_random_prompts():
    generator = StoryPromptGenerator()
    
    print("Testing Random Prompt Generation:")
    print("-" * 40)
    
    # Generate several random prompts
    for i in range(5):
        prompt = generator.generate_random_prompt()
        print(f"{i+1}. {prompt}")
    
    print("\nTesting Themed Prompts:")
    print("-" * 40)
    
    themes = ["fantasy", "sci-fi", "mystery", "adventure"]
    for theme in themes:
        themed_prompt = generator.get_themed_prompts(theme)
        print(f"{theme.capitalize()}: {themed_prompt}")

if __name__ == "__main__":
    test_random_prompts()