# Pomodoro Timer - Complete Code Documentation

## Overview
This is a comprehensive Pomodoro Timer GUI application implemented in Python using tkinter. The application follows the Pomodoro Technique - a time management method that uses timed work intervals separated by short breaks.

## Features
- Customizable work and break durations
- Visual progress tracking with progress bar
- Audio notifications when sessions complete
- Automatic session progression (work → break → work)
- Multiple timer modes (Classic 25/5/15, Focus 45/10/30)
- Pause/resume functionality
- Auto-start options for breaks and work sessions
- Responsive design that adapts to window resizing

## Dependencies
- `tkinter`: GUI framework (built into Python)
- `pygame`: Audio notification system
- `numpy`: Sound wave generation
- `threading`: Non-blocking timer execution
- `time`: Timer countdown functionality

## Installation & Usage
```bash
# Install required dependencies
pip install pygame numpy

# Run the application
python pomodoro_timer.py
```

---

## Detailed Line-by-Line Code Explanation

### Module Header and Documentation (Lines 1-24)

```python
"""
POMODORO TIMER GUI APPLICATION
...
"""
```

**Purpose**: Multi-line docstring that serves as the module's documentation
- **Lines 2-3**: Application title and brief description
- **Lines 4-5**: Explains the Pomodoro Technique methodology
- **Lines 7-14**: Lists all key features of the application
- **Lines 16-21**: Documents required dependencies with descriptions
- **Lines 23-24**: Metadata about authorship and creation date

### Import Statements (Lines 26-32)

```python
import tkinter as tk
from tkinter import ttk, messagebox
import time
import threading
import pygame
import os
from datetime import datetime, timedelta
```

**Line 26**: `import tkinter as tk`
- Imports the main GUI framework
- Aliased as `tk` for shorter, cleaner syntax throughout the code

**Line 27**: `from tkinter import ttk, messagebox`
- `ttk`: Themed widgets for modern appearance (progress bar)
- `messagebox`: Dialog boxes for user notifications

**Line 28**: `import time`
- Provides `time.sleep()` for countdown delays
- Used for precise timing in the timer loop

**Line 29**: `import threading`
- Enables running timer countdown in separate thread
- Prevents GUI from freezing during countdown operations

**Line 30**: `import pygame`
- Audio system for playing notification sounds
- Cross-platform audio support

**Line 31**: `import os`
- Operating system interface (imported but not used in current implementation)

**Line 32**: `from datetime import datetime, timedelta`
- Date/time handling utilities (imported but not used in current implementation)

### Class Definition and Documentation (Lines 34-50)

```python
class PomodoroTimer:
    """
    Main Pomodoro Timer Application Class
    ...
    """
```

**Line 34**: `class PomodoroTimer:`
- Defines the main application class using object-oriented programming
- Encapsulates all timer functionality in a single class

**Lines 35-50**: Class docstring
- Documents the class's responsibilities and architecture
- Explains the Model-View-Controller pattern implementation
- **Model**: Timer state variables and settings
- **View**: GUI widgets and display elements  
- **Controller**: Event handlers and timer logic

### Constructor Method (__init__) (Lines 52-118)

#### Method Signature and Documentation (Lines 52-72)

```python
def __init__(self, root):
    """
    Initialize the Pomodoro Timer Application
    ...
    """
```

**Line 52**: `def __init__(self, root):`
- Constructor method called when creating new PomodoroTimer instance
- `root` parameter: main tkinter window object

**Lines 53-72**: Method docstring
- Explains initialization process and purpose
- Documents all state variables that will be initialized
- Describes the setup sequence

#### Window Configuration (Lines 73-86)

```python
self.root = root
self.root.title("🍅 Pomodoro Timer")

# Set responsive window sizing with minimum constraints
self.root.geometry("500x480")
self.root.minsize(400, 400)
self.root.configure(bg="#2c3e50")

# Keep window always on top of other applications
self.root.attributes('-topmost', True)

# Dynamic spacing and font calculations
self.base_width = 500
self.base_height = 480
```

**Line 73**: `self.root = root`
- Stores reference to main window for later access

**Line 74**: `self.root.title("🍅 Pomodoro Timer")`
- Sets window title with tomato emoji representing Pomodoro

**Line 77**: `self.root.geometry("500x480")`
- Sets initial window size to 500 pixels wide by 480 pixels tall

**Line 78**: `self.root.minsize(400, 400)`
- Sets minimum window dimensions to prevent it becoming unusably small

**Line 79**: `self.root.configure(bg="#2c3e50")`
- Sets background color to dark blue-gray for professional appearance

**Line 82**: `self.root.attributes('-topmost', True)`
- Makes window stay on top of other applications for visibility during work

**Lines 85-86**: Base dimensions storage
- `self.base_width = 500`: Reference width for responsive design calculations
- `self.base_height = 480`: Reference height for responsive design calculations

