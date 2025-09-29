import keyboard
import requests
import sys
import atexit
import signal

# CONFIGURATION
API_URL = "https://pa-notificator.onrender.com"
USER_ID = "player1"  # Change to "player2" for your friend
HOTKEY = "ctrl+shift+y"

def set_status(available):
    """Set status to a specific state"""
    try:
        # Get current status first
        response = requests.get(f"{API_URL}/status/{USER_ID}", timeout=5)
        if response.status_code == 200:
            current = response.json()
            # Only toggle if different from desired state
            if current["available"] != available:
                response = requests.post(f"{API_URL}/toggle/{USER_ID}", timeout=5)
                return response.status_code == 200
            return True
    except Exception as e:
        print(f"Error: {e}")
        return False

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

def set_offline():
    """Set status to offline when script exits"""
    print("\nSetting status to OFFLINE...")
    try:
        response = requests.get(f"{API_URL}/status/{USER_ID}", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data["available"]:  # Only toggle if currently available
                requests.post(f"{API_URL}/toggle/{USER_ID}", timeout=5)
                print("✅ Status set to OFFLINE")
    except Exception as e:
        print(f"⚠️ Could not set offline status: {e}")

# Register cleanup function for normal exit
atexit.register(set_offline)

# Handle Ctrl+C gracefully
def signal_handler(sig, frame):
    print("\nExiting...")
    set_offline()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

print(f"🎮 PA Status Hotkey Active!")
print(f"Press {HOTKEY} to toggle your availability")
print(f"User: {USER_ID}")
print(f"Press Ctrl+C to exit")
print(f"Status will automatically go OFFLINE when you close this or shutdown PC\n")

# Set to offline on startup (in case PC crashed last time)
set_offline()

keyboard.add_hotkey(HOTKEY, toggle_availability)

try:
    keyboard.wait()
except KeyboardInterrupt:
    set_offline()
    sys.exit(0)