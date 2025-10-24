# --- IMPORT STATEMENTS --- #
# These lines import the necessary libraries (modules) that your script needs to run.

import tkinter
from tkinter import ttk, simpledialog
import math
from datetime import datetime
import os

# This is a 'try-except' block. It's a way to handle potential errors gracefully.
try:
    # Python will try to import the 'playsound' library.
    from playsound import playsound
except ImportError:
    # If the 'playsound' library isn't installed, Python would normally crash with an 'ImportError'.
    # This 'except' block catches that specific error.
    print("The 'playsound' library is not installed. Please install it to enable the ringtone.")
    # As a fallback, we define a dummy 'playsound' function that does nothing.
    # This prevents the rest of the script from crashing if the library is missing.
    def playsound(sound):
        pass

# --- CONSTANTS --- #
# Constants are variables whose values are not meant to change. Using them makes the code
# more readable (e.g., using 'RED' is clearer than '#e7305b') and easier to modify.
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"

# Timer settings in minutes.
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 15

# --- GLOBAL VARIABLES --- #
# These variables are defined outside of any function, making them 'global'.
# They can be accessed and modified by any function in the script, but you must use
# the 'global' keyword inside a function to modify them.

pomodoros_completed = 0
timer = None
rectangle_id = None # Stores the unique ID for the canvas rectangle, so we can modify it later.
timer_text_id = None # Stores the unique ID for the canvas text, so we can update the time.
current_task = None # Stores the description of the current task.

# --- TIMER ACTIONS --- #
# These functions are "event handlers" that run when you click the corresponding buttons.

def start_work():
    """Starts a work session timer."""
    reset_timer(silent=True)  # Stop any existing timer without resetting the checkmarks.
    global current_task
    # Prompt the user for the task they are working on.
    task = simpledialog.askstring("New Task", "What are you working on?", parent=window)

    # Only start the timer if the user entered a task.
    if task:
        current_task = task
        title_label.config(text=f"Work: {current_task}")  # Update the title to show the current task.
        style.configure("Title.TLabel", foreground=GREEN)  # Change the title color to green.
        count_down(WORK_MIN * 60)  # Start the countdown with the work duration (in seconds).

def start_short_break():
    """Starts a short break timer."""
    reset_timer(silent=True)  # Stop any existing timer.
    title_label.config(text="Break")  # Change the title label to "Break".
    style.configure("Title.TLabel", foreground=PINK)  # Change the title color to pink.
    count_down(SHORT_BREAK_MIN * 60)  # Start the countdown with the short break duration.

def start_long_break():
    """Starts a long break timer."""
    reset_timer(silent=True)  # Stop any existing timer.
    title_label.config(text="Break")  # Change the title label to "Break".
    style.configure("Title.TLabel", foreground=RED)  # Change the title color to red.
    count_down(LONG_BREAK_MIN * 60)  # Start the countdown with the long break duration.

def reset_timer(silent=False):
    """
    Resets the timer. If 'silent' is False, it performs a full UI reset.
    The 'silent=True' mode is used internally to stop an old timer before starting a new one.
    """
    # The 'global' keyword tells Python that we want to modify the global variables
    # 'timer' and 'pomodoros_completed', not create new local ones.
    global timer
    global pomodoros_completed

    # 'timer' holds the ID of the scheduled 'after' job.
    if timer:
        # 'window.after_cancel()' stops the scheduled countdown loop.
        window.after_cancel(timer)
        timer = None

    # This block only runs for a full reset (when the user clicks the "Reset" button).
    if not silent:
        # 'canvas.itemconfig' changes the properties of an item on the canvas.
        canvas.itemconfig(timer_text_id, text="00:00")  # Reset the timer text.
        title_label.config(text="Timer")  # Reset the title text.
        style.configure("Title.TLabel", foreground=GREEN)  # Reset the title color.
        check_marks.config(text="")  # Clear all checkmarks.
        pomodoros_completed = 0  # Reset the completed pomodoros counter.

