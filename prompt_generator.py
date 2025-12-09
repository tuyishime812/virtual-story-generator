import random

class StoryPromptGenerator:
    """
    Generates random story prompts to inspire creativity
    """
    
    def __init__(self):
        self.characters = [
            "A brave knight", "A mysterious wizard", "A curious child", 
            "An old hermit", "A young artist", "A traveling merchant", 
            "A reformed thief", "A lonely lighthouse keeper", 
            "A talking animal", "A time traveler", "A space explorer", 
            "A ghost", "A robot", "A fairy", "A dragon", 
            "A pirate captain", "A detective", "A chef", 
            "A musician", "A farmer", "A scientist", "A teacher"
        ]
        
        self.verbs = [
            "discovers", "finds", "stumbles upon", "uncovers", 
            "encounters", "meets", "betrays", "rescues", 
            "challenges", "befriends", "duels", "escapes from",
            "investigates", "creates", "destroys", "learns about",
            "is haunted by", "travels to", "accidentally", "must find"
        ]
        
        self.objects = [
            "a magical artifact", "an ancient map", "a hidden treasure", 
            "a secret door", "a mysterious letter", "a forgotten spell", 
            "a powerful weapon", "a cursed object", "an enchanted forest", 
            "a parallel universe", "a time portal", "a secret society", 
            "an abandoned castle", "a hidden city", "a magical creature", 
            "a lost civilization", "a prophecy", "a dangerous secret",
            "a family heirloom", "a strange device", "a cryptic message"
        ]
        
        self.settings = [
            "in a bustling city", "in a remote village", "in a haunted mansion", 
            "in an enchanted forest", "in a distant galaxy", "in a post-apocalyptic world", 
            "underwater", "in a magical kingdom", "in the Wild West", 
            "during medieval times", "in ancient Egypt", "in a futuristic city", 
            "on a mysterious island", "in the Arctic", "in a volcano", 
            "in the clouds", "in a dream world", "in the underworld", 
            "on a spaceship", "in a parallel dimension", "during a festival"
        ]
    
    def generate_random_prompt(self):
        """
        Generate a random story prompt combining character, verb, object, and setting
        """
        character = random.choice(self.characters)
        verb = random.choice(self.verbs)
        obj = random.choice(self.objects)
        setting = random.choice(self.settings)
        
        prompt = f"{character} {verb} {obj} {setting}."
        return prompt
    
    def get_themed_prompts(self, theme=None):
        """
        Get some themed prompts based on common themes
        """
        themes = {
            "fantasy": [
                "A young wizard discovers an ancient spell hidden in their grandmother's attic",
                "A dragon and a knight must work together to save their kingdoms",
                "An enchanted forest is dying, and only a bard's song can save it"
            ],
            "sci-fi": [
                "A space explorer finds an abandoned ship with a single survivor who claims to be from Earth",
                "A robot develops emotions and questions its purpose in human society",
                "Time travelers accidentally change history in a subtle but devastating way"
            ],
            "mystery": [
                "A detective realizes the victim in their case is someone they know personally",
                "A person receives a letter from their future self warning of danger",
                "A small town loses a day of time, but only one person remembers"
            ],
            "adventure": [
                "A treasure hunter finds a map to their own location",
                "A mountain climber discovers a path that leads to impossible places",
                "A shipwreck survivor finds they're not alone on the island"
            ]
        }
        
        if theme and theme in themes:
            return random.choice(themes[theme])
        else:
            # Return a random prompt from any theme
            all_prompts = []
            for theme_prompts in themes.values():
                all_prompts.extend(theme_prompts)
            return random.choice(all_prompts)

if __name__ == "__main__":
    generator = StoryPromptGenerator()
    
    print("Random Story Prompts:")
    print("-" * 30)
    
    for i in range(5):
        print(f"{i+1}. {generator.generate_random_prompt()}")
    
    print("\nThemed Prompts:")
    print("-" * 30)
    
    for theme in ["fantasy", "sci-fi", "mystery", "adventure"]:
        print(f"{theme.capitalize()}: {generator.get_themed_prompts(theme)}")