#### Audio System Initialization (Lines 88-89)

```python
# Initialize pygame for sound
pygame.mixer.init()
```

**Line 89**: `pygame.mixer.init()`
- Initializes pygame's audio mixing system
- Must be called before any audio operations
- Enables cross-platform sound notification support

#### Timer State Variables (Lines 91-98)

```python
# Timer state variables
self.is_running = False
self.is_paused = False
self.current_session = "Work"
self.time_left = 0
self.total_time = 0
self.session_count = 0
self.completed_pomodoros = 0
```

**Line 92**: `self.is_running = False`
- Boolean flag indicating if timer is actively counting down
- `False` = stopped, `True` = running

**Line 93**: `self.is_paused = False`
- Boolean flag indicating if timer is paused (preserves progress)
- Allows resuming from exact same point

**Line 94**: `self.current_session = "Work"`
- String indicating current session type
- Possible values: "Work", "Short Break", "Long Break"

**Line 95**: `self.time_left = 0`
- Integer storing remaining seconds in current session
- Decrements every second during countdown

**Line 96**: `self.total_time = 0`
- Integer storing total session duration in seconds
- Used for progress bar percentage calculation

**Line 97**: `self.session_count = 0`
- Counter for completed work sessions
- Used to determine when long breaks should occur

**Line 98**: `self.completed_pomodoros = 0`
- Counter for total completed pomodoros
- Used for statistics tracking

#### Timer Settings Variables (Lines 100-105)

```python
# Timer settings (in minutes)
self.work_duration = tk.IntVar(value=25)
self.short_break_duration = tk.IntVar(value=5)
self.long_break_duration = tk.IntVar(value=15)
self.long_break_interval = tk.IntVar(value=4)
```

**Line 101**: `self.work_duration = tk.IntVar(value=25)`
- tkinter IntVar automatically syncs with GUI spinbox widgets
- Default 25 minutes (classic Pomodoro duration)

**Line 102**: `self.short_break_duration = tk.IntVar(value=5)`
- Short break duration, default 5 minutes
- Brief rest between work sessions

**Line 103**: `self.long_break_duration = tk.IntVar(value=15)`
- Long break duration, default 15 minutes
- Extended rest after multiple work sessions

**Line 104**: `self.long_break_interval = tk.IntVar(value=4)`
- Long break interval, default every 4 work sessions
- Determines when to trigger long vs short breaks

#### User Preference Variables (Lines 107-111)

```python
# Sound settings
self.sound_enabled = tk.BooleanVar(value=True)
self.auto_start_breaks = tk.BooleanVar(value=False)
self.auto_start_work = tk.BooleanVar(value=False)
```

**Line 108**: `self.sound_enabled = tk.BooleanVar(value=True)`
- Controls whether audio notifications play
- tkinter BooleanVar syncs with GUI checkbox widgets
- Default enabled

**Line 109**: `self.auto_start_breaks = tk.BooleanVar(value=False)`
- Controls automatic break starting after work sessions
- Default disabled (requires manual confirmation)

**Line 110**: `self.auto_start_work = tk.BooleanVar(value=False)`
- Controls automatic work resumption after breaks
- Default disabled (requires manual confirmation)

#### Final Initialization Steps (Lines 113-118)

```python
# Bind window resize event for responsive design
self.root.bind('<Configure>', self.on_window_resize)

# Create GUI elements
self.create_widgets()
self.update_display()
```

**Line 114**: `self.root.bind('<Configure>', self.on_window_resize)`
- Binds window resize events to responsive design handler
- Enables dynamic font and spacing adjustments

**Line 117**: `self.create_widgets()`
- Calls method to create all GUI components
- Builds the complete user interface

**Line 118**: `self.update_display()`
- Calls method to update display with initial values
- Ensures proper initial state representation

### GUI Creation Method (create_widgets) (Lines 120-232)

#### Method Documentation and Setup (Lines 120-136)

```python
def create_widgets(self):
    """
    Create and Configure All GUI Elements
    ...
    """
    # Calculate initial responsive values
    self.calculate_responsive_values()
    
    # Create main container frame for better spacing control
    main_container = tk.Frame(self.root, bg="#2c3e50")
    main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
```

**Line 132**: `self.calculate_responsive_values()`
- Calculates responsive font sizes and spacing based on current window size
- Must be called before creating widgets that use these values

**Line 135**: `main_container = tk.Frame(self.root, bg="#2c3e50")`
- Creates main container frame with dark background matching window
- Provides better spacing control than placing widgets directly on root

**Line 136**: `main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)`
- Packs container to fill entire window
- `fill=tk.BOTH, expand=True`: Expands to fill available space
- `padx=10, pady=5`: 10px horizontal, 5px vertical padding

