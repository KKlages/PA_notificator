import keyboard
import requests
import sys
import time

# CONFIGURATION - CHANGE THESE
API_URL = "https://your-backend-url.com"  # Your deployed backend URL
USER_ID = "player1"  # Change to "player2" for the other person
HOTKEY = "ctrl+shift+p"  # Change to whatever hotkey you want

def toggle_availability():
    try:
        response = requests.post(f"{API_URL}/toggle/{USER_ID}", timeout=5)
        if response.status_code == 200:
            data = response.json()
            status = "AVAILABLE ✅" if data["available"] else "NOT AVAILABLE ❌"
            print(f"Status toggled to: {status}")
        else:
            print(f"Error: {response.status_code}")
    except Exception as e:
        print(f"Error connecting to API: {e}")

print(f"PA Status Hotkey Active!")
print(f"Press {HOTKEY} to toggle your availability")
print(f"User: {USER_ID}")
print(f"Press Ctrl+C to exit\n")

keyboard.add_hotkey(HOTKEY, toggle_availability)

try:
    keyboard.wait()
except KeyboardInterrupt:
    print("\nExiting...")
    sys.exit(0)