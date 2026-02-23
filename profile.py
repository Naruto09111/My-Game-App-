# profile.py

import json
import os
import random
import string
import re


# -------- PATH --------

DATA_DIR = "data"
PROFILE_FILE = os.path.join(DATA_DIR, "profiles.json")


# -------- CREATE FOLDER --------

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)


# -------- CREATE FILE --------

if not os.path.exists(PROFILE_FILE):
    with open(PROFILE_FILE, "w") as f:
        json.dump({}, f)


# -------- LOAD --------

def load_profiles():

    try:

        with open(PROFILE_FILE, "r") as f:

            return json.load(f)

    except:

        return {}



# -------- SAVE --------

def save_profiles(profiles):

    with open(PROFILE_FILE, "w") as f:

        json.dump(profiles, f, indent=4)



# -------- UID (UPDATED TO 8 DIGIT NUMBER) --------

def generate_uid():

    profiles = load_profiles()

    existing_uids = set(profiles.keys())

    while True:

        uid = str(random.randint(10000000, 99999999))  # 8 digit number

        if uid not in existing_uids:

            return uid



# -------- USERNAME VALIDATION --------

def is_valid_username(username):

    pattern = r'^[A-Za-z0-9]+$'

    return re.match(pattern, username)



# -------- CREATE ACCOUNT --------

def create_profile(username=None, password=None, bio=""):

    profiles = load_profiles()


    if username is None:

        username = input("Write your username (letters and numbers only, no space): ")


    if password is None:

        password = input("Write your password: ")


    if not is_valid_username(username):

        print("Invalid username! Use only letters and numbers, no spaces.")

        return None


    for uid in profiles:

        if profiles[uid]["username"] == username:

            print("Username exists")

            return None


    uid = generate_uid()


    profiles[uid] = {

        "uid": uid,

        "username": username,

        "password": password,

        "bio": bio,

        "level": 1,

        "xp": 0,

        "likes": 0,

        "avatar": None,

        "banner": None

    }


    save_profiles(profiles)

    print("Account created. UID:", uid)

    return uid



# -------- LOGIN --------

def login(username, password):

    profiles = load_profiles()


    for uid in profiles:

        if (

            profiles[uid]["username"] == username

            and

            profiles[uid]["password"] == password

        ):

            print("Login success")

            return uid


    print("Login failed")

    return None



# -------- GET PROFILE --------

def get_profile(uid):

    profiles = load_profiles()

    return profiles.get(uid)



# -------- DELETE ACCOUNT --------

def delete_profile(uid):

    profiles = load_profiles()


    if uid in profiles:

        del profiles[uid]

        save_profiles(profiles)

        print("Account deleted")

        return True


    print("Delete failed")

    return False



# -------- UPDATE --------

def update_profile(uid, **kwargs):

    profiles = load_profiles()


    if uid in profiles:

        for key in kwargs:

            if key in profiles[uid]:

                profiles[uid][key] = kwargs[key]


        save_profiles(profiles)

        return True


    return False



# -------- XP --------

def add_xp(uid, amount):

    profiles = load_profiles()


    if uid in profiles:

        profiles[uid]["xp"] += amount


        while profiles[uid]["xp"] >= profiles[uid]["level"] * 100:

            profiles[uid]["xp"] -= profiles[uid]["level"] * 100

            profiles[uid]["level"] += 1


        save_profiles(profiles)

        return True


    return False



# -------- LIKE --------

def add_like(uid):

    profiles = load_profiles()


    if uid in profiles:

        profiles[uid]["likes"] += 1

        save_profiles(profiles)

        return True


    return False



# -------- AVATAR --------

def set_avatar(uid, path):

    profiles = load_profiles()


    if uid in profiles:

        profiles[uid]["avatar"] = path

        save_profiles(profiles)

        return True


    return False



# -------- BANNER --------

def set_banner(uid, path):

    profiles = load_profiles()


    if uid in profiles:

        profiles[uid]["banner"] = path

        save_profiles(profiles)

        return True


    return False



# -------- TEST --------

if __name__ == "__main__":


    uid = create_profile()


    print(get_profile(uid))


    delete_profile(uid)