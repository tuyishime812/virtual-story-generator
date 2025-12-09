# Simple test to verify the story generator functionality
from story_generator import VirtualStoryGenerator

def test_story_generation():
    """Test the story generation functionality"""
    print("Testing the Virtual Story Generator...")

    # Create an instance of the generator
    generator = VirtualStoryGenerator()

    # Test with a sample prompt
    test_prompt = "A brave knight encounters a mysterious dragon in a magical forest"

    print(f"\nUsing test prompt: {test_prompt}")
    print("Note: If no API key is set, a mock response will be shown.")

    story = generator.generate_story(test_prompt)

    print("\nGenerated story:")
    print("="*50)
    print(story)
    print("="*50)

    print("\nTest completed!")

if __name__ == "__main__":
    test_story_generation()