import openai
import time

# Set up your OpenAI API key here
openai.api_key = 'your-api-key-here'  # Replace with your OpenAI API key

def slow_print(text, delay=0.05):
    """
    Print text slowly, simulating an immersive game narrative.
    """
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def get_ai_response(prompt):
    """
    Get a response from the GPT-3 model based on the provided prompt.
    """
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",  # Use the appropriate engine, GPT-3 model
            prompt=prompt,
            max_tokens=300,  # Maximum number of tokens to generate
            temperature=0.7,  # Controls creativity (0.0 to 1.0)
            top_p=1,  # Use the top-p sampling method
            frequency_penalty=0,  # Discourages repetition
            presence_penalty=0.6,  # Discourages repetition of ideas
            stop=["\n"]
        )
        return response.choices[0].text.strip()
    except Exception as e:
        print(f"Error with OpenAI API: {e}")
        return None

def start_game():
    """
    Start the game and interact with the player.
    """
    slow_print("Welcome to AI Dungeon! You are about to embark on an incredible adventure!")
    slow_print("Your journey begins now...\n")
    
    player_name = input("What is your name, adventurer? ")
    slow_print(f"Ah, {player_name}, a brave soul ready for the unknown.\n")

    story_prompt = f"You are {player_name}, a brave adventurer in a vast and magical world. The journey ahead is filled with mysteries and challenges. What will you do first?"

    while True:
        # Get AI's response based on the current prompt
        ai_response = get_ai_response(story_prompt)
        if ai_response:
            slow_print(ai_response)

        # Get player's input to continue the story
        player_action = input("\nWhat will you do next? ")
        if player_action.lower() == 'quit':
            slow_print("You have decided to end your journey. Thank you for playing!")
            break

        # Update the prompt to include the player's action
        story_prompt += f"\nThe player decides to: {player_action}. The adventure continues..."

def main():
    """
    Main function to start the game.
    """
    start_game()

if __name__ == "__main__":
    main()