#### Title Label Creation (Lines 138-146)

```python
# Main title
self.title_label = tk.Label(
    main_container, 
    text="🍅 Pomodoro Timer", 
    font=("Arial", self.title_font_size, "bold"),
    bg="#2c3e50", 
    fg="#ecf0f1"
)
self.title_label.pack(pady=self.title_pady)
```

**Lines 139-145**: Label widget creation
- `parent=main_container`: Places label in main container
- `text="🍅 Pomodoro Timer"`: Display text with tomato emoji
- `font=("Arial", self.title_font_size, "bold")`: Arial font, responsive size, bold weight
- `bg="#2c3e50"`: Dark background matching container
- `fg="#ecf0f1"`: Light gray text for contrast

**Line 146**: `self.title_label.pack(pady=self.title_pady)`
- Packs label with responsive vertical padding
- Centers horizontally by default

#### Session Type Label (Lines 148-156)

```python
# Current session label
self.session_label = tk.Label(
    main_container,
    text="Work Session",
    font=("Arial", self.session_font_size),
    bg="#2c3e50",
    fg="#e74c3c"
)
self.session_label.pack(pady=self.session_pady)
```

**Line 151**: `text="Work Session"`
- Initial display text showing current session type
- Will change dynamically during operation

**Line 154**: `fg="#e74c3c"`
- Red text color for work sessions
- Color changes based on session type (red/orange/purple)

#### Timer Display Container (Lines 158-169)

```python
# Time display with fixed container to prevent jumping
timer_container = tk.Frame(main_container, bg="#2c3e50", height=80)
timer_container.pack(pady=self.timer_pady, fill=tk.X)
timer_container.pack_propagate(False)

self.time_label = tk.Label(
    timer_container,
    text="25:00",
    font=("Arial", self.timer_font_size, "bold"),
    bg="#2c3e50",
    fg="#ecf0f1"
)
self.time_label.pack(expand=True)
```

**Line 159**: `timer_container = tk.Frame(..., height=80)`
- Creates fixed-height container to prevent timer display from jumping
- `height=80`: Fixed pixel height

**Line 161**: `timer_container.pack_propagate(False)`
- Prevents container from shrinking to fit contents
- Maintains consistent layout during time updates

**Line 165**: `text="25:00"`
- Initial time display showing 25 minutes
- Format: MM:SS with zero padding

**Line 166**: `font=("Arial", self.timer_font_size, "bold")`
- Uses fixed font size (48pt) for optimal readability
- Bold weight for prominence

**Line 169**: `self.time_label.pack(expand=True)`
- `expand=True`: Centers the label vertically in fixed container

#### Progress Bar (Lines 171-179)

```python
# Progress bar container for centered positioning
progress_container = tk.Frame(main_container, bg="#2c3e50")
progress_container.pack(pady=self.progress_pady, fill=tk.X)

self.progress = ttk.Progressbar(
    progress_container,
    length=self.progress_length,
    mode='determinate'
)
self.progress.pack()
```

**Line 172**: `progress_container = tk.Frame(...)`
- Creates container for progress bar to ensure proper centering

**Line 175**: `self.progress = ttk.Progressbar(...)`
- Uses themed widget (ttk) for modern appearance
- `length=self.progress_length`: Responsive width based on window size
- `mode='determinate'`: Shows specific percentage completion (0-100%)

#### Control Buttons (Lines 181-220)

```python
# Control buttons frame with improved spacing
control_frame = tk.Frame(main_container, bg="#2c3e50")
control_frame.pack(pady=self.controls_pady)

# Button width based on window size
button_width = max(8, int(10 * (self.root.winfo_width() / self.base_width)))

self.start_button = tk.Button(
    control_frame,
    text="Start",
    font=("Arial", self.button_font_size, "bold"),
    bg="#27ae60",
    fg="white",
    width=button_width,
    command=self.start_timer
)
self.start_button.pack(side=tk.LEFT, padx=8)
```

**Line 185**: `button_width = max(8, int(10 * (...)))`
- Calculates responsive button width based on window size
- `max(8, ...)`: Ensures minimum width of 8 characters
- Scales proportionally with window width

**Lines 187-196**: Start button creation
- `bg="#27ae60"`: Green background (semantic color for "go/start")
- `fg="white"`: White text for contrast
- `command=self.start_timer`: Connects button click to start_timer method

**Line 197**: `self.start_button.pack(side=tk.LEFT, padx=8)`
- Packs button to left side of control frame
- `padx=8`: 8 pixels horizontal spacing between buttons

