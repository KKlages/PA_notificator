import requests
import time
import subprocess
import platform
import sys
from plyer import notification
import winsound  # For Windows sound

# CONFIGURATION - CHANGE THESE
API_URL = "https://pa-notificator.onrender.com"
FRIEND_USER_ID = "player2"
DISCORD_USER_ID = "455124990166302750"
CHECK_INTERVAL = 3

previous_status = False

def play_alert_sound():
    """Play an alert sound"""
    system = platform.system()
    
    try:
        if system == "Windows":
            # Play Windows exclamation sound 5 times
            for _ in range(5):
                winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
                time.sleep(0.3)
        elif system == "Darwin":  # macOS
            # Play system alert sound
            subprocess.run(['afplay', '/System/Library/Sounds/Glass.aiff'])
        elif system == "Linux":
            # Play system beep
            subprocess.run(['paplay', '/usr/share/sounds/freedesktop/stereo/message.oga'])
    except Exception as e:
        print(f"⚠️ Could not play sound: {e}")

def notify_friend_available():
    """Show persistent desktop notification with sound"""
    
    # Play sound first
    print("🔊 Playing alert sound...")
    play_alert_sound()
    
    # Show desktop notification (stays until dismissed)
    notification.notify(
        title='🎮 FRIEND AVAILABLE FOR PA!',
        message=f'{FRIEND_USER_ID} is ready to play!\n\nClick to dismiss, then call them on Discord.',
        app_name='PA Notifier',
        timeout=0  # 0 = stays on screen until manually dismissed
    )
    
    # Open Discord DM
    system = platform.system()
    discord_url = f"discord://-/channels/@me/{DISCORD_USER_ID}"
    
    try:
        if system == "Windows":
            subprocess.run(f'start {discord_url}', shell=True)
        elif system == "Darwin":
            subprocess.run(['open', discord_url])
        elif system == "Linux":
            subprocess.run(['xdg-open', discord_url])
        
        print(f"✅ Opened Discord DM with user {DISCORD_USER_ID}")
        print("💡 Notification will stay on screen - dismiss it when ready!")
    except Exception as e:
        print(f"❌ Error opening Discord: {e}")

def main():
    global previous_status
    print("🎮 PA Discord Auto-Notifier Active!")
    print(f"Watching: {FRIEND_USER_ID}")
    print(f"Discord user: {DISCORD_USER_ID}")
    print(f"Checking every {CHECK_INTERVAL} seconds...")
    print("Press Ctrl+C to exit\n")
    
    while True:
        try:
            response = requests.get(f"{API_URL}/status/{FRIEND_USER_ID}", timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                current_status = data.get("available", False)
                
                # Detect transition from unavailable to available
                if current_status and not previous_status:
                    print(f"\n🚀 {FRIEND_USER_ID} is now AVAILABLE!")
                    print("📞 Sending notification and opening Discord...")
                    notify_friend_available()
                    print()
                elif not current_status and previous_status:
                    print(f"❌ {FRIEND_USER_ID} is now unavailable\n")
                
                previous_status = current_status
            else:
                print(f"⚠️ API error: {response.status_code}")
            
        except requests.exceptions.RequestException as e:
            print(f"⚠️ Connection error: {e}")
        except Exception as e:
            print(f"⚠️ Unexpected error: {e}")
        
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExiting Discord notifier...")
        sys.exit(0)