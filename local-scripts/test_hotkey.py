import keyboard

HOTKEY = "ctrl+shift+y"

def test():
    print("✅ HOTKEY WORKS!")

print(f"Testing hotkey: {HOTKEY}")
print("Press the hotkey now...")

keyboard.add_hotkey(HOTKEY, test)
keyboard.wait()