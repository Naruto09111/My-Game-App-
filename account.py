import requests
import webbrowser

# --- CONFIGURATION (Updated with your ID) ---
API_KEY = "AIzaSyDbJpeZ8IqZmn-9gJHLSkMPCylJUvxT1V8"
PROJECT_ID = "my-game-2aab1"
# Aapki copy ki hui Client ID
CLIENT_ID = "321534946794-f2o148nou4rlvf5r593fm86tp6p7oq02.apps.googleusercontent.com"

def login_with_google():
    """Google Login page browser mein kholne ke liye"""
    # Firebase standard auth handler URL
    auth_url = f"https://{PROJECT_ID}.firebaseapp.com/__/auth/handler"
    try:
        webbrowser.open(auth_url)
        print("Opening Google Login in browser... Please sign in.")
        return True
    except Exception as e:
        print(f"Error opening browser: {e}")
        return False

def signup(email, password):
    """Naya account aur verification email ke liye"""
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={API_KEY}"
    payload = {"email": email, "password": password, "returnSecureToken": True}
    try:
        r = requests.post(url, json=payload).json()
        if "idToken" in r:
            # Verification email link bhejna
            v_url = f"https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode?key={API_KEY}"
            requests.post(v_url, json={"requestType": "VERIFY_EMAIL", "idToken": r["idToken"]})
            print("Signup Success! Verify your email.")
            return r["localId"]
        else:
            print("Signup Error:", r.get('error', {}).get('message'))
    except:
        pass
    return None

def login(email, password):
    """Email login aur verification check"""
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={API_KEY}"
    payload = {"email": email, "password": password, "returnSecureToken": True}
    try:
        r = requests.post(url, json=payload).json()
        if "idToken" in r:
            # Check if email verified
            check_url = f"https://identitytoolkit.googleapis.com/v1/accounts:lookup?key={API_KEY}"
            info = requests.post(check_url, json={"idToken": r["idToken"]}).json()
            if info["users"][0]["emailVerified"]:
                print("Login Successful!")
                return r["localId"]
            else:
                print("Error: Please verify your email first!")
    except:
        pass
    return None

def forgot_password(email):
    """Password reset link bhejna"""
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode?key={API_KEY}"
    payload = {"requestType": "PASSWORD_RESET", "email": email}
    requests.post(url, json=payload)
    print("Reset email sent!")
