import requests
import time
import subprocess
import platform
import sys

# CONFIGURATION - CHANGE THESE
API_URL = "https://your-backend-url.com"  # Your deployed backend URL
FRIEND_USER_ID = "player2"  # The user ID you're watching (the OTHER person)
DISCORD_USER_ID = "123456789012345678"  # Your friend's Discord user ID (right-click their name, Copy ID)
CHECK_INTERVAL = 3  # seconds between checks

previous_status = False

def open_discord_call():
    """Opens Discord and initiates a call"""
    system = platform.system()
    
    # Method 1: Try to open Discord call directly
    discord_url = f"discord://call/{DISCORD_USER_ID}"
    
    try:
        if system == "Windows":
            subprocess.run(f'start {discord_url}', shell=True)
        elif system == "Darwin":  # macOS
            subprocess.run(['open', discord_url])
        elif system == "Linux":
            subprocess.run(['xdg-open', discord_url])
        
        print(f"✅ Opened Discord call to user {DISCORD_USER_ID}")
    except Exception as e:
        print(f"❌ Error opening Discord: {e}")

def main():
    global previous_status
    print("🎮 PA Discord Auto-Caller Active!")
    print(f"Watching: {FRIEND_USER_ID}")
    print(f"Will call Discord user: {DISCORD_USER_ID}")
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
                    print("📞 Initiating Discord call...")
                    open_discord_call()
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
        print("\n\nExiting Discord watcher...")
        sys.exit(0)