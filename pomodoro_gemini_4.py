import tkinter
from tkinter import ttk
import math
try:
    from playsound import playsound
except ImportError:
    print("The 'playsound' library is not installed. Please install it to enable the ringtone.")
    def playsound(sound):
        pass

# --- CONSTANTS --- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 15
pomodoros_completed = 0
timer = None
rectangle_id = None # Global variable to store the ID of the red rectangle
timer_text_id = None # Global variable to store the ID of the timer text

# --- TIMER ACTIONS --- #
def start_work():
    """Starts a work session timer."""
    reset_timer(silent=True)
    title_label.config(text="Work")
    style.configure("Title.TLabel", foreground=GREEN)
    count_down(WORK_MIN * 60)

def start_short_break():
    """Starts a short break timer."""
    reset_timer(silent=True)
    title_label.config(text="Break")
    style.configure("Title.TLabel", foreground=PINK)
    count_down(SHORT_BREAK_MIN * 60)

def start_long_break():
    """Starts a long break timer."""
    reset_timer(silent=True)
    title_label.config(text="Break")
    style.configure("Title.TLabel", foreground=RED)
    count_down(LONG_BREAK_MIN * 60)

def reset_timer(silent=False):
    """
    Resets the timer. If silent is False, it resets checkmarks too.
    'silent=True' is used when starting a new timer to stop the old one.
    """
    global timer
    global pomodoros_completed

    # Stop the currently running timer
    if timer:
        window.after_cancel(timer)
        timer = None

    # Full reset (if triggered by the Reset button)
    if not silent:
        canvas.itemconfig(timer_text_id, text="00:00")
        title_label.config(text="Timer")
        style.configure("Title.TLabel", foreground=GREEN)
        check_marks.config(text="")
        pomodoros_completed = 0

# --- COUNTDOWN MECHANISM --- #
def count_down(count):
    """Handles the timer countdown logic and updates the display every second."""
    global timer
    global pomodoros_completed
    
    count_min = math.floor(count / 60)
    count_sec = count % 60
    
    if count_sec < 10:
        count_sec = f"0{count_sec}"

    canvas.itemconfig(timer_text_id, text=f"{count_min}:{count_sec}")
    
    if count > 0:
        timer = window.after(1000, count_down, count - 1)
    else:
        playsound('ring.wav') # Replace 'ring.wav' with your own sound file
        if title_label.cget("text") == "Work":
            pomodoros_completed += 1
            check_marks.config(text="✔" * pomodoros_completed)

# --- UI SETUP --- #
window = tkinter.Tk()
window.title("Pomodoro")
window.attributes('-topmost', True) # <-- ALWAYS ON TOP
window.config(padx=5, pady=5) # Initial padding

# Make row 1 (where the canvas is) expandable
window.grid_rowconfigure(1, weight=1)
# Make columns 0-3 (which the canvas spans) expandable
for i in range(4):
    window.grid_columnconfigure(i, weight=1)

def on_canvas_resize(event):
    """Resizes the red rectangle and repositions the timer text when the canvas changes size."""
    global rectangle_id, timer_text_id
    new_width = event.width
    new_height = event.height
    canvas.coords(rectangle_id, 0, 0, new_width, new_height)
    canvas.coords(timer_text_id, new_width / 2, new_height / 2)


# --- TTK STYLE CONFIGURATION --- #
style = ttk.Style()
style.configure("Title.TLabel",
                foreground=GREEN,
                font=(FONT_NAME, 30, "bold"))

style.configure("Check.TLabel",
                foreground=GREEN,
                font=(FONT_NAME, 15, "bold"))

# --- WIDGET LAYOUT --- #
# Row 0: Title
title_label = ttk.Label(text="Timer", style="Title.TLabel")
title_label.grid(column=0, row=0, columnspan=4)

# Row 1: Canvas with Tomato and Timer Text
canvas = tkinter.Canvas(width=200, height=224, highlightthickness=0) # Keep initial size, but it will expand
# try:
#     tomato_img = tkinter.PhotoImage(file="tomato.png")
#     canvas.create_image(100, 112, image=tomato_img)
# except tkinter.TclError: # This comment was part of the original code, but it's good to keep it for context.
#     print("Error: 'tomato.png' not found. A placeholder will be used.") # This comment was part of the original code, but it's good to keep it for context.

# Initial draw of the rectangle and timer text, storing their IDs
rectangle_id = canvas.create_rectangle(0, 0, 200, 224, fill=RED, outline="")
timer_text_id = canvas.create_text(100, 112, text="00:00", fill="white", font=(FONT_NAME, 25, "bold"))
canvas.grid(column=0, row=1, columnspan=4, sticky="nsew") # Added sticky="nsew" to make canvas fill its grid cell
canvas.bind("<Configure>", on_canvas_resize) # Bind the resize event to the canvas

# Row 2: Checkmarks
check_marks = ttk.Label(text="", style="Check.TLabel")
check_marks.grid(column=0, row=2, columnspan=4)

# Row 3: Buttons
work_button = tkinter.Button(text="Work",
                             command=start_work)
work_button.grid(column=0, row=3)

short_break_button = tkinter.Button(text="Short Break",
                                     command=start_short_break)
short_break_button.grid(column=1, row=3)

long_break_button = tkinter.Button(text="Long Break",
                                    command=start_long_break)
long_break_button.grid(column=2, row=3)

reset_button = tkinter.Button(text="Reset",
                               command=reset_timer)
reset_button.grid(column=3, row=3)

# Start the application's main event loop
window.mainloop()
