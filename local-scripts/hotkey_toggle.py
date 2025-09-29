import keyboard
import requests
import sys

# CONFIGURATION
API_URL = "https://pa-notificator.onrender.com"
USER_ID = "player1"  # Change to "player2" for your friend
HOTKEY = "ctrl+shift+y"

def toggle_availability():
    try:
        response = requests.post(f"{API_URL}/toggle/{USER_ID}", timeout=5)
        if response.status_code == 200:
            data = response.json()
            # Silent operation - no console output when running in background
    except:
        pass  # Fail silently

keyboard.add_hotkey(HOTKEY, toggle_availability)

try:
    keyboard.wait()
except:
    sys.exit(0)