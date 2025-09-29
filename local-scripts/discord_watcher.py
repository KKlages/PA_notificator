import requests
import time
import subprocess
import sys
from win10toast import ToastNotifier
import winsound
import atexit
import signal

# CONFIGURATION
API_URL = "https://pa-notificator.onrender.com"
MY_USER_ID = "player1"  # YOUR user ID
FRIEND_USER_ID = "player2"
DISCORD_USER_ID = "455124990166302750"
CHECK_INTERVAL = 3

toast = ToastNotifier()
previous_both_available = False

def set_my_status_offline():
    """Set my own status to offline when script exits"""
    try:
        response = requests.get(f"{API_URL}/status/{MY_USER_ID}", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data["available"]:  # Only toggle if currently available
                requests.post(f"{API_URL}/toggle/{MY_USER_ID}", timeout=5)
    except:
        pass

# Register cleanup
atexit.register(set_my_status_offline)

def signal_handler(sig, frame):
    set_my_status_offline()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def play_alert_sound():
    try:
        for i in range(10):
            winsound.Beep(1000, 200)
            time.sleep(0.1)
            winsound.Beep(1500, 200)
            time.sleep(0.1)
    except:
        pass

def notify_both_available():
    print("🚀 BOTH PLAYERS AVAILABLE!")
    play_alert_sound()
    
    try:
        toast.show_toast(
            "🎮 BOTH READY FOR PA!",
            f"You AND {FRIEND_USER_ID} are both available!\n\nCall them on Discord NOW!",
            duration=20,
            threaded=True
        )
    except:
        pass
    
    discord_url = f"discord://-/channels/@me/{DISCORD_USER_ID}"
    try:
        subprocess.run(f'start {discord_url}', shell=True)
    except:
        pass

def main():
    global previous_both_available
    
    print(f"🎮 PA Discord Auto-Notifier Active!")
    print(f"Watching for BOTH players to be available")
    print(f"You: {MY_USER_ID} | Friend: {FRIEND_USER_ID}\n")
    
    # Set my own status to offline on startup
    set_my_status_offline()
    
    # Get initial status
    try:
        response = requests.get(f"{API_URL}/all_status", timeout=5)
        if response.status_code == 200:
            data = response.json()
            my_status = data.get(MY_USER_ID, {}).get("available", False)
            friend_status = data.get(FRIEND_USER_ID, {}).get("available", False)
            previous_both_available = my_status and friend_status
            
            print(f"Initial status:")
            print(f"  You ({MY_USER_ID}): {'✅ Available' if my_status else '❌ Not Available'}")
            print(f"  Friend ({FRIEND_USER_ID}): {'✅ Available' if friend_status else '❌ Not Available'}")
            print()
    except:
        pass
    
    while True:
        try:
            response = requests.get(f"{API_URL}/all_status", timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                my_status = data.get(MY_USER_ID, {}).get("available", False)
                friend_status = data.get(FRIEND_USER_ID, {}).get("available", False)
                current_both_available = my_status and friend_status
                
                # Trigger notification when BOTH become available (transition to both green)
                if current_both_available and not previous_both_available:
                    notify_both_available()
                elif not current_both_available and previous_both_available:
                    print("❌ One or both players no longer available\n")
                
                previous_both_available = current_both_available
        except:
            pass
        
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        set_my_status_offline()
        sys.exit(0)