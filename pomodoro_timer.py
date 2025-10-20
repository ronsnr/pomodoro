"""
POMODORO TIMER GUI APPLICATION - EDUCATIONAL VERSION FOR PYTHON BEGINNERS

🍅 LEARNING GOALS FOR NEW PYTHON PROGRAMMERS:
==================================================
This application will teach you:

1. OBJECT-ORIENTED PROGRAMMING (OOP):
   - How to create classes and methods
   - Instance variables (self.variable_name)
   - How methods work together to create functionality

2. GUI PROGRAMMING WITH TKINTER:
   - Creating windows, buttons, labels
   - Event handling (what happens when user clicks)
   - Layout management (organizing widgets on screen)

3. THREADING AND CONCURRENCY:
   - Running timer in background without freezing GUI
   - Thread-safe communication between processes

4. EVENT-DRIVEN PROGRAMMING:
   - Responding to user actions (clicks, window resize)
   - Callback functions and event binding

5. STATE MANAGEMENT:
   - Tracking application state (running, paused, etc.)
   - Coordinating multiple variables to work together

6. PYTHON BEST PRACTICES:
   - Code organization and documentation
   - Error handling with try/except
   - Using built-in data types effectively

This application implements the Pomodoro Technique - a time management method that uses 
a timer to break down work into intervals (traditionally 25 minutes) separated by short breaks.

Key Features:
- Customizable work and break durations
- Visual progress tracking with progress bar
- Audio notifications when sessions complete
- Automatic session progression (work → break → work)
- Multiple timer modes (Classic 25/5/15, Focus 45/10/30)
- Pause/resume functionality
- Auto-start options for breaks and work sessions
- Responsive design that adapts to window resizing

Dependencies (External Libraries We Need):
- tkinter: GUI framework (built into Python - no installation needed!)
- pygame: Audio notification system (pip install pygame)
- numpy: Sound wave generation (pip install numpy)
- threading: Non-blocking timer execution (built into Python)
- time: Timer countdown functionality (built into Python)

Author: GitHub Copilot
Date: October 2025
"""

# ============================================================================
# IMPORT STATEMENTS - BRINGING IN THE TOOLS WE NEED
# ============================================================================

# PYTHON LEARNING TIP: Import statements bring in code from other modules
# Think of them like borrowing tools from a toolbox

import tkinter as tk                    # Main GUI toolkit - "tk" is a shorter nickname
from tkinter import ttk, messagebox     # Special widgets (ttk) and popup dialogs (messagebox)
import time                             # For time-related functions like sleep()
import threading                        # For running timer in background
import pygame                           # For playing notification sounds
import os                               # Operating system interface (not used but imported)
from datetime import datetime, timedelta  # Date/time utilities (not used but imported)

# ============================================================================
# MAIN APPLICATION CLASS - THE HEART OF OUR PROGRAM
# ============================================================================

