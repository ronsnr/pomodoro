"""
POMODORO TIMER GUI APPLICATION

This application implements the Pomodoro Technique - a time management method that uses 
a timer to break down work into intervals (traditionally 25 minutes) separated by short breaks.

Key Features:
- Customizable work and break durations
- Visual progress tracking with progress bar
- Audio notifications when sessions complete
- Automatic session progression (work → break → work)
- Statistics tracking for completed pomodoros
- Multiple timer modes (Classic 25/5/15, Focus 45/10/30)
- Pause/resume functionality
- Auto-start options for breaks and work sessions

Dependencies:
- tkinter: GUI framework (built into Python)
- pygame: Audio notification system
- numpy: Sound wave generation
- threading: Non-blocking timer execution
- time: Timer countdown functionality

Author: GitHub Copilot
Date: October 2025
"""

import tkinter as tk
from tkinter import ttk, messagebox
import time
import threading
import pygame
import os
from datetime import datetime, timedelta

class PomodoroTimer:
    """
    Main Pomodoro Timer Application Class
    
    This class handles the complete Pomodoro timer functionality including:
    - GUI creation and management
    - Timer logic and state management
    - User settings and preferences
    - Audio notifications
    - Session tracking and statistics
    
    The class follows the Model-View-Controller pattern where:
    - Model: Timer state variables and settings
    - View: GUI widgets and display elements
    - Controller: Event handlers and timer logic
    """
    
    def __init__(self, root):
        """
        Initialize the Pomodoro Timer Application
        
        Purpose: Sets up the main application window, initializes all state variables,
        configures audio system, and creates the user interface.
        
        Args:
            root (tk.Tk): The main tkinter window object
            
        State Variables Initialized:
        - Timer control: is_running, is_paused
        - Session tracking: current_session, session_count, completed_pomodoros
        - Time management: time_left, total_time
        - User preferences: work_duration, break_durations, sound settings
        """
        self.root = root
        self.root.title("🍅 Pomodoro Timer")
        
        # Set responsive window sizing with minimum constraints
        self.root.geometry("500x480")
        self.root.minsize(400, 400)
        self.root.configure(bg="#2c3e50")
        
        # Keep window always on top of other applications
        # This ensures the timer remains visible for continuous productivity monitoring
        self.root.attributes('-topmost', True)
        
        # Dynamic spacing and font calculations
        self.base_width = 500
        self.base_height = 480
        
        # Initialize pygame for sound
        pygame.mixer.init()
        
        # Timer state variables
        self.is_running = False
        self.is_paused = False
        self.current_session = "Work"
        self.time_left = 0
        self.total_time = 0
        self.session_count = 0
        self.completed_pomodoros = 0
        
        # Timer settings (in minutes)
        self.work_duration = tk.IntVar(value=25)
        self.short_break_duration = tk.IntVar(value=5)
        self.long_break_duration = tk.IntVar(value=15)
        self.long_break_interval = tk.IntVar(value=4)
        
        # Sound settings
        self.sound_enabled = tk.BooleanVar(value=True)
        self.auto_start_breaks = tk.BooleanVar(value=False)
        self.auto_start_work = tk.BooleanVar(value=False)
        
        # Bind window resize event for responsive design
        self.root.bind('<Configure>', self.on_window_resize)
        
        # Create GUI elements
        self.create_widgets()
        self.update_display()
        
    def create_widgets(self):
        """
        Create and Configure All GUI Elements
        
        Purpose: Builds the complete user interface with proper layout, styling, and event bindings.
        This method creates a professional-looking timer interface with all necessary controls.
        
        GUI Components Created:
        - Title label
        - Session type indicator
        - Countdown display
        - Progress bar
        - Control buttons (Start/Pause/Reset)
        - Settings button
        """
        # Calculate initial responsive values
        self.calculate_responsive_values()
        
        # Create main container frame for better spacing control
        main_container = tk.Frame(self.root, bg="#2c3e50")
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Main title
        self.title_label = tk.Label(
            main_container, 
            text="🍅 Pomodoro Timer", 
            font=("Arial", self.title_font_size, "bold"),
            bg="#2c3e50", 
            fg="#ecf0f1"
        )
        self.title_label.pack(pady=self.title_pady)
        
        # Current session label
        self.session_label = tk.Label(
            main_container,
            text="Work Session",
            font=("Arial", self.session_font_size),
            bg="#2c3e50",
            fg="#e74c3c"
        )
        self.session_label.pack(pady=self.session_pady)
        
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
        
        # Progress bar container for centered positioning
        progress_container = tk.Frame(main_container, bg="#2c3e50")
        progress_container.pack(pady=self.progress_pady, fill=tk.X)
        
        self.progress = ttk.Progressbar(
            progress_container,
            length=self.progress_length,
            mode='determinate'
        )
        self.progress.pack()
        
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
        
        self.pause_button = tk.Button(
            control_frame,
            text="Pause",
            font=("Arial", self.button_font_size, "bold"),
            bg="#f39c12",
            fg="white",
            width=button_width,
            command=self.pause_timer
        )
        self.pause_button.pack(side=tk.LEFT, padx=8)
        
        self.reset_button = tk.Button(
            control_frame,
            text="Reset",
            font=("Arial", self.button_font_size, "bold"),
            bg="#e74c3c",
            fg="white",
            width=button_width,
            command=self.reset_timer
        )
        self.reset_button.pack(side=tk.LEFT, padx=8)
        
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
        Initialize and Begin Timer Countdown
        
        Purpose: Starts a new timer session or resumes a paused session.
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
        
    def pause_timer(self):
        """
        Temporarily Suspend Timer Countdown
        
        Purpose: Pauses the active timer without losing progress.
        """
        if self.is_running:
            self.is_paused = True
            self.is_running = False
            self.start_button.config(text="Resume", state="normal")
            self.pause_button.config(state="disabled")
        
    def reset_timer(self):
        """
        Reset Timer to Initial State
        
        Purpose: Completely resets the timer to beginning state.
        """
        self.is_running = False
        self.is_paused = False
        self.current_session = "Work"
        self.time_left = self.work_duration.get() * 60
        self.total_time = self.time_left
        self.start_button.config(text="Start", state="normal")
        self.pause_button.config(state="normal")
        self.update_display()
        
    def run_timer(self):
        """
        Execute Timer Countdown Loop
        
        Purpose: This is the core timer engine that runs in a separate thread.
        """
        while self.time_left > 0 and self.is_running:
            time.sleep(1)
            if self.is_running:
                self.time_left -= 1
                self.root.after(0, self.update_display)
                
        if self.time_left <= 0 and self.is_running:
            self.root.after(0, self.timer_finished)
            
    def timer_finished(self):
        """
        Handle Session Completion and Transition Logic
        
        Purpose: Orchestrates the complete session completion process.
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
        
    def reset_for_new_session(self):
        """
        Configure Timer for Next Session Type
        
        Purpose: Prepares the timer display and internal state for the next session.
        """
        if self.current_session == "Work":
            self.time_left = self.work_duration.get() * 60
        elif self.current_session == "Short Break":
            self.time_left = self.short_break_duration.get() * 60
        else:  # Long Break
            self.time_left = self.long_break_duration.get() * 60
            
        self.total_time = self.time_left
        self.update_display()
        
    def play_notification_sound(self):
        """
        Generate and Play Audio Notification
        
        Purpose: Creates a pleasant audio alert when sessions complete.
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
            
    def update_display(self):
        """
        Refresh All GUI Elements with Current State
        
        Purpose: Synchronizes all visual elements with the current timer state.
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
            
    def calculate_responsive_values(self):
        """
        Calculate responsive font sizes and spacing based on current window size
        
        Purpose: Dynamically adjusts UI elements based on window dimensions
        while keeping the timer font at a fixed readable size.
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
        
    def on_window_resize(self, event):
        """
        Handle window resize events for responsive design
        
        Purpose: Updates font sizes and spacing when window is resized
        """
        if event.widget == self.root:
            self.calculate_responsive_values()
            self.update_widget_styling()
            
    def update_widget_styling(self):
        """
        Update widget fonts and spacing based on current responsive values
        
        Purpose: Applies calculated responsive values to existing widgets
        """
        try:
            # Update fonts
            self.title_label.config(font=("Arial", self.title_font_size, "bold"))
            self.session_label.config(font=("Arial", self.session_font_size))
            self.time_label.config(font=("Arial", self.timer_font_size, "bold"))  # Timer font stays fixed
            
            self.start_button.config(font=("Arial", self.button_font_size, "bold"))
            self.pause_button.config(font=("Arial", self.button_font_size, "bold"))
            self.reset_button.config(font=("Arial", self.button_font_size, "bold"))
            
            self.settings_button.config(font=("Arial", self.button_font_size))
            
            # Update progress bar length
            self.progress.config(length=self.progress_length)
        except AttributeError:
            # Widgets not created yet
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