# --- COUNTDOWN MECHANISM --- #
def count_down(count):
    """Handles the timer countdown logic and updates the display every second."""
    # We need to modify the global 'timer' and 'pomodoros_completed' variables.
    global timer
    global current_task
    global pomodoros_completed
    
    # 'math.floor' gives the whole number part of a division (e.g., 155 / 60 = 2.58 -> 2).
    count_min = math.floor(count / 60)  # Calculate remaining minutes.
    # The modulo operator '%' gives the remainder of a division (e.g., 155 % 60 = 35).
    count_sec = count % 60  # Calculate remaining seconds.
    
    # This ensures the seconds are always two digits (e.g., "09" instead of "9").
    if count_sec < 10:
        count_sec = f"0{count_sec}"

    # Update the text on the canvas to show the new time.
    # f-strings (formatted strings) are an easy way to embed variables in text.
    canvas.itemconfig(timer_text_id, text=f"{count_min}:{count_sec}")
    
    # This is the main loop of the timer.
    if count > 0:
        # 'window.after()' tells tkinter to call a function after a specified time (in milliseconds).
        # Here, it calls 'count_down' again after 1000ms (1 second) with the count reduced by 1.
        # We store the job ID in 'timer' so we can cancel it later if needed.
        timer = window.after(1000, count_down, count - 1)
    else:
        # When the count reaches 0, the timer is done.
        # --- Sound Notification with Fallback ---
        # This try/except block prevents the app from crashing if the sound file is missing or there's an audio error.
        sound_file = 'ring.wav'
        try:
            if os.path.exists(sound_file):
                playsound(sound_file)
            else:
                print(f"Warning: Sound file '{sound_file}' not found. Using system bell.")
                window.bell() # Use a simple system beep as a fallback.
        except Exception as e:
            print(f"Error playing sound: {e}. Using system bell as a fallback.")
            window.bell() # Use a simple system beep as a fallback.
        # Check if the session that just ended was a "Work" session by checking the title.
        if title_label.cget("text").startswith("Work"):
            pomodoros_completed += 1  # Increment the counter.
            # Update the checkmarks label to show the new total.
            # In Python, multiplying a string repeats it (e.g., "A" * 3 is "AAA").
            check_marks.config(text="✔" * pomodoros_completed)

            # --- LOG THE COMPLETED TASK TO A FILE ---
            if current_task:
                # Get the current date to use in the filename.
                today_str = datetime.now().strftime("%Y-%m-%d")
                filename = f"{today_str}_Completed-Pomodoro-Tasks.txt"
                # Get a full timestamp for the log entry.
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                # Open the file in "append" mode ('a') and write the new log entry.
                with open(filename, "a") as file:
                    file.write(f"[{timestamp}] Completed: {current_task}\n")
                current_task = None # Clear the task after it has been logged.

# --- UI SETUP --- #
# This section creates the main window and all the visual elements (widgets).

# Create the main application window. 'Tk()' is the top-level widget.
window = tkinter.Tk()
window.title("Pomodoro")  # Set the text that appears in the window's title bar.
window.attributes('-topmost', True)  # This makes the window always stay on top of others.
window.config(padx=5, pady=5)  # Add 5 pixels of padding around the inside of the window.

# --- GRID LAYOUT CONFIGURATION FOR RESIZING --- #
# The 'grid' layout manager organizes widgets in a table-like structure.
# By default, rows and columns don't resize with the window.
# 'weight=1' tells the row/column to expand and take up any extra space.

window.grid_rowconfigure(1, weight=1)  # Make row 1 (where the canvas is) expandable.
# The canvas spans 4 columns, so we make all of them expandable.
for i in range(4):
    window.grid_columnconfigure(i, weight=1)

def on_canvas_resize(event):
    """Resizes the red rectangle and repositions the timer text when the canvas changes size."""
    # This function is an event handler bound to the canvas's resize event.
    global rectangle_id, timer_text_id
    new_width = event.width  # Get the new width of the canvas from the event object.
    new_height = event.height  # Get the new height.
    # 'canvas.coords' updates the coordinates of a canvas item.
    # Update the rectangle to fill the new canvas size.
    canvas.coords(rectangle_id, 0, 0, new_width, new_height)
    # Update the timer text to be in the center of the new canvas size.
    canvas.coords(timer_text_id, new_width / 2, new_height / 2)


# --- TTK STYLE CONFIGURATION --- #
# 'ttk' provides themed widgets that look more modern than the classic tkinter widgets.
# 'ttk.Style()' allows us to define custom styles for these widgets.
style = ttk.Style()

# Define a custom style named "Title.TLabel".
style.configure("Title.TLabel",
                foreground=GREEN,  # Set the text color.
                font=(FONT_NAME, 15, "bold"))  # Set the font, size, and weight.

# Define a custom style for the checkmarks label.
style.configure("Check.TLabel",
                foreground=GREEN,
                font=(FONT_NAME, 15, "bold"))

# --- WIDGET LAYOUT --- #
# Here we create the widgets and place them in the window using the 'grid' layout manager.

# Row 0: Title Label
title_label = ttk.Label(text="Timer", style="Title.TLabel")  # Create a label with our custom style.
# Place the label in the grid at row 0, column 0.
# 'columnspan=4' makes the label stretch across all 4 columns.
title_label.grid(column=0, row=0, columnspan=4)

# Row 1: Canvas for Timer Display
# A Canvas widget is used for drawing shapes and images.
canvas = tkinter.Canvas(width=200, height=224, highlightthickness=0)  # Set initial size and remove border.

# Draw the background rectangle and the timer text, storing their IDs in our global variables.
rectangle_id = canvas.create_rectangle(0, 0, 200, 224, fill=RED, outline="") # This line creates the red rectangle
timer_text_id = canvas.create_text(100, 112, text="00:00", fill="white", font=(FONT_NAME, 35, "bold")) # Change '25' to your desired font size

# Place the canvas in the grid at row 1.
# 'sticky="nsew"' makes the canvas stick to all four sides (north, south, east, west) of its grid cell,
# causing it to expand when the cell expands.
canvas.grid(column=0, row=1, columnspan=4, sticky="nsew")
# 'bind' attaches an event handler to a widget. Here, whenever the canvas is resized ('<Configure>' event),
# the 'on_canvas_resize' function will be called.
canvas.bind("<Configure>", on_canvas_resize)

# Row 2: Checkmarks Label
check_marks = ttk.Label(text="", style="Check.TLabel")  # Create the label for checkmarks.
check_marks.grid(column=0, row=2, columnspan=4)  # Place it in row 2, spanning all columns.

# Row 3: Control Buttons
# These are standard tkinter Buttons. The 'command' option links a button click to a function.
work_button = tkinter.Button(text="Work", command=start_work)
work_button.grid(column=0, row=3)  # Place in row 3, column 0.

short_break_button = tkinter.Button(text="Short Break", command=start_short_break)
short_break_button.grid(column=1, row=3)  # Place in row 3, column 1.

long_break_button = tkinter.Button(text="Long Break", command=start_long_break)
long_break_button.grid(column=2, row=3)  # Place in row 3, column 2.

# Note: The 'reset_timer' function is called directly without arguments, so 'silent' defaults to False.
reset_button = tkinter.Button(text="Reset", command=reset_timer)
reset_button.grid(column=3, row=3)  # Place in row 3, column 3.

# --- START THE APPLICATION --- #
# 'window.mainloop()' starts the tkinter event loop. This is a blocking call that keeps the
# window open, listens for events (like button clicks and window resizing), and runs the
# appropriate event handlers. The script will stay on this line until the window is closed.
window.mainloop()