class PomodoroTimer:
    """
    🎯 PYTHON LEARNING: Understanding Classes
    ==========================================
    
    A CLASS is like a blueprint for creating objects. Think of it like:
    - A recipe for making cookies (class = recipe, cookies = objects)
    - A blueprint for building houses (class = blueprint, houses = objects)
    
    In our case:
    - PomodoroTimer class = blueprint for timer applications
    - Each timer we create = an object made from this blueprint
    
    INSTANCE VARIABLES (self.variable_name):
    - These belong to each specific object
    - Each timer object has its own set of variables
    - "self" refers to the current object instance
    
    METHODS (def function_name):
    - These are functions that belong to the class
    - They define what objects can DO
    - Like start_timer(), pause_timer(), etc.
    
    This class handles the complete Pomodoro timer functionality including:
    - GUI creation and management (what the user sees)
    - Timer logic and state management (keeping track of time and status)
    - User settings and preferences (remembering user choices)
    - Audio notifications (playing sounds)
    - Session tracking (counting completed work sessions)
    """
    
    def __init__(self, root):
        """
        🔧 PYTHON LEARNING: The Constructor Method (__init__)
        ====================================================
        
        __init__ is a SPECIAL METHOD called automatically when creating a new object.
        It's like the "setup instructions" that run when you build something new.
        
        WHAT HAPPENS HERE:
        1. Set up the main window appearance
        2. Initialize all our tracking variables
        3. Configure the audio system
        4. Create the user interface
        5. Start with everything in the "ready" state
        
        PARAMETERS:
        - self: Reference to the object being created (Python adds this automatically)
        - root: The main window object passed in from outside
        
        PYTHON TIP: Notice how we store root as self.root - this lets other methods 
        in this class access the window object later!
        """
        
        # ═══════════════════════════════════════════════════════════════
        # WINDOW SETUP AND CONFIGURATION
        # ═══════════════════════════════════════════════════════════════
        
        # Store the main window reference so other methods can use it
        # PYTHON LEARNING: self.variable_name creates an instance variable
        self.root = root
        
        # Set the window title (what appears in the title bar)
        # 🍅 emoji makes it easy to spot in the taskbar!
        self.root.title("🍅 Pomodoro Timer")
        
        # Set window size: width x height in pixels
        # PYTHON LEARNING: Strings with numbers become method arguments
        self.root.geometry("500x480")
        
        # Set minimum window size (prevents user from making it too small)
        self.root.minsize(400, 400)
        
        # Set background color using hex color code
        # PYTHON LEARNING: #2c3e50 is a dark blue-gray color in hexadecimal
        self.root.configure(bg="#2c3e50")
        
        # Make window stay on top of other applications
        # This ensures timer remains visible while working
        # PYTHON LEARNING: attributes() method sets special window properties
        self.root.attributes('-topmost', True)
        
        # Store reference dimensions for responsive design calculations
        # PYTHON LEARNING: These help us scale the interface when window is resized
        self.base_width = 500   # Our "standard" width
        self.base_height = 480  # Our "standard" height
        
        # ═══════════════════════════════════════════════════════════════
        # AUDIO SYSTEM INITIALIZATION
        # ═══════════════════════════════════════════════════════════════
        
        # Initialize pygame's sound system
        # PYTHON LEARNING: Some libraries need to be "initialized" before use
        pygame.mixer.init()
        
        # ═══════════════════════════════════════════════════════════════
        # TIMER STATE VARIABLES - KEEPING TRACK OF WHAT'S HAPPENING
        # ═══════════════════════════════════════════════════════════════
        
        # PYTHON LEARNING: Boolean variables can only be True or False
        # These act like on/off switches for different states
        
        self.is_running = False    # Is the timer currently counting down?
        self.is_paused = False     # Is the timer paused (but not reset)?
        
        # PYTHON LEARNING: Strings store text data
        # This tracks what type of session we're in
        self.current_session = "Work"    # Can be "Work", "Short Break", or "Long Break"
        
        # PYTHON LEARNING: Integer variables store whole numbers
        # These track time and session information
        self.time_left = 0              # Seconds remaining in current session
        self.total_time = 0             # Total seconds in current session (for progress bar)
        self.session_count = 0          # How many work sessions completed
        self.completed_pomodoros = 0    # Total pomodoros finished
        
        # ═══════════════════════════════════════════════════════════════
        # TIMER SETTINGS - USER CUSTOMIZABLE VALUES
        # ═══════════════════════════════════════════════════════════════
        
        # PYTHON LEARNING: tkinter Variables
        # These special variable types automatically sync with GUI widgets
        # When user changes a spinbox, the variable updates automatically!
        
        # IntVar stores integer values and syncs with spinbox widgets
        self.work_duration = tk.IntVar(value=25)         # Work session length (minutes)
        self.short_break_duration = tk.IntVar(value=5)   # Short break length (minutes)
        self.long_break_duration = tk.IntVar(value=15)   # Long break length (minutes)
        self.long_break_interval = tk.IntVar(value=4)    # Work sessions before long break
        
        # BooleanVar stores True/False values and syncs with checkbox widgets
        self.sound_enabled = tk.BooleanVar(value=True)        # Play sounds when sessions end?
        self.auto_start_breaks = tk.BooleanVar(value=False)   # Automatically start breaks?
        self.auto_start_work = tk.BooleanVar(value=False)     # Automatically start work?
        
        # ═══════════════════════════════════════════════════════════════
        # EVENT BINDING AND FINAL SETUP
        # ═══════════════════════════════════════════════════════════════
        
        # PYTHON LEARNING: Event Binding
        # This connects window events (like resizing) to our functions
        # When user resizes window, on_window_resize() will be called
        self.root.bind('<Configure>', self.on_window_resize)
        
        # Build the user interface (all the buttons, labels, etc.)
        # PYTHON LEARNING: We separate this into its own method for organization
        self.create_widgets()
        
        # Update the display to show initial values
        # PYTHON LEARNING: Always good to start with everything in sync
        self.update_display()
        
    def create_widgets(self):
        """
        🎨 PYTHON LEARNING: GUI Creation and Layout Management
        =====================================================
        
        This method builds all the visual elements (widgets) that users interact with.
        
        KEY GUI CONCEPTS:
        
        1. WIDGETS: Visual elements like buttons, labels, text boxes
        2. CONTAINERS: Frames that hold and organize other widgets
        3. LAYOUT MANAGERS: Systems that position widgets (pack, grid, place)
        4. EVENT HANDLING: Connecting user actions to code functions
        
        LAYOUT STRATEGY:
        - Use Frame containers to group related widgets
        - Use pack() layout manager for flexible positioning
        - Calculate responsive sizes based on window dimensions
        - Apply consistent styling with colors and fonts
        
        WIDGET HIERARCHY (parent → child relationships):
        root window
        └── main_container (Frame)
            ├── title_label (Label)
            ├── session_label (Label)  
            ├── timer_container (Frame)
            │   └── time_label (Label)
            ├── progress_container (Frame)
            │   └── progress (Progressbar)
            ├── control_frame (Frame)
            │   ├── start_button (Button)
            │   ├── pause_button (Button)
            │   └── reset_button (Button)
            └── settings_container (Frame)
                └── settings_button (Button)
        """
        
        # ═══════════════════════════════════════════════════════════════
        # RESPONSIVE DESIGN CALCULATION
        # ═══════════════════════════════════════════════════════════════
        
        # Calculate font sizes and spacing based on current window size
        # PYTHON LEARNING: This makes the interface adapt to different window sizes
        self.calculate_responsive_values()
        
        # ═══════════════════════════════════════════════════════════════
        # MAIN CONTAINER FRAME
        # ═══════════════════════════════════════════════════════════════
        
        # Create the main container that holds all other widgets
        # PYTHON LEARNING: Frame widgets are like invisible boxes for organization
        main_container = tk.Frame(
            self.root,              # Parent widget (the main window)
            bg="#2c3e50"           # Background color (same as window)
        )
        
        # Position the container in the window
        # PYTHON LEARNING: pack() is a layout manager that automatically positions widgets
        main_container.pack(
            fill=tk.BOTH,          # Expand to fill available space in both directions
            expand=True,           # Allow container to grow when window is resized
            padx=10,              # 10 pixels of padding on left and right
            pady=5                # 5 pixels of padding on top and bottom
        )
        
        # ═══════════════════════════════════════════════════════════════
        # TITLE LABEL - "🍅 Pomodoro Timer"
        # ═══════════════════════════════════════════════════════════════
        
        # PYTHON LEARNING: Labels display text that users can see but not edit
        self.title_label = tk.Label(
            main_container,                                        # Parent container
            text="🍅 Pomodoro Timer",                             # Text to display
            font=("Arial", self.title_font_size, "bold"),        # Font: family, size, style
            bg="#2c3e50",                                         # Background color
            fg="#ecf0f1"                                          # Foreground (text) color
        )
        
        # Position the title at the top
        # PYTHON LEARNING: pady adds vertical spacing around the widget
        self.title_label.pack(pady=self.title_pady)
        
        # ═══════════════════════════════════════════════════════════════
        # SESSION TYPE LABEL - "Work Session", "Break", etc.
        # ═══════════════════════════════════════════════════════════════
        
        self.session_label = tk.Label(
            main_container,
            text="Work Session",                                  # Initial text
            font=("Arial", self.session_font_size),              # Responsive font size
            bg="#2c3e50",                                         # Dark background
            fg="#e74c3c"                                          # Red text color for work
        )
        
        # PYTHON LEARNING: We'll change the text and color of this label
        # dynamically as the session type changes
        self.session_label.pack(pady=self.session_pady)
        
        # ═══════════════════════════════════════════════════════════════
        # TIMER DISPLAY CONTAINER - PREVENTS JUMPING
        # ═══════════════════════════════════════════════════════════════
        
        # Create a fixed-height container for the timer display
        # PYTHON LEARNING: This prevents the layout from "jumping" when time changes
        timer_container = tk.Frame(
            main_container,
            bg="#2c3e50",          # Same background as parent
            height=80              # Fixed height in pixels
        )
        
        # Position the container
        timer_container.pack(
            pady=self.timer_pady,  # Responsive vertical spacing
            fill=tk.X              # Expand horizontally to full width
        )
        
        # PYTHON LEARNING: pack_propagate(False) prevents container from shrinking
        # Without this, the container would resize based on its contents
        timer_container.pack_propagate(False)
        
        # ═══════════════════════════════════════════════════════════════
        # TIME DISPLAY LABEL - "25:00"
        # ═══════════════════════════════════════════════════════════════
        
        self.time_label = tk.Label(
            timer_container,                                      # Parent is the fixed container
            text="25:00",                                        # Initial time display
            font=("Arial", self.timer_font_size, "bold"),       # Large, bold font
            bg="#2c3e50",                                        # Dark background
            fg="#ecf0f1"                                         # Light text color
        )
        
        # Center the time display vertically in its container
        # PYTHON LEARNING: expand=True centers the widget in available space
        self.time_label.pack(expand=True)
        
        # ═══════════════════════════════════════════════════════════════
        # PROGRESS BAR CONTAINER
        # ═══════════════════════════════════════════════════════════════
        
        # Container for centering the progress bar
        progress_container = tk.Frame(main_container, bg="#2c3e50")
        progress_container.pack(
            pady=self.progress_pady,    # Responsive spacing
            fill=tk.X                   # Expand horizontally
        )
        
        # PYTHON LEARNING: ttk widgets have a more modern appearance than basic tk widgets
        self.progress = ttk.Progressbar(
            progress_container,
            length=self.progress_length,    # Responsive width
            mode='determinate'              # Shows specific percentage (0-100%)
        )
        
        # Center the progress bar in its container
        self.progress.pack()
        
        # ═══════════════════════════════════════════════════════════════
        # CONTROL BUTTONS FRAME
        # ═══════════════════════════════════════════════════════════════
        
        # Container for the Start/Pause/Reset buttons
        control_frame = tk.Frame(main_container, bg="#2c3e50")
        control_frame.pack(pady=self.controls_pady)
        
        # Calculate responsive button width
        # PYTHON LEARNING: max() ensures minimum width, int() converts to whole number
        button_width = max(8, int(10 * (self.root.winfo_width() / self.base_width)))
        
        # ═══════════════════════════════════════════════════════════════
        # START BUTTON - GREEN "START" BUTTON
        # ═══════════════════════════════════════════════════════════════
        
        # PYTHON LEARNING: Buttons respond to clicks and run functions
        self.start_button = tk.Button(
            control_frame,                                  # Parent container
            text="Start",                                   # Button label
            font=("Arial", self.button_font_size, "bold"), # Font styling
            bg="#27ae60",                                   # Green background (go/start color)
            fg="white",                                     # White text
            width=button_width,                             # Responsive width
            command=self.start_timer                        # Function to call when clicked
        )
        
        # Position button on the left side with spacing
        # PYTHON LEARNING: side=tk.LEFT makes buttons line up horizontally
        self.start_button.pack(side=tk.LEFT, padx=8)
        
        # ═══════════════════════════════════════════════════════════════
        # PAUSE BUTTON - ORANGE "PAUSE" BUTTON
        # ═══════════════════════════════════════════════════════════════
        
        self.pause_button = tk.Button(
            control_frame,
            text="Pause",
            font=("Arial", self.button_font_size, "bold"),
            bg="#f39c12",                                   # Orange background (caution/pause color)
            fg="white",
            width=button_width,
            command=self.pause_timer                        # Different function for pause
        )
        
        self.pause_button.pack(side=tk.LEFT, padx=8)
        
        # ═══════════════════════════════════════════════════════════════
        # RESET BUTTON - RED "RESET" BUTTON
        # ═══════════════════════════════════════════════════════════════
        
        self.reset_button = tk.Button(
            control_frame,
            text="Reset",
            font=("Arial", self.button_font_size, "bold"),
            bg="#e74c3c",                                   # Red background (stop/danger color)
            fg="white",
            width=button_width,
            command=self.reset_timer                        # Different function for reset
        )
        
        self.reset_button.pack(side=tk.LEFT, padx=8)
        
        # ═══════════════════════════════════════════════════════════════
        # SETTINGS BUTTON CONTAINER
        # ═══════════════════════════════════════════════════════════════
        
        # Container positioned at bottom of main container
        settings_container = tk.Frame(main_container, bg="#2c3e50")
        settings_container.pack(
            pady=self.settings_pady,    # Responsive spacing
            side=tk.BOTTOM,             # Position at bottom
            fill=tk.X                   # Expand horizontally
        )
        
        # ═══════════════════════════════════════════════════════════════
        # SETTINGS BUTTON - PURPLE GEAR BUTTON
        # ═══════════════════════════════════════════════════════════════
        
        self.settings_button = tk.Button(
            settings_container,
            text="⚙️ Settings",                             # Gear emoji + text
            font=("Arial", self.button_font_size),
            bg="#9b59b6",                                   # Purple background (settings color)
            fg="white",
            command=self.open_settings                      # Opens settings window
        )
        
        # Center the settings button
        self.settings_button.pack()

    def create_settings_window(self):
        """
        Create Advanced Settings Configuration Window
        
        Purpose: Provides a comprehensive interface for customizing all timer parameters,
        automation options, and user preferences. This window opens as a modal dialog
        when the settings button is clicked.
        """
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Pomodoro Settings")
        settings_window.geometry("400x500")
        settings_window.configure(bg="#2c3e50")
        
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
        
        # Short break duration
        tk.Label(duration_frame, text="Short Break:", bg="#34495e", fg="#ecf0f1").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        short_break_spinbox = tk.Spinbox(duration_frame, from_=1, to=30, textvariable=self.short_break_duration, width=10)
        short_break_spinbox.grid(row=1, column=1, padx=5, pady=5)
        
        # Long break duration
        tk.Label(duration_frame, text="Long Break:", bg="#34495e", fg="#ecf0f1").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        long_break_spinbox = tk.Spinbox(duration_frame, from_=1, to=60, textvariable=self.long_break_duration, width=10)
        long_break_spinbox.grid(row=2, column=1, padx=5, pady=5)
        
        # Long break interval
        tk.Label(duration_frame, text="Long Break Interval:", bg="#34495e", fg="#ecf0f1").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        interval_spinbox = tk.Spinbox(duration_frame, from_=2, to=10, textvariable=self.long_break_interval, width=10)
        interval_spinbox.grid(row=3, column=1, padx=5, pady=5)
        
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
        
        auto_break_check = tk.Checkbutton(
            options_frame,
            text="Auto-start breaks",
            variable=self.auto_start_breaks,
            bg="#34495e",
            fg="#ecf0f1",
            selectcolor="#2c3e50"
        )
        auto_break_check.pack(anchor="w", padx=5, pady=5)
        
        auto_work_check = tk.Checkbutton(
            options_frame,
            text="Auto-start work sessions",
            variable=self.auto_start_work,
            bg="#34495e",
            fg="#ecf0f1",
            selectcolor="#2c3e50"
        )
        auto_work_check.pack(anchor="w", padx=5, pady=5)
        
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
        
        focus_button = tk.Button(
            mode_buttons_frame,
            text="Focus Mode",
            bg="#8e44ad",
            fg="white",
            command=lambda: self.set_focus_mode()
        )
        focus_button.pack(side=tk.LEFT, padx=5)
        
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
        
        cancel_button = tk.Button(
            button_frame,
            text="Cancel",
            bg="#e74c3c",
            fg="white",
            command=settings_window.destroy
        )
        cancel_button.pack(side=tk.LEFT, padx=5)
        
    def set_classic_mode(self):
        """
        Configure Classic Pomodoro Technique Settings
        
        Purpose: Instantly applies the traditional Pomodoro Technique intervals
        as defined by Francesco Cirillo. This is the most widely used configuration.
        """
        self.work_duration.set(25)
        self.short_break_duration.set(5)
        self.long_break_duration.set(15)
        self.long_break_interval.set(4)
        
    def set_focus_mode(self):
        """
        Configure Extended Focus Mode Settings
        
        Purpose: Applies longer intervals designed for deep work sessions
        that require sustained concentration and minimal interruption.
        """
        self.work_duration.set(45)
        self.short_break_duration.set(10)
        self.long_break_duration.set(30)
        self.long_break_interval.set(3)
        
    def open_settings(self):
        """
        Launch Settings Configuration Window
        
        Purpose: Creates and displays the settings window when user clicks
        the settings button.
        """
        self.create_settings_window()
        
    def save_settings(self):
        """
        Save User Configuration and Update Timer Display
        
        Purpose: Applies all user-modified settings and refreshes the timer
        display to reflect new configurations.
        """
        if not self.is_running:
            self.reset_timer()
        messagebox.showinfo("Settings", "Settings saved successfully!")
        
    def start_timer(self):
        """
        🚀 PYTHON LEARNING: Timer Control and Threading
        ==============================================
        
        This method handles starting or resuming the timer. It demonstrates several
        important Python concepts:
        
        1. CONDITIONAL LOGIC: Using if/elif/else to make decisions
        2. THREADING: Running tasks in the background
        3. STATE MANAGEMENT: Coordinating multiple variables
        4. METHOD CALLS: How methods work together
        
        WHAT HAPPENS WHEN USER CLICKS START:
        1. Check if we're starting fresh or resuming
        2. If starting fresh, calculate time based on session type
        3. Update button states to show timer is running
        4. Create and start a background thread for countdown
        
        WHY USE THREADING:
        - GUI runs on main thread (handles user clicks, updates display)
        - Timer countdown runs on separate thread (counts seconds)
        - This prevents GUI from "freezing" during countdown
        """
        
        # ═══════════════════════════════════════════════════════════════
        # DETERMINE SESSION DURATION (ONLY IF STARTING FRESH)
        # ═══════════════════════════════════════════════════════════════
        
        # PYTHON LEARNING: Conditional Logic (if/elif/else)
        # Check if we're starting a brand new session (not resuming a pause)
        if not self.is_running and not self.is_paused:
            
            # PYTHON LEARNING: Dictionary-like logic using if/elif
            # Determine how many seconds based on current session type
            if self.current_session == "Work":
                # Get user's work duration setting and convert minutes to seconds
                # PYTHON LEARNING: .get() method retrieves value from tkinter variable
                self.time_left = self.work_duration.get() * 60
                
            elif self.current_session == "Short Break":
                self.time_left = self.short_break_duration.get() * 60
                
            else:  # Must be "Long Break"
                # PYTHON LEARNING: else clause handles remaining cases
                self.time_left = self.long_break_duration.get() * 60
            
            # Store total time for progress bar calculation
            # PYTHON LEARNING: We need this reference because time_left will decrease
            self.total_time = self.time_left
            
        # ═══════════════════════════════════════════════════════════════
        # UPDATE TIMER STATE AND BUTTON APPEARANCE
        # ═══════════════════════════════════════════════════════════════
        
        # Set state flags to indicate timer is active
        # PYTHON LEARNING: Boolean variables act like switches
        self.is_running = True      # Timer is counting down
        self.is_paused = False      # Clear any previous pause state
        
        # Update start button to show timer is running
        # PYTHON LEARNING: .config() method changes widget properties after creation
        self.start_button.config(
            text="Running...",      # Change button text
            state="disabled"        # Disable button to prevent double-clicking
        )
        
        # ═══════════════════════════════════════════════════════════════
        # CREATE AND START BACKGROUND TIMER THREAD
        # ═══════════════════════════════════════════════════════════════
        
        # PYTHON LEARNING: Threading - Running Code in the Background
        # Create a new thread that will run our timer countdown
        timer_thread = threading.Thread(
            target=self.run_timer    # Function to run in the background
        )
        
        # PYTHON LEARNING: Daemon Threads
        # daemon=True means thread will automatically close when main program exits
        # Without this, program might not close properly
        timer_thread.daemon = True
        
        # Start the background thread (begins countdown)
        # PYTHON LEARNING: .start() method begins thread execution
        timer_thread.start()
        
    def pause_timer(self):
        """
        ⏸️ PYTHON LEARNING: State Management and User Interaction
        ========================================================
        
        This method pauses the timer without losing progress. It shows:
        
        1. CONDITIONAL EXECUTION: Only pause if timer is running
        2. STATE UPDATES: Changing multiple related variables together
        3. UI SYNCHRONIZATION: Keeping buttons in sync with state
        4. PRESERVE DATA: Maintaining progress for later resume
        
        PAUSE vs RESET:
        - Pause: Stops countdown but remembers time_left
        - Reset: Stops countdown and sets time back to beginning
        """
        
        # Only allow pausing if timer is currently running
        # PYTHON LEARNING: Guard clause - exit early if condition not met
        if self.is_running:
            
            # Update state flags
            # PYTHON LEARNING: Notice we set paused BEFORE clearing running
            self.is_paused = True       # Remember we're paused (for resume)
            self.is_running = False     # Stop the countdown loop
            
            # Update button states to reflect paused condition
            # PYTHON LEARNING: Multiple widget updates to keep UI consistent
            self.start_button.config(
                text="Resume",          # Button now says "Resume" instead of "Start"
                state="normal"          # Re-enable button for clicking
            )
            
            self.pause_button.config(
                state="disabled"        # Disable pause button (already paused!)
            )
        
    def reset_timer(self):
        """
        🔄 PYTHON LEARNING: Complete State Reset and Method Coordination
        ==============================================================
        
        This method completely resets the timer to its initial state. It demonstrates:
        
        1. COMPREHENSIVE STATE MANAGEMENT: Resetting all related variables
        2. METHOD COORDINATION: Calling other methods to update display
        3. UI RESTORATION: Returning buttons to initial appearance
        4. DEFAULT VALUES: Setting everything back to starting conditions
        
        RESET PROCESS:
        1. Stop any running timer
        2. Clear all state flags
        3. Return to "Work" session
        4. Reset time to current work duration
        5. Restore button states
        6. Update display to show changes
        """
        
        # ═══════════════════════════════════════════════════════════════
        # STOP ALL TIMER ACTIVITY
        # ═══════════════════════════════════════════════════════════════
        
        # Clear all running/paused states
        # PYTHON LEARNING: Always good to be explicit about state changes
        self.is_running = False     # Stop countdown if running
        self.is_paused = False      # Clear pause state
        
        # ═══════════════════════════════════════════════════════════════
        # RESET TO INITIAL SESSION STATE
        # ═══════════════════════════════════════════════════════════════
        
        # Always return to work session after reset
        # PYTHON LEARNING: String assignment changes the session type
        self.current_session = "Work"
        
        # Reset time to current work duration setting
        # PYTHON LEARNING: This uses current user settings (might have changed!)
        self.time_left = self.work_duration.get() * 60
        self.total_time = self.time_left
        
        # ═══════════════════════════════════════════════════════════════
        # RESTORE BUTTON STATES TO INITIAL APPEARANCE
        # ═══════════════════════════════════════════════════════════════
        
        # Reset start button to initial state
        self.start_button.config(
            text="Start",           # Back to original text
            state="normal"          # Re-enable for clicking
        )
        
        # Reset pause button to initial state
        self.pause_button.config(
            state="normal"          # Re-enable for clicking
        )
        
        # ═══════════════════════════════════════════════════════════════
        # UPDATE DISPLAY TO REFLECT RESET STATE
        # ═══════════════════════════════════════════════════════════════
        
        # PYTHON LEARNING: Method calls - using other methods in our class
        # This updates all the visual elements to show the reset state
        self.update_display()
        
    def run_timer(self):
        """
        ⏰ PYTHON LEARNING: Threading, Loops, and Thread-Safe Communication
        ==================================================================
        
        This is the CORE TIMER ENGINE that runs in a background thread. It shows:
        
        1. WHILE LOOPS: Repeating code while a condition is true
        2. SLEEP FUNCTION: Pausing execution for precise timing
        3. THREAD SAFETY: Safely communicating between threads
        4. LOOP CONDITIONS: Using multiple conditions to control loops
        
        BACKGROUND THREAD CONCEPTS:
        - This function runs separately from the main GUI
        - It counts down seconds without freezing the interface
        - Uses root.after() to safely update GUI from background thread
        - Exits cleanly when timer completes or is stopped
        
        THREAD SAFETY:
        - Never update GUI directly from background thread
        - Use root.after() to schedule GUI updates on main thread
        - This prevents crashes and display issues
        """
        
        # ═══════════════════════════════════════════════════════════════
        # MAIN COUNTDOWN LOOP
        # ═══════════════════════════════════════════════════════════════
        
        # PYTHON LEARNING: while loop with multiple conditions
        # Continue looping while BOTH conditions are true:
        # 1. time_left > 0 (still have time remaining)
        # 2. self.is_running (timer hasn't been paused/stopped)
        while self.time_left > 0 and self.is_running:
            
            # PYTHON LEARNING: time.sleep() pauses execution
            # Sleep for exactly 1 second (this creates our countdown interval)
            time.sleep(1)
            
            # PYTHON LEARNING: Double-check state after sleep
            # User might have paused timer while we were sleeping!
            if self.is_running:
                
                # Decrement remaining time by 1 second
                # PYTHON LEARNING: -= operator subtracts and assigns in one step
                self.time_left -= 1
                
                # PYTHON LEARNING: Thread-Safe GUI Updates
                # Schedule display update on main thread (safe from background)
                # root.after(0, function) means "run function immediately on main thread"
                self.root.after(0, self.update_display)
                
        # ═══════════════════════════════════════════════════════════════
        # HANDLE TIMER COMPLETION
        # ═══════════════════════════════════════════════════════════════
        
        # Check if timer completed naturally (time reached zero)
        # PYTHON LEARNING: Verify both conditions to be sure timer finished normally
        if self.time_left <= 0 and self.is_running:
            
            # Schedule completion handler on main thread
            # PYTHON LEARNING: Another thread-safe GUI operation
            self.root.after(0, self.timer_finished)
            
    def timer_finished(self):
        """
        🎉 PYTHON LEARNING: Complex Logic, State Transitions, and Automation
        ===================================================================
        
        This method handles what happens when a timer session completes. It shows:
        
        1. COMPLEX CONDITIONAL LOGIC: Different behavior based on session type
        2. MATHEMATICAL OPERATIONS: Using modulo (%) for cycling behavior
        3. AUTOMATED DECISION MAKING: Computer choosing next action
        4. USER INTERACTION: Optional automation vs manual confirmation
        5. METHOD COORDINATION: Calling multiple methods in sequence
        
        SESSION TRANSITION LOGIC:
        Work Session Complete → Short Break (usually)
        Work Session Complete → Long Break (every Nth session)
        Any Break Complete → Work Session (always)
        
        AUTOMATION OPTIONS:
        - Auto-start breaks: Immediately begin break without asking
        - Auto-start work: Immediately resume work after break
        - Manual mode: Show dialog and wait for user confirmation
        """
        
        # ═══════════════════════════════════════════════════════════════
        # STOP TIMER AND PLAY NOTIFICATION
        # ═══════════════════════════════════════════════════════════════
        
        # Immediately stop timer
        # PYTHON LEARNING: Always update state first
        self.is_running = False
        
        # Play sound notification if user has enabled it
        # PYTHON LEARNING: .get() method retrieves value from BooleanVar
        if self.sound_enabled.get():
            self.play_notification_sound()
            
        # ═══════════════════════════════════════════════════════════════
        # HANDLE WORK SESSION COMPLETION
        # ═══════════════════════════════════════════════════════════════
        
        if self.current_session == "Work":
            
            # Update counters for completed work
            # PYTHON LEARNING: += operator adds to existing value
            self.completed_pomodoros += 1    # Total pomodoros completed
            self.session_count += 1          # Work sessions for break timing
            
            # PYTHON LEARNING: Modulo Operator (%) for Cycling Logic
            # Determine if it's time for a long break
            # session_count % interval == 0 means evenly divisible
            # Example: if interval=4, long break after sessions 4, 8, 12, etc.
            if self.session_count % self.long_break_interval.get() == 0:
                self.current_session = "Long Break"
            else:
                self.current_session = "Short Break"
                
            # Handle automatic vs manual break starting
            # PYTHON LEARNING: Conditional automation
            if self.auto_start_breaks.get():
                # Automatically start break after 1 second delay
                # PYTHON LEARNING: root.after(delay, function) schedules future execution
                self.root.after(1000, self.start_timer)
            else:
                # Show dialog asking user to start break manually
                # PYTHON LEARNING: f-strings for dynamic text formatting
                messagebox.showinfo(
                    "Session Complete", 
                    f"Work session complete! Time for a {self.current_session.lower()}."
                )
                
        # ═══════════════════════════════════════════════════════════════
        # HANDLE BREAK SESSION COMPLETION
        # ═══════════════════════════════════════════════════════════════
        
        else:  # Any type of break session
            
            # All breaks return to work
            # PYTHON LEARNING: Simple state transition
            self.current_session = "Work"
            
            # Handle automatic vs manual work resumption
            if self.auto_start_work.get():
                # Automatically resume work after 1 second delay
                self.root.after(1000, self.start_timer)
            else:
                # Show dialog asking user to resume work manually
                messagebox.showinfo(
                    "Break Complete", 
                    "Break time is over! Ready for another work session?"
                )
        
        # ═══════════════════════════════════════════════════════════════
        # RESTORE BUTTON STATES AND PREPARE FOR NEXT SESSION
        # ═══════════════════════════════════════════════════════════════
        
        # Reset buttons to normal state for next session
        # PYTHON LEARNING: Always restore UI state after operations
        self.start_button.config(text="Start", state="normal")
        self.pause_button.config(state="normal")
        
        # Prepare display for next session
        # PYTHON LEARNING: Method calls to coordinate complex operations
        self.reset_for_new_session()
        
    def reset_for_new_session(self):
        """
        🔄 PYTHON LEARNING: State Preparation and Method Separation
        ==========================================================
        
        This method prepares the timer for the next session type. It shows:
        
        1. SEPARATION OF CONCERNS: One method, one responsibility
        2. LOOKUP LOGIC: Using current session to determine duration
        3. STATE COORDINATION: Setting multiple related variables
        4. METHOD DELEGATION: Calling other methods to complete the work
        
        WHY SEPARATE METHOD:
        - Keeps timer_finished() focused on transition logic
        - Reusable for other situations that need session preparation
        - Easier to test and debug individual pieces
        - Clean code organization
        """
        
        # ═══════════════════════════════════════════════════════════════
        # DETERMINE DURATION FOR NEXT SESSION
        # ═══════════════════════════════════════════════════════════════
        
        # PYTHON LEARNING: if/elif/else logic for lookup
        # Set appropriate duration based on what session type we're preparing for
        if self.current_session == "Work":
            # Get current work duration setting (user might have changed it!)
            self.time_left = self.work_duration.get() * 60
            
        elif self.current_session == "Short Break":
            self.time_left = self.short_break_duration.get() * 60
            
        else:  # Must be "Long Break"
            self.time_left = self.long_break_duration.get() * 60
            
        # ═══════════════════════════════════════════════════════════════
        # UPDATE RELATED STATE AND DISPLAY
        # ═══════════════════════════════════════════════════════════════
        
        # Store total time for progress calculation
        # PYTHON LEARNING: Keep reference to original value before countdown begins
        self.total_time = self.time_left
        
        # Update all display elements to show new session information
        # PYTHON LEARNING: Delegate display updates to specialized method
        self.update_display()
        
    def play_notification_sound(self):
        """
        🔊 PYTHON LEARNING: Audio Generation, Error Handling, and Mathematical Concepts
        =============================================================================
        
        This method creates and plays a notification sound using mathematical sound generation.
        It demonstrates several advanced Python concepts:
        
        1. TRY/EXCEPT ERROR HANDLING: Graceful handling of potential failures
        2. MATHEMATICAL SOUND GENERATION: Creating audio waves using math
        3. LIBRARY INTEGRATION: Using NumPy and pygame together
        4. FALLBACK STRATEGIES: What to do when things go wrong
        5. AUDIO PROGRAMMING: Understanding digital sound concepts
        
        SOUND GENERATION PROCESS:
        1. Define audio parameters (sample rate, duration, frequency)
        2. Calculate number of audio frames needed
        3. Generate sine wave using mathematical formula
        4. Convert floating-point values to integer audio format
        5. Create stereo sound and play through speakers
        
        WHY GENERATE SOUNDS INSTEAD OF USING FILES:
        - No external sound files needed (self-contained application)
        - Cross-platform compatibility (works on all operating systems)
        - Customizable tone and duration
        - Smaller application size
        """
        
        # ═══════════════════════════════════════════════════════════════
        # ERROR HANDLING - PROTECT AGAINST AUDIO FAILURES
        # ═══════════════════════════════════════════════════════════════
        
        # PYTHON LEARNING: try/except blocks handle potential errors gracefully
        # Audio systems can fail for many reasons (no speakers, permissions, etc.)
        try:
            
            # ═══════════════════════════════════════════════════════════
            # AUDIO PARAMETERS - DEFINING THE SOUND CHARACTERISTICS
            # ═══════════════════════════════════════════════════════════
            
            # PYTHON LEARNING: Audio Programming Concepts
            sample_rate = 22050     # Samples per second (22,050 Hz = CD quality)
            duration = 0.5          # Length of sound in seconds (half second)
            frequency = 800         # Pitch of tone in Hertz (800 Hz = pleasant beep)
            
            # Import numpy locally (only when needed)
            # PYTHON LEARNING: You can import libraries inside functions
            import numpy as np
            
            # ═══════════════════════════════════════════════════════════
            # CALCULATE AUDIO FRAMES
            # ═══════════════════════════════════════════════════════════
            
            # PYTHON LEARNING: Mathematical calculation
            # frames = duration × sample_rate
            # Example: 0.5 seconds × 22,050 samples/second = 11,025 frames
            frames = int(duration * sample_rate)
            
            # Create empty array to hold audio data
            # PYTHON LEARNING: np.zeros() creates array filled with zeros
            arr = np.zeros(frames)
            
            # ═══════════════════════════════════════════════════════════
            # GENERATE SINE WAVE - THE MATHEMATICAL MAGIC
            # ═══════════════════════════════════════════════════════════
            
            # PYTHON LEARNING: for loop with range() to process each audio frame
            for i in range(frames):
                
                # PYTHON LEARNING: Mathematical Formula for Sound Waves
                # arr[i] = sin(2π × frequency × time)
                # This creates a pure sine wave at the specified frequency
                arr[i] = np.sin(2 * np.pi * frequency * i / sample_rate)
                
                # MATH EXPLANATION:
                # - np.sin() = sine function (creates wave shape)
                # - 2 * np.pi = full circle in radians (360 degrees)
                # - frequency = how many cycles per second
                # - i / sample_rate = current time in seconds
                
            # ═══════════════════════════════════════════════════════════
            # CONVERT TO AUDIO FORMAT
            # ═══════════════════════════════════════════════════════════
            
            # PYTHON LEARNING: Data Type Conversion
            # Convert floating-point numbers (-1.0 to 1.0) to integers (-32767 to 32767)
            # This is the format that audio systems expect
            arr = (arr * 32767).astype(np.int16)
            
            # EXPLANATION:
            # - Multiply by 32767 to scale to full 16-bit range
            # - .astype(np.int16) converts to 16-bit signed integers
            
            # ═══════════════════════════════════════════════════════════
            # CREATE STEREO SOUND AND PLAY
            # ═══════════════════════════════════════════════════════════
            
            # PYTHON LEARNING: Array Manipulation
            # Create stereo sound by duplicating mono channel for left and right speakers
            # np.array([arr, arr]).T creates 2-channel audio array
            sound = pygame.sndarray.make_sound(np.array([arr, arr]).T)
            
            # PYTHON LEARNING: Non-blocking function call
            # .play() starts sound and immediately returns (doesn't wait for sound to finish)
            sound.play()
            
        # ═══════════════════════════════════════════════════════════════
        # ERROR HANDLING - FALLBACK TO SYSTEM BEEP
        # ═══════════════════════════════════════════════════════════════
        
        # PYTHON LEARNING: except clause catches ANY exception that occurs
        except:
            # If audio generation fails for any reason, use simple system beep
            # PYTHON LEARNING: print("\a") triggers system alert sound
            # \a is an "escape character" that means "alert/bell"
            print("\a")
            
    def update_display(self):
        """
        🖥️ PYTHON LEARNING: String Formatting, Dictionaries, and Mathematical Operations
        ================================================================================
        
        This method updates all visual elements to reflect the current timer state.
        It demonstrates several important Python concepts:
        
        1. MATHEMATICAL OPERATIONS: Converting seconds to minutes/seconds
        2. STRING FORMATTING: Creating formatted text displays
        3. DICTIONARY LOOKUPS: Using dictionaries for data mapping
        4. CONDITIONAL CALCULATIONS: Preventing division by zero errors
        5. WIDGET CONFIGURATION: Updating GUI elements dynamically
        
        DISPLAY ELEMENTS UPDATED:
        - Timer display (MM:SS format)
        - Session label text and color
        - Progress bar percentage
        
        CALLED FROM MULTIPLE PLACES:
        - Every second during countdown (from background thread)
        - When user resets timer
        - When sessions change
        - During initialization
        """
        
        # ═══════════════════════════════════════════════════════════════
        # TIME FORMATTING - CONVERT SECONDS TO MINUTES:SECONDS
        # ═══════════════════════════════════════════════════════════════
        
        # PYTHON LEARNING: Integer Division (//) and Modulo (%) operators
        # Example: 150 seconds = 2 minutes and 30 seconds
        # 150 // 60 = 2 (minutes)
        # 150 % 60 = 30 (remaining seconds)
        minutes = self.time_left // 60    # How many full minutes
        seconds = self.time_left % 60     # Remaining seconds after removing full minutes
        
        # PYTHON LEARNING: f-string formatting with zero-padding
        # f"{minutes:02d}" means format as integer with at least 2 digits, pad with zeros
        # Example: 5 becomes "05", 25 stays "25"
        time_text = f"{minutes:02d}:{seconds:02d}"
        
        # Update the timer display label
        # PYTHON LEARNING: .config() method changes widget properties after creation
        self.time_label.config(text=time_text)
        
        # ═══════════════════════════════════════════════════════════════
        # SESSION LABEL COLOR CODING
        # ═══════════════════════════════════════════════════════════════
        
        # PYTHON LEARNING: Dictionary for mapping values
        # Dictionaries store key-value pairs for quick lookups
        session_colors = {
            "Work": "#e74c3c",           # Red for work sessions (focus/concentration)
            "Short Break": "#f39c12",    # Orange for short breaks (brief rest)
            "Long Break": "#9b59b6"      # Purple for long breaks (extended restoration)
        }
        
        # Update session label with current session name and appropriate color
        self.session_label.config(
            text=f"{self.current_session}",                                    # Session name
            fg=session_colors.get(self.current_session, "#ecf0f1")           # Color lookup with default
        )
        
        # PYTHON LEARNING: .get() method with default value
        # dict.get(key, default) returns the value for key, or default if key not found
        # This prevents KeyError if somehow an unexpected session type exists
        
        # ═══════════════════════════════════════════════════════════════
        # PROGRESS BAR UPDATE
        # ═══════════════════════════════════════════════════════════════
        
        # PYTHON LEARNING: Conditional calculation to prevent division by zero
        # Always check denominator before dividing!
        if self.total_time > 0:
            
            # PYTHON LEARNING: Percentage calculation
            # progress = (completed_time / total_time) × 100
            # completed_time = total_time - time_left
            progress = ((self.total_time - self.time_left) / self.total_time) * 100
            
            # Update progress bar value
            # PYTHON LEARNING: Dictionary-style access to widget properties
            # Some tkinter widgets use ['property'] instead of .config()
            self.progress['value'] = progress
            
    def calculate_responsive_values(self):
        """
        📐 PYTHON LEARNING: Mathematical Scaling, Constraints, and Responsive Design
        ===========================================================================
        
        This method calculates font sizes and spacing that adapt to window size changes.
        It demonstrates several important programming concepts:
        
        1. MATHEMATICAL SCALING: Proportional calculations based on ratios
        2. CONSTRAINT FUNCTIONS: Using max() and min() to limit values
        3. RESPONSIVE DESIGN: Adapting interface to different screen sizes
        4. REFERENCE VALUES: Using base measurements for calculations
        5. INSTANCE VARIABLE ASSIGNMENT: Storing calculated values for later use
        
        RESPONSIVE DESIGN PRINCIPLES:
        - Fonts scale with window width (bigger window = bigger fonts)
        - Spacing scales with window height (taller window = more spacing)
        - Minimum and maximum limits prevent unusable sizes
        - Timer font stays fixed for optimal readability
        
        MATHEMATICAL APPROACH:
        - Calculate scale factors by comparing current size to base size
        - Apply scale factors to base font sizes and spacing values
        - Use constraints to keep values within usable ranges
        """
        
        # ═══════════════════════════════════════════════════════════════
        # GET CURRENT WINDOW DIMENSIONS
        # ═══════════════════════════════════════════════════════════════
        
        # PYTHON LEARNING: Widget information methods
        # These methods return the current actual size of the window
        current_width = self.root.winfo_width()      # Current width in pixels
        current_height = self.root.winfo_height()    # Current height in pixels
        
        # ═══════════════════════════════════════════════════════════════
        # CALCULATE SCALING FACTORS
        # ═══════════════════════════════════════════════════════════════
        
        # PYTHON LEARNING: Ratio calculations for proportional scaling
        # scale_factor = current_size / reference_size
        # Example: 600px / 500px = 1.2 (20% larger than reference)
        width_scale = current_width / self.base_width
        height_scale = current_height / self.base_height
        
        # PYTHON LEARNING: Constraint functions - limiting values to safe ranges
        # max(0.8, min(1.5, value)) keeps value between 0.8 and 1.5
        # This prevents fonts from becoming too small (unreadable) or too large (overwhelming)
        width_scale = max(0.8, min(1.5, width_scale))
        height_scale = max(0.8, min(1.5, height_scale))
        
        # ═══════════════════════════════════════════════════════════════
        # CALCULATE RESPONSIVE FONT SIZES
        # ═══════════════════════════════════════════════════════════════
        
        # PYTHON LEARNING: Mathematical scaling with minimum constraints
        # Formula: scaled_size = base_size × scale_factor
        # max(minimum, scaled_size) ensures fonts never get too small
        
        # Title font scales with window width
        self.title_font_size = max(16, int(24 * width_scale))
        
        # Session label font scales with width
        self.session_font_size = max(12, int(16 * width_scale))
        
        # PYTHON LEARNING: Fixed vs. Responsive values
        # Timer font stays at 48 for optimal readability - never changes!
        self.timer_font_size = 48  # Always fixed for optimal readability
        
        # Button font scales with width
        self.button_font_size = max(10, int(12 * width_scale))
        
        # ═══════════════════════════════════════════════════════════════
        # CALCULATE RESPONSIVE SPACING VALUES
        # ═══════════════════════════════════════════════════════════════
        
        # PYTHON LEARNING: Spacing scales with HEIGHT to maintain proportions
        # Vertical spacing should grow when window gets taller
        
        self.title_pady = max(10, int(15 * height_scale))        # Title spacing
        self.session_pady = max(5, int(8 * height_scale))        # Session label spacing
        self.timer_pady = max(15, int(20 * height_scale))        # Timer spacing
        self.progress_pady = max(8, int(10 * height_scale))      # Progress bar spacing
        self.controls_pady = max(15, int(18 * height_scale))     # Button spacing
        self.settings_pady = max(8, int(10 * height_scale))      # Settings spacing
        
        # ═══════════════════════════════════════════════════════════════
        # CALCULATE PROGRESS BAR LENGTH
        # ═══════════════════════════════════════════════════════════════
        
        # PYTHON LEARNING: Horizontal elements scale with WIDTH
        # Progress bar should get longer when window gets wider
        self.progress_length = max(250, int(300 * width_scale))
        
    def on_window_resize(self, event):
        """
        🪟 PYTHON LEARNING: Event Handling and Callback Functions
        ========================================================
        
        This method is called automatically whenever the window is resized.
        It demonstrates important event-driven programming concepts:
        
        1. EVENT CALLBACKS: Functions that respond to user actions
        2. EVENT FILTERING: Only responding to specific events
        3. METHOD COORDINATION: Calling other methods in response to events
        4. RESPONSIVE UPDATES: Keeping interface updated during changes
        
        EVENT-DRIVEN PROGRAMMING:
        - User resizes window → System generates '<Configure>' event
        - tkinter calls this method automatically → We check if it's the main window
        - If yes → We recalculate sizes and update the interface
        
        WHY CHECK event.widget:
        - Many widgets can generate '<Configure>' events
        - We only care about main window resize events
        - Child widgets resizing shouldn't trigger our calculations
        """
        
        # ═══════════════════════════════════════════════════════════════
        # EVENT FILTERING - ONLY RESPOND TO MAIN WINDOW RESIZE
        # ═══════════════════════════════════════════════════════════════
        
        # PYTHON LEARNING: Event object properties
        # event.widget tells us which widget generated the event
        # We only want to respond when the main window (self.root) is resized
        if event.widget == self.root:
            
            # ═══════════════════════════════════════════════════════════
            # RESPONSIVE DESIGN UPDATE SEQUENCE
            # ═══════════════════════════════════════════════════════════
            
            # PYTHON LEARNING: Method coordination
            # Call methods in the right order to update interface
            
            # 1. Recalculate all responsive values based on new window size
            self.calculate_responsive_values()
            
            # 2. Apply new values to existing widgets
            self.update_widget_styling()
            
    def update_widget_styling(self):
        """
        🎨 PYTHON LEARNING: Error Handling and Widget Management
        =======================================================
        
        This method applies calculated responsive values to existing widgets.
        It demonstrates important GUI programming concepts:
        
        1. ERROR HANDLING: Gracefully handling widget access errors
        2. WIDGET CONFIGURATION: Updating multiple widget properties
        3. EXCEPTION TYPES: Understanding AttributeError specifically
        4. INITIALIZATION TIMING: Handling cases where widgets don't exist yet
        
        WHY ERROR HANDLING IS NEEDED:
        - This method might be called before widgets are created
        - During initialization, calculate_responsive_values() might run
        - Before create_widgets() has finished creating all the widgets
        - AttributeError occurs when trying to access non-existent widgets
        
        FONT UPDATE STRATEGY:
        - Update all text widgets with new calculated font sizes
        - Maintain font families and weights (Arial, bold)
        - Keep timer font fixed at 48pt for readability
        - Update progress bar length for responsive width
        """
        
        # ═══════════════════════════════════════════════════════════════
        # ERROR HANDLING FOR WIDGET ACCESS
        # ═══════════════════════════════════════════════════════════════
        
        # PYTHON LEARNING: try/except for specific error types
        # AttributeError occurs when trying to access attributes that don't exist
        try:
            
            # ═══════════════════════════════════════════════════════════
            # UPDATE TEXT WIDGET FONTS
            # ═══════════════════════════════════════════════════════════
            
            # PYTHON LEARNING: Widget configuration with calculated values
            # Each widget gets updated with its appropriate responsive font size
            
            # Update title with new responsive font size
            self.title_label.config(font=("Arial", self.title_font_size, "bold"))
            
            # Update session label with new responsive font size  
            self.session_label.config(font=("Arial", self.session_font_size))
            
            # PYTHON LEARNING: Fixed vs responsive values
            # Timer font stays at 48pt - notice we use self.timer_font_size which is always 48
            self.time_label.config(font=("Arial", self.timer_font_size, "bold"))
            
            # Update all button fonts with new responsive size
            self.start_button.config(font=("Arial", self.button_font_size, "bold"))
            self.pause_button.config(font=("Arial", self.button_font_size, "bold"))
            self.reset_button.config(font=("Arial", self.button_font_size, "bold"))
            
            # Update settings button (no bold weight for this one)
            self.settings_button.config(font=("Arial", self.button_font_size))
            
            # ═══════════════════════════════════════════════════════════
            # UPDATE PROGRESS BAR LENGTH
            # ═══════════════════════════════════════════════════════════
            
            # PYTHON LEARNING: Different widget configuration styles
            # Some widgets use .config(), others use dictionary-style access
            self.progress.config(length=self.progress_length)
            
        # ═══════════════════════════════════════════════════════════════
        # HANDLE INITIALIZATION TIMING ISSUES
        # ═══════════════════════════════════════════════════════════════
        
        # PYTHON LEARNING: Specific exception handling
        # AttributeError means we tried to access an attribute that doesn't exist
        except AttributeError:
            # This happens when widgets haven't been created yet
            # During initialization, this method might run before create_widgets()
            # PYTHON LEARNING: pass statement does nothing - silently ignore the error
            pass

def main():
    """
    Application Entry Point and Main Loop Initialization
    
    Purpose: Creates the main application window and starts the tkinter
    event loop.
    """
    root = tk.Tk()
    app = PomodoroTimer(root)
    root.mainloop()

if __name__ == "__main__":
    main()