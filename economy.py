# economy.py
import json
import os
import time
from profile import load_profiles, save_profiles

DATA_DIR = "data"
LEADERBOARD_FILE = os.path.join(DATA_DIR, "leaderboards.json")

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

if not os.path.exists(LEADERBOARD_FILE):
    with open(LEADERBOARD_FILE, "w") as f:
        json.dump({}, f)

# --- XP & Gold System ---
def add_rewards(uid, mode, difficulty, survive_time, accuracy):
    """
    Adds XP and Gold based on performance
    """
    profiles = load_profiles()
    if uid not in profiles:
        return

    base_xp = 10
    base_gold = 5

    diff_multiplier = {"Easy":1, "Normal":1.5, "Hard":2, "Hell":3}.get(difficulty,1)
    mode_multiplier = {"Default":1, "Teleportation":2, "Spinning":2}.get(mode,1)

    xp_gain = int(base_xp * diff_multiplier * mode_multiplier * (survive_time/60))
    gold_gain = int(base_gold * diff_multiplier * mode_multiplier * (survive_time/60))

    profiles[uid]["xp"] += xp_gain
    profiles[uid]["gold"] = profiles[uid].get("gold",0) + gold_gain

    # Level up if XP threshold crossed
    while profiles[uid]["xp"] >= profiles[uid]["level"] * 100:
        profiles[uid]["xp"] -= profiles[uid]["level"] * 100
        profiles[uid]["level"] += 1

    save_profiles(profiles)
    return xp_gain, gold_gain

# --- Skills ---
SKILLS = {
    "slow_ball": {"price":15, "cooldown":10, "active":False},
    "protection": {"price":30, "cooldown":30, "active":False}
}

def buy_skill(uid, skill_name):
    profiles = load_profiles()
    if uid not in profiles:
        return False, "Profile not found"

    if skill_name not in SKILLS:
        return False, "Skill not found"

    gold = profiles[uid].get("gold",0)
    price = SKILLS[skill_name]["price"]

    if gold >= price:
        profiles[uid]["gold"] -= price
        profiles[uid].setdefault("skills", {})[skill_name] = True
        save_profiles(profiles)
        return True, f"{skill_name} purchased!"
    return False, "Not enough gold"

def check_skill(uid, skill_name):
    profiles = load_profiles()
    return profiles.get(uid, {}).get("skills", {}).get(skill_name, False)

# --- Leaderboard ---
def update_leaderboard(uid, mode, survive_time):
    """
    Saves best survive_time per mode
    """
    with open(LEADERBOARD_FILE, "r") as f:
        boards = json.load(f)

    boards.setdefault(mode, {})
    boards[mode][uid] = max(survive_time, boards[mode].get(uid,0))

    with open(LEADERBOARD_FILE, "w") as f:
        json.dump(boards, f, indent=4)

def get_leaderboard(mode):
    with open(LEADERBOARD_FILE, "r") as f:
        boards = json.load(f)
    mode_board = boards.get(mode,{})
    sorted_board = sorted(mode_board.items(), key=lambda x:x[1], reverse=True)
    return sorted_board

# --- Timer system ---
def start_timer():
    return time.time()

def end_timer(start_time):
    return int(time.time() - start_time)