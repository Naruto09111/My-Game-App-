# hell_game.py

from aim_game_template import start_game_with_mode

def start_hell(user_profile):
    """
    Start the game in Hell difficulty
    """
    settings = {
        "difficulty": "Hell",
        "fall_speed": {"Easy":4, "Medium":7, "Hard":11, "Hell":18},
        "speed_delay": {"Easy":500, "Medium":250, "Hard":150, "Hell":70}
    }
    start_game_with_mode(user_profile, settings)

if __name__ == "__main__":
    dummy_user = {"username":"TestPlayer"}
    start_hell(dummy_user)