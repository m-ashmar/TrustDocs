# Import libraries
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import math
import time
from queue import Queue
import pyautogui
import mss
import tkinter as tk
from tkinter import messagebox
import Quartz
import AppKit
from ScriptingBridge import SBApplication  # MacOS-only automation

safari = SBApplication.alloc().initWithBundleIdentifier_("com.apple.Safari")  # ✅ Correct
safari.activate()  # Open Safari if it's closed

if safari.windows():
    safari.windows()[0].tabs()[0].setURL_("https://google.com")  # ✅ Correct method
    def popup_message(message, title="Message"):
        root = tk.Tk()
        root.withdraw()  # Hide the main tkinter window
        messagebox.showinfo(title, message)
        root.destroy()

# Function to get the active application window
def get_active_window():
    """Returns the active application window's bounds on macOS"""
    app = AppKit.NSWorkspace.sharedWorkspace().frontmostApplication()
    options = Quartz.kCGWindowListOptionOnScreenOnly
    window_list = Quartz.CGWindowListCopyWindowInfo(options, Quartz.kCGNullWindowID)

    for window in window_list:
        if "kCGWindowOwnerName" in window and window["kCGWindowOwnerName"] == app.localizedName():
            bounds = window["kCGWindowBounds"]
            return bounds["X"], bounds["Y"], bounds["Width"], bounds["Height"]
    return None
    # start game
result = messagebox.askyesno("Karate Kido2 Launcher", "Would you like to run Karate Kido2?")
if result:
    # Open game in browser
    import webbrowser
    webbrowser.open('https://prizes.gamee.com/game/karatekid2')
    popup_message("Running game... Wait!", "Launching")
    time.sleep(2)

    # Ask user to hover over the PLAY button
    popup_message("Hover your mouse over the PLAY button in the next 3 seconds.", "Instruction")
    time.sleep(1)
    play_button = pyautogui.position()

    popup_message("Hover your mouse over the LEFT position in the next 3 seconds.", "Instruction")
    time.sleep(1)
    left_button = pyautogui.position()

    popup_message("Hover your mouse over the RIGHT position in the next 3 seconds.", "Instruction")
    time.sleep(1)
    right_button = pyautogui.position()

    popup_message("All Done! The game will start playing. HAVE FUN!", "Done!")

else:
    shell.Popup("Maybe next time.", 4, "Bye!")
    
    
    
# detect window
game_window_bounds = get_active_window()
if game_window_bounds :
        
        x, y, w, h = game_window_bounds
        with mss.mss() as sct:
            monitor = {"top": int(y), "left": int(x), "width": int(w), "height": int(h)}
            screenshot = sct.grab(monitor)
            mss.tools.to_png(screenshot.rgb, screenshot.size, output="result.png")

        full_screenshot = cv.imread('result.png')
        game_window_template = cv.imread('game_window.png')
                                                 # Function to detect game window in screenshot (placeholder, implement logic)
        def detect_game_window(template, screenshot):
            return (x, y), (x + w, y + h)

        window_top_left, window_bottom_right = detect_game_window(game_window_template, full_screenshot)

        if window_top_left and window_bottom_right:
            top, left = window_top_left
            width, height = window_bottom_right[0] - left, window_bottom_right[1] - top
            cropped_image = full_screenshot[top: top + height, left: left + width]

            # Placeholder functions (implement actual logic)
            def preprocess_log(image):
                return [], []

            def log_coordinate(image, vertical_lines):
                return (0, 0), (0, 0), (0, 0)

            vertical_lines, horizontal_lines = preprocess_log(cropped_image)
            log_center, log_top_left, log_bottom_right = log_coordinate(cropped_image, vertical_lines)

            # Determine player position
            player_center = (230, 650)
            player_placement = "right" if player_center[0] > log_center[0] else "left"
else:
    popup_message("Maybe next time.", "Bye!")
    
    
    
    with mss.mss() as sct:
    # ✅ Make sure `game_window_bounds` is defined
         game_window_bounds = get_active_window()
    
    if game_window_bounds:
        x, y, w, h = game_window_bounds  # ✅ Extract window bounds correctly
        top, left, width, height = int(y), int(x), int(w), int(h)  # ✅ Ensure integer values

        monitor = {"top": top, "left": left, "width": width, "height": height}

        print('start')  
        i = 0  
        
        while i < 30:  # ✅ Avoid infinite loops
            frame = np.array(sct.grab(monitor))

            # ✅ Ensure these functions exist
            vertical_lines, horizontal_lines = preprocess_log(frame)
            branches = branches_coordinates(log_center, 
                                            (log_top_left[0] - 10, log_top_left[1]), 
                                            (log_bottom_right[0] + 10, log_bottom_right[1]), 
                                            horizontal_lines)
            glass_center, glass_top_left, glass_bottom_right = glass_filter(log_bottom_right, frame)

            _, branches_positions = decision_making(player_center, log_center, branches)     

            # ✅ Make a decision
            branch = None
            for element in range(len(branches_positions) - 1, -1, -1):  # Fix loop range
                branch = branches_positions[element]
                if branch['position'] == player_placement:
                    break
            
            if branch is None:
                continue  # Skip if no branch is found
            
            # ✅ Player movement logic
            if player_placement == 'right' and abs(player_center[1] - branch['coordinate']) < 150:
                player_placement = 'left'
            elif player_placement == 'left' and abs(player_center[1] - branch['coordinate']) < 150:
                player_placement = 'right'

            move_x = right_button_x if player_placement == 'right' else left_button_x
            move_y = right_button_y if player_placement == 'right' else left_button_y

            # ✅ Avoid clicking too frequently
            if abs(glass_center[1] - player_center[1]) < 180 and abs(glass_center[1] - player_center[1]) > 40:
                print(f'Frame {i}: Hit glass')
                pyautogui.click(x=move_x, y=move_y)

            pyautogui.click(x=move_x, y=move_y)
            i += 1

    else:
        print("❌ Error: Unable to detect game window.")