**Similar pattern for Pause and Reset buttons**:
- Pause button: Orange background (#f39c12), calls `self.pause_timer`
- Reset button: Red background (#e74c3c), calls `self.reset_timer`

#### Settings Button (Lines 222-232)

```python
# Settings button with bottom spacing
settings_container = tk.Frame(main_container, bg="#2c3e50")
settings_container.pack(pady=self.settings_pady, side=tk.BOTTOM, fill=tk.X)

self.settings_button = tk.Button(
    settings_container,
    text="⚙️ Settings",
    font=("Arial", self.button_font_size),
    bg="#9b59b6",
    fg="white",
    command=self.open_settings
)
self.settings_button.pack()
```

**Line 225**: `settings_container.pack(..., side=tk.BOTTOM, ...)`
- `side=tk.BOTTOM`: Positions container at bottom of main container
- `fill=tk.X`: Expands horizontally to full width

**Line 228**: `text="⚙️ Settings"`
- Gear emoji provides visual identification of settings function

**Line 230**: `bg="#9b59b6"`
- Purple background to distinguish from other buttons

**Line 232**: `command=self.open_settings`
- Connects to method that creates settings window

### Settings Window Creation (create_settings_window) (Lines 234-374)

#### Window Setup (Lines 234-242)

```python
def create_settings_window(self):
    """
    Create Advanced Settings Configuration Window
    ...
    """
    settings_window = tk.Toplevel(self.root)
    settings_window.title("Pomodoro Settings")
    settings_window.geometry("400x500")
    settings_window.configure(bg="#2c3e50")
```

**Line 241**: `settings_window = tk.Toplevel(self.root)`
- Creates new top-level window (modal dialog)
- `self.root` as parent ensures proper window hierarchy

**Line 242**: `settings_window.title("Pomodoro Settings")`
- Sets window title for identification

**Line 243**: `settings_window.geometry("400x500")`
- Sets window size to 400x500 pixels (smaller than main window)

**Line 244**: `settings_window.configure(bg="#2c3e50")`
- Matches main window's dark theme

#### Duration Settings Frame (Lines 246-267)

```python
# Duration settings
duration_frame = tk.LabelFrame(
    settings_window,
    text="Timer Durations (minutes)",
    font=("Arial", 12, "bold"),
    bg="#34495e",
    fg="#ecf0f1"
)
duration_frame.pack(pady=10, padx=20, fill=tk.X)

# Work duration
tk.Label(duration_frame, text="Work Duration:", bg="#34495e", fg="#ecf0f1").grid(row=0, column=0, sticky="w", padx=5, pady=5)
work_spinbox = tk.Spinbox(duration_frame, from_=1, to=60, textvariable=self.work_duration, width=10)
work_spinbox.grid(row=0, column=1, padx=5, pady=5)
```

**Lines 247-254**: LabelFrame creation
- `tk.LabelFrame`: Frame with title border for grouping related controls
- `text="Timer Durations (minutes)"`: Title displayed in frame border
- `bg="#34495e"`: Slightly lighter than main background for visual hierarchy

**Line 257**: Work duration label
- `sticky="w"`: Aligns text to west (left) side of grid cell
- Grid layout used for precise alignment of labels and spinboxes

**Lines 258-259**: Work duration spinbox
- `from_=1, to=60`: Range of 1-60 minutes
- `textvariable=self.work_duration`: Automatically syncs with tkinter variable
- `width=10`: 10-character width for consistent appearance

**Similar pattern repeats for**:
- Short break duration (1-30 minutes range)
- Long break duration (1-60 minutes range)  
- Long break interval (2-10 sessions range)

#### Options Frame (Lines 276-308)

```python
# Sound and automation settings
options_frame = tk.LabelFrame(
    settings_window,
    text="Options",
    font=("Arial", 12, "bold"),
    bg="#34495e",
    fg="#ecf0f1"
)
options_frame.pack(pady=10, padx=20, fill=tk.X)

sound_check = tk.Checkbutton(
    options_frame,
    text="Enable sound notifications",
    variable=self.sound_enabled,
    bg="#34495e",
    fg="#ecf0f1",
    selectcolor="#2c3e50"
)
sound_check.pack(anchor="w", padx=5, pady=5)
```

**Lines 285-293**: Sound notification checkbox
- `tk.Checkbutton`: Checkbox widget for boolean options
- `variable=self.sound_enabled`: Automatically syncs with BooleanVar
- `selectcolor="#2c3e50"`: Color of checkbox when selected
- `anchor="w"`: Left-aligns checkbox in frame

**Similar pattern for**:
- Auto-start breaks checkbox
- Auto-start work sessions checkbox

#### Timer Modes Frame (Lines 310-347)

```python
# Theme selection
theme_frame = tk.LabelFrame(
    settings_window,
    text="Timer Modes",
    font=("Arial", 12, "bold"),
    bg="#34495e",
    fg="#ecf0f1"
)
theme_frame.pack(pady=10, padx=20, fill=tk.X)

mode_buttons_frame = tk.Frame(theme_frame, bg="#34495e")
mode_buttons_frame.pack(pady=5)

classic_button = tk.Button(
    mode_buttons_frame,
    text="Classic Mode",
    bg="#e67e22",
    fg="white",
    command=lambda: self.set_classic_mode()
)
classic_button.pack(side=tk.LEFT, padx=5)
```

**Line 324**: `command=lambda: self.set_classic_mode()`
- Lambda function creates anonymous function for button command
- Calls `set_classic_mode()` method when button clicked

**Classic Mode Button**: Orange background (#e67e22)
**Focus Mode Button**: Purple background (#8e44ad)

#### Save/Cancel Buttons (Lines 349-374)

```python
# Save and close buttons
button_frame = tk.Frame(settings_window, bg="#2c3e50")
button_frame.pack(pady=20)

save_button = tk.Button(
    button_frame,
    text="Save Settings",
    bg="#27ae60",
    fg="white",
    command=lambda: [self.save_settings(), settings_window.destroy()]
)
save_button.pack(side=tk.LEFT, padx=5)
```

**Line 359**: `command=lambda: [self.save_settings(), settings_window.destroy()]`
- Lambda with list executes multiple commands in sequence
- First saves settings, then closes window
- Provides immediate feedback and cleanup

**Cancel button**: Only calls `settings_window.destroy()` to close without saving

### Timer Mode Configuration Methods (Lines 376-401)

#### Classic Mode (Lines 376-388)

```python
def set_classic_mode(self):
    """
    Configure Classic Pomodoro Technique Settings
    ...
    """
    self.work_duration.set(25)
    self.short_break_duration.set(5)
    self.long_break_duration.set(15)
    self.long_break_interval.set(4)
```

**Purpose**: Applies traditional Francesco Cirillo Pomodoro settings
- 25-minute work sessions (optimal focus duration)
- 5-minute short breaks (brief mental rest)
- 15-minute long breaks (comprehensive restoration)
- Long break every 4 work sessions

#### Focus Mode (Lines 390-401)

```python
def set_focus_mode(self):
    """
    Configure Extended Focus Mode Settings
    ...
    """
    self.work_duration.set(45)
    self.short_break_duration.set(10)
    self.long_break_duration.set(30)
    self.long_break_interval.set(3)
```

**Purpose**: Applies extended intervals for deep work
- 45-minute work sessions (extended concentration)
- 10-minute short breaks (adequate recovery)
- 30-minute long breaks (comprehensive restoration)
- Long break every 3 sessions (more frequent due to intensity)

### Settings Management Methods (Lines 403-418)

#### Open Settings (Lines 403-410)

```python
def open_settings(self):
    """
    Launch Settings Configuration Window
    ...
    """
    self.create_settings_window()
```

**Purpose**: Simple wrapper method to create and display settings window

#### Save Settings (Lines 412-418)

```python
def save_settings(self):
    """
    Save User Configuration and Update Timer Display
    ...
    """
    if not self.is_running:
        self.reset_timer()
    messagebox.showinfo("Settings", "Settings saved successfully!")
```

**Line 417**: `if not self.is_running:`
- Only resets timer if not currently running
- Prevents interruption of active sessions

**Line 418**: `self.reset_timer()`
- Updates display with new duration settings
- Ensures consistency between settings and display

**Line 419**: `messagebox.showinfo(...)`
- Shows confirmation dialog to user
- Provides immediate feedback that settings were saved

### Timer Control Methods (Lines 420-483)

#### Start Timer (Lines 420-449)

```python
def start_timer(self):
    """
    Initialize and Begin Timer Countdown
    ...
    """
    if not self.is_running and not self.is_paused:
        if self.current_session == "Work":
            self.time_left = self.work_duration.get() * 60
        elif self.current_session == "Short Break":
            self.time_left = self.short_break_duration.get() * 60
        else:  # Long Break
            self.time_left = self.long_break_duration.get() * 60
        
        self.total_time = self.time_left
        
    self.is_running = True
    self.is_paused = False
    self.start_button.config(text="Running...", state="disabled")
    
    # Start the timer in a separate thread
    timer_thread = threading.Thread(target=self.run_timer)
    timer_thread.daemon = True
    timer_thread.start()
```

**Line 426**: `if not self.is_running and not self.is_paused:`
- Only initializes new session if starting fresh (not resuming)

**Lines 427-432**: Session duration lookup
- Determines duration based on current session type
- Multiplies by 60 to convert minutes to seconds

**Line 434**: `self.total_time = self.time_left`
- Stores total duration for progress calculation

**Lines 436-438**: State updates
- Sets running and paused flags
- Updates button text and disables to prevent double-clicking

**Lines 441-443**: Thread creation and startup
- `threading.Thread(target=self.run_timer)`: Creates new thread
- `daemon=True`: Thread automatically closes when main program exits
- `start()`: Begins thread execution

#### Pause Timer (Lines 451-460)

```python
def pause_timer(self):
    """
    Temporarily Suspend Timer Countdown
    ...
    """
    if self.is_running:
        self.is_paused = True
        self.is_running = False
        self.start_button.config(text="Resume", state="normal")
        self.pause_button.config(state="disabled")
```

**Line 456**: `if self.is_running:`
- Only allows pausing if timer is currently running

**Lines 457-458**: State updates
- Sets paused flag to preserve progress
- Clears running flag to stop countdown loop

**Lines 459-460**: Button updates
- Changes start button text to "Resume"
- Disables pause button to prevent multiple pause calls

#### Reset Timer (Lines 462-475)

```python
def reset_timer(self):
    """
    Reset Timer to Initial State
    ...
    """
    self.is_running = False
    self.is_paused = False
    self.current_session = "Work"
    self.time_left = self.work_duration.get() * 60
    self.total_time = self.time_left
    self.start_button.config(text="Start", state="normal")
    self.pause_button.config(state="normal")
    self.update_display()
```

**Lines 468-472**: Complete state reset
- Clears all running/paused flags
- Returns to "Work" session
- Sets time to current work duration setting
- Preserves user settings and statistics

**Lines 473-474**: Button restoration
- Resets button text and states to initial values

**Line 475**: `self.update_display()`
- Refreshes all display elements to reflect reset state

### Core Timer Engine (run_timer) (Lines 477-489)

```python
def run_timer(self):
    """
    Execute Timer Countdown Loop
    ...
    """
    while self.time_left > 0 and self.is_running:
        time.sleep(1)
        if self.is_running:
            self.time_left -= 1
            self.root.after(0, self.update_display)
            
    if self.time_left <= 0 and self.is_running:
        self.root.after(0, self.timer_finished)
```

**Line 483**: `while self.time_left > 0 and self.is_running:`
- Main countdown loop continues while time remains AND timer is running
- Dual condition allows for pause functionality

**Line 484**: `time.sleep(1)`
- Sleeps exactly 1 second (countdown interval)
- Prevents excessive CPU usage

**Line 485**: `if self.is_running:`
- Double-checks running state after sleep
- State may have changed during sleep (user clicked pause)

**Line 486**: `self.time_left -= 1`
- Decrements remaining time by 1 second

**Line 487**: `self.root.after(0, self.update_display)`
- Schedules display update on main thread (thread-safe)
- `after(0, ...)` executes immediately on main thread

**Lines 489-490**: Timer completion handling
- Checks if time expired while timer was still running
- Schedules completion handler on main thread

### Session Completion Handler (timer_finished) (Lines 491-527)

```python
def timer_finished(self):
    """
    Handle Session Completion and Transition Logic
    ...
    """
    self.is_running = False
    
    if self.sound_enabled.get():
        self.play_notification_sound()
        
    if self.current_session == "Work":
        self.completed_pomodoros += 1
        self.session_count += 1
        
        if self.session_count % self.long_break_interval.get() == 0:
            self.current_session = "Long Break"
        else:
            self.current_session = "Short Break"
            
        if self.auto_start_breaks.get():
            self.root.after(1000, self.start_timer)
        else:
            messagebox.showinfo("Session Complete", f"Work session complete! Time for a {self.current_session.lower()}.")
            
    else:
        self.current_session = "Work"
        
        if self.auto_start_work.get():
            self.root.after(1000, self.start_timer)
        else:
            messagebox.showinfo("Break Complete", "Break time is over! Ready for another work session?")
    
    self.start_button.config(text="Start", state="normal")
    self.pause_button.config(state="normal")
    self.reset_for_new_session()
```

**Line 497**: `self.is_running = False`
- Immediately stops timer upon completion

**Lines 499-500**: Audio notification
- Plays sound if user has enabled notifications

**Lines 502-515**: Work session completion handling
- Increments pomodoro and session counters
- Uses modulo arithmetic to determine break type
- `session_count % long_break_interval == 0`: Every Nth session triggers long break

**Lines 507-512**: Automatic vs manual progression
- If auto-start enabled: automatically begins break after 1-second delay
- If manual: shows dialog and waits for user confirmation

**Lines 514-522**: Break session completion handling
- Always returns to work session after any break
- Similar auto/manual progression logic

**Lines 524-526**: State restoration
- Resets button states for next session
- Calls `reset_for_new_session()` to prepare display

### Session Preparation (reset_for_new_session) (Lines 529-541)

```python
def reset_for_new_session(self):
    """
    Configure Timer for Next Session Type
    ...
    """
    if self.current_session == "Work":
        self.time_left = self.work_duration.get() * 60
    elif self.current_session == "Short Break":
        self.time_left = self.short_break_duration.get() * 60
    else:  # Long Break
        self.time_left = self.long_break_duration.get() * 60
        
    self.total_time = self.time_left
    self.update_display()
```

**Lines 535-540**: Duration assignment logic
- Sets appropriate duration based on current session type
- Uses current user settings (may have been modified)

**Line 542**: `self.total_time = self.time_left`
- Stores total for progress calculation

**Line 543**: `self.update_display()`
- Updates all display elements with new session information

### Audio Notification System (play_notification_sound) (Lines 545-564)

```python
def play_notification_sound(self):
    """
    Generate and Play Audio Notification
    ...
    """
    try:
        sample_rate = 22050
        duration = 0.5
        frequency = 800
        
        import numpy as np
        frames = int(duration * sample_rate)
        arr = np.zeros(frames)
        for i in range(frames):
            arr[i] = np.sin(2 * np.pi * frequency * i / sample_rate)
        
        arr = (arr * 32767).astype(np.int16)
        sound = pygame.sndarray.make_sound(np.array([arr, arr]).T)
        sound.play()
    except:
        print("\a")
```

**Lines 551-553**: Audio parameters
- `sample_rate = 22050`: CD-quality sample rate (Hz)
- `duration = 0.5`: Half-second notification (non-intrusive)
- `frequency = 800`: Pleasant, attention-getting tone (Hz)

**Line 556**: `frames = int(duration * sample_rate)`
- Calculates total number of audio samples needed

**Line 557**: `arr = np.zeros(frames)`
- Creates empty numpy array for audio data

**Lines 558-559**: Sine wave generation
- Mathematical formula: `sin(2π * frequency * time)`
- Creates pure tone at specified frequency

**Line 561**: `arr = (arr * 32767).astype(np.int16)`
- Converts floating-point audio to 16-bit signed integer
- Scales to full 16-bit range for proper volume

**Line 562**: `sound = pygame.sndarray.make_sound(np.array([arr, arr]).T)`
- Creates stereo sound (duplicates mono channel for left/right)
- `.T` transposes array for pygame compatibility

**Line 563**: `sound.play()`
- Plays sound non-blocking (doesn't pause program)

**Line 565**: `print("\a")`
- Fallback system beep if audio generation fails
- ASCII bell character triggers system notification sound

### Display Update System (update_display) (Lines 566-586)

```python
def update_display(self):
    """
    Refresh All GUI Elements with Current State
    ...
    """
    minutes = self.time_left // 60
    seconds = self.time_left % 60
    time_text = f"{minutes:02d}:{seconds:02d}"
    self.time_label.config(text=time_text)
    
    session_colors = {
        "Work": "#e74c3c",
        "Short Break": "#f39c12",
        "Long Break": "#9b59b6"
    }
    
    self.session_label.config(
        text=f"{self.current_session}",
        fg=session_colors.get(self.current_session, "#ecf0f1")
    )
    
    if self.total_time > 0:
        progress = ((self.total_time - self.time_left) / self.total_time) * 100
        self.progress['value'] = progress
```

**Lines 572-575**: Time formatting
- `//` : Integer division for minutes
- `%` : Modulo for remaining seconds
- `f"{minutes:02d}:{seconds:02d}"`: Zero-padded MM:SS format

**Lines 577-581**: Color coding system
- Work: Red (#e74c3c) - Focus/concentration
- Short Break: Orange (#f39c12) - Brief rest
- Long Break: Purple (#9b59b6) - Extended restoration

**Lines 583-586**: Session label update
- Updates text and color based on current session
- `.get(key, default)`: Returns default color if session type not found

**Lines 588-590**: Progress bar update
- Calculates completion percentage: `(total - remaining) / total * 100`
- `if self.total_time > 0`: Prevents division by zero error

### Responsive Design System (Lines 588-633)

#### Responsive Value Calculation (Lines 588-618)

```python
def calculate_responsive_values(self):
    """
    Calculate responsive font sizes and spacing based on current window size
    ...
    """
    current_width = self.root.winfo_width()
    current_height = self.root.winfo_height()
    
    # Calculate scaling factors
    width_scale = max(0.8, min(1.5, current_width / self.base_width))
    height_scale = max(0.8, min(1.5, current_height / self.base_height))
    
    # Font sizes (timer stays at 48)
    self.title_font_size = max(16, int(24 * width_scale))
    self.session_font_size = max(12, int(16 * width_scale))
    self.timer_font_size = 48  # Always fixed for optimal readability
    self.button_font_size = max(10, int(12 * width_scale))
    
    # Spacing values
    self.title_pady = max(10, int(15 * height_scale))
    self.session_pady = max(5, int(8 * height_scale))
    self.timer_pady = max(15, int(20 * height_scale))
    self.progress_pady = max(8, int(10 * height_scale))
    self.controls_pady = max(15, int(18 * height_scale))
    self.settings_pady = max(8, int(10 * height_scale))
    
    # Progress bar length
    self.progress_length = max(250, int(300 * width_scale))
```

**Lines 594-595**: Current window dimensions
- `winfo_width()`: Gets current window width in pixels
- `winfo_height()`: Gets current window height in pixels

**Lines 598-599**: Scaling factor calculation
- Divides current size by base size to get ratio
- `max(0.8, min(1.5, ratio))`: Clamps scaling between 80%-150%
- Prevents fonts from becoming too small or too large

**Lines 602-605**: Font size calculation
- Each font has base size multiplied by scale factor
- `max(minimum, scaled_size)`: Ensures minimum readability
- Timer font stays fixed at 48pt for optimal visibility

**Lines 608-613**: Spacing calculation
- Vertical padding scales with height changes
- Maintains proportional spacing as window resizes

**Line 616**: Progress bar length
- Scales horizontally with window width
- Minimum 250px ensures usability

#### Window Resize Handler (Lines 620-627)

```python
def on_window_resize(self, event):
    """
    Handle window resize events for responsive design
    ...
    """
    if event.widget == self.root:
        self.calculate_responsive_values()
        self.update_widget_styling()
```

**Line 625**: `if event.widget == self.root:`
- Only responds to main window resize events
- Ignores resize events from child widgets

**Lines 626-627**: Response sequence
- Recalculates responsive values based on new size
- Applies new values to existing widgets

#### Widget Styling Update (Lines 629-653)

```python
def update_widget_styling(self):
    """
    Update widget fonts and spacing based on current responsive values
    ...
    """
    try:
        # Update fonts
        self.title_label.config(font=("Arial", self.title_font_size, "bold"))
        self.session_label.config(font=("Arial", self.session_font_size))
        self.time_label.config(font=("Arial", self.timer_font_size, "bold"))
        
        self.start_button.config(font=("Arial", self.button_font_size, "bold"))
        self.pause_button.config(font=("Arial", self.button_font_size, "bold"))
        self.reset_button.config(font=("Arial", self.button_font_size, "bold"))
        
        self.settings_button.config(font=("Arial", self.button_font_size))
        
        # Update progress bar length
        self.progress.config(length=self.progress_length)
    except AttributeError:
        # Widgets not created yet
        pass
```

**Lines 636-643**: Font updates
- Applies newly calculated font sizes to all text widgets
- Maintains font family (Arial) and weights (bold where appropriate)

**Line 646**: Progress bar update
- Applies new responsive length

**Lines 647-649**: Error handling
- `except AttributeError`: Handles case where widgets don't exist yet
- Occurs during initial startup before widgets are created
- `pass`: Silently ignores error and continues

### Application Entry Point (Lines 655-667)

```python
def main():
    """
    Application Entry Point and Main Loop Initialization
    ...
    """
    root = tk.Tk()
    app = PomodoroTimer(root)
    root.mainloop()

if __name__ == "__main__":
    main()
```

**Line 660**: `root = tk.Tk()`
- Creates main tkinter window object
- This is the root window for the entire application

**Line 661**: `app = PomodoroTimer(root)`
- Creates PomodoroTimer instance
- Passes root window to constructor
- Triggers complete application initialization

**Line 662**: `root.mainloop()`
- Starts tkinter event loop (blocking call)
- Handles all GUI events (clicks, resize, etc.)
- Continues until user closes window

**Lines 664-665**: Script execution guard
- `if __name__ == "__main__":`: Only runs main() when script executed directly
- Prevents execution when module is imported
- Standard Python idiom for executable scripts

---

## Architecture Summary

### Model-View-Controller Pattern

**Model (Data & State)**:
- Timer state variables (`is_running`, `is_paused`, `time_left`)
- User settings (`work_duration`, `sound_enabled`, etc.)
- Session tracking (`current_session`, `session_count`)

**View (User Interface)**:
- GUI widgets (labels, buttons, progress bar)
- Responsive design system
- Visual feedback and color coding

**Controller (Logic & Events)**:
- Event handlers (button clicks, window resize)
- Timer logic and session management
- Audio notifications and user preferences

### Threading Architecture

**Main Thread**:
- GUI event handling and updates
- User interaction processing
- Window management

**Timer Thread**:
- Countdown loop execution
- Non-blocking timer operation
- Thread-safe communication via `root.after()`

### Key Design Patterns

**Observer Pattern**: tkinter variables automatically sync with GUI widgets
**Command Pattern**: Button commands connected to specific methods
**Singleton Pattern**: Single application instance with centralized state
**Strategy Pattern**: Different timer modes (Classic vs Focus) with same interface

This comprehensive documentation covers every aspect of the Pomodoro timer implementation, from low-level technical details to high-level architectural decisions.