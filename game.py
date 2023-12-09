import spacy
import time

# Download spaCy model
nlp = spacy.load("en_core_web_sm")

class Player:
    def __init__(self):
        self.inventory = []
        self.emotion = 0
        self.quest_progress = 0

    def add_to_inventory(self, item):
        self.inventory.append(item)

class StorytellingGame:
    def __init__(self):
        self.story = []
        self.current_state = 0
        self.player = Player()

    def add_state(self, text, options, quest=None, effects=None):
        self.story.append({"text": text, "options": options, "quest": quest, "effects": effects})

    def display_current_state(self):
        print(self.story[self.current_state]["text"])
        print("Options:")
        for idx, option in enumerate(self.story[self.current_state]["options"], start=1):
            print(f"{idx}. {option}")

    def get_user_input(self):
        choice = input("Enter the number of your choice: ")
        return int(choice) - 1

    def analyze_user_input(self, user_input):
        # Use spaCy for advanced NLP analysis
        doc = nlp(user_input)
        for token in doc:
            print(f"Token: {token.text}, POS: {token.pos_}, NE: {token.ent_type_}")

    def execute_effects(self, effects):
        # Apply effects to the player
        if effects:
            for effect, value in effects.items():
                if effect == "add_to_inventory":
                    self.player.add_to_inventory(value)
                elif effect == "increase_emotion":
                    self.player.emotion += value
                elif effect == "advance_quest":
                    self.player.quest_progress += value

    def play_game(self):
        while self.current_state < len(self.story):
            state = self.story[self.current_state]
            self.display_current_state()
            user_choice = self.get_user_input()

            if 0 <= user_choice < len(state["options"]):
                user_input = state["options"][user_choice]
                self.analyze_user_input(user_input)
                self.execute_effects(state.get("effects"))

                # Check for quest progression
                if state.get("quest") and self.player.quest_progress >= state["quest"]["required_progress"]:
                    print("Quest completed! You gain additional benefits.")
                    self.execute_effects(state["quest"].get("completion_effects"))

                self.current_state += 1
            else:
                print("Invalid choice. Please choose a valid option.")

        print("Congratulations! You've completed the game.")
        time.sleep(1)
        print("Let's see how you did...")

        time.sleep(2)
        print(f"\nFinal Emotion Score: {self.player.emotion}")
        print("Final Inventory:", self.player.inventory)

# Example usage:
game = StorytellingGame()

# Define the story states with quests and effects, adding a touch of humor
game.add_state("You wake up in a land of talking llamas. They seem friendly.", ["Talk to the llamas", "Run away"])
game.add_state("The llamas tell you about a magical taco that grants wishes.", ["Search for the magical taco", "Ask for more llama wisdom"],
              quest={"required_progress": 1, "completion_effects": {"increase_emotion": 5}})
game.add_state("You find a taco stand run by a wizard llama. He demands a joke for a magical taco.", ["Tell a joke", "Decline and buy a regular taco"])
game.add_state("Your joke makes the wizard llama laugh. He rewards you with the magical taco.", ["Eat the magical taco", "Save it for later"],
              effects={"add_to_inventory": "Magical Taco"})
game.add_state("The magical taco grants your wish! You can now speak llama.", ["Converse with llamas", "Use your new skill to become a llama ambassador"],
              quest={"required_progress": 3, "completion_effects": {"increase_emotion": 10}})
game.add_state("As the llama ambassador, you negotiate peace between llamas and humans. The llamas throw a party in your honor!", ["Celebrate with the llamas", "Decline and go on a solo adventure"])

# Play the game
game.play_game()
