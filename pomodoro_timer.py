import tkinter as tk
from tkinter import ttk, messagebox
import time
import threading
import pygame
import os
from datetime import datetime, timedelta

class PomodoroTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("Pomodoro Timer")
        self.root.geometry("500x600")
        self.root.configure(bg="#2c3e50")
        
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
        
        # Create GUI elements
        self.create_widgets()
        self.update_display()
        
    def create_widgets(self):
        # Main title
        title_label = tk.Label(
            self.root, 
            text="🍅 Pomodoro Timer", 
            font=("Arial", 24, "bold"),
            bg="#2c3e50", 
            fg="#ecf0f1"
        )
        title_label.pack(pady=20)
        
        # Current session label
        self.session_label = tk.Label(
            self.root,
            text="Work Session",
            font=("Arial", 16),
            bg="#2c3e50",
            fg="#e74c3c"
        )
        self.session_label.pack(pady=10)
        
        # Time display
        self.time_label = tk.Label(
            self.root,
            text="25:00",
            font=("Arial", 48, "bold"),
            bg="#2c3e50",
            fg="#ecf0f1"
        )
        self.time_label.pack(pady=20)
        
        # Progress bar
        self.progress = ttk.Progressbar(
            self.root,
            length=300,
            mode='determinate'
        )
        self.progress.pack(pady=10)
        
        # Control buttons frame
        control_frame = tk.Frame(self.root, bg="#2c3e50")
        control_frame.pack(pady=20)
        
        self.start_button = tk.Button(
            control_frame,
            text="Start",
            font=("Arial", 12, "bold"),
            bg="#27ae60",
            fg="white",
            width=8,
            command=self.start_timer
        )
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.pause_button = tk.Button(
            control_frame,
            text="Pause",
            font=("Arial", 12, "bold"),
            bg="#f39c12",
            fg="white",
            width=8,
            command=self.pause_timer
        )
        self.pause_button.pack(side=tk.LEFT, padx=5)
        
        self.reset_button = tk.Button(
            control_frame,
            text="Reset",
            font=("Arial", 12, "bold"),
            bg="#e74c3c",
            fg="white",
            width=8,
            command=self.reset_timer
        )
        self.reset_button.pack(side=tk.LEFT, padx=5)
        
        # Statistics frame
        stats_frame = tk.Frame(self.root, bg="#34495e", relief=tk.RAISED, bd=2)
        stats_frame.pack(pady=20, padx=20, fill=tk.X)
        
        stats_title = tk.Label(
            stats_frame,
            text="Session Statistics",
            font=("Arial", 14, "bold"),
            bg="#34495e",
            fg="#ecf0f1"
        )
        stats_title.pack(pady=5)
        
        self.stats_label = tk.Label(
            stats_frame,
            text="Completed Pomodoros: 0\nCurrent Session: 1",
            font=("Arial", 12),
            bg="#34495e",
            fg="#ecf0f1"
        )
        self.stats_label.pack(pady=5)
        
        # Settings button
        settings_button = tk.Button(
            self.root,
            text="⚙️ Settings",
            font=("Arial", 12),
            bg="#9b59b6",
            fg="white",
            command=self.open_settings
        )
        settings_button.pack(pady=10)
        
    def create_settings_window(self):
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
        """Classic Pomodoro: 25min work, 5min short break, 15min long break"""
        self.work_duration.set(25)
        self.short_break_duration.set(5)
        self.long_break_duration.set(15)
        self.long_break_interval.set(4)
        
    def set_focus_mode(self):
        """Extended focus: 45min work, 10min short break, 30min long break"""
        self.work_duration.set(45)
        self.short_break_duration.set(10)
        self.long_break_duration.set(30)
        self.long_break_interval.set(3)
        
    def open_settings(self):
        self.create_settings_window()
        
    def save_settings(self):
        if not self.is_running:
            self.reset_timer()
        messagebox.showinfo("Settings", "Settings saved successfully!")
        
    def start_timer(self):
        if not self.is_running and not self.is_paused:
            # Starting a new session
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
        if self.is_running:
            self.is_paused = True
            self.is_running = False
            self.start_button.config(text="Resume", state="normal")
            self.pause_button.config(state="disabled")
        
    def reset_timer(self):
        self.is_running = False
        self.is_paused = False
        self.current_session = "Work"
        self.time_left = self.work_duration.get() * 60
        self.total_time = self.time_left
        self.start_button.config(text="Start", state="normal")
        self.pause_button.config(state="normal")
        self.update_display()
        
    def run_timer(self):
        while self.time_left > 0 and self.is_running:
            time.sleep(1)
            if self.is_running:  # Check again in case it was paused during sleep
                self.time_left -= 1
                self.root.after(0, self.update_display)
                
        if self.time_left <= 0 and self.is_running:
            self.root.after(0, self.timer_finished)
            
    def timer_finished(self):
        self.is_running = False
        
        # Play notification sound
        if self.sound_enabled.get():
            self.play_notification_sound()
            
        # Update session count and switch session type
        if self.current_session == "Work":
            self.completed_pomodoros += 1
            self.session_count += 1
            
            # Determine next session type
            if self.session_count % self.long_break_interval.get() == 0:
                self.current_session = "Long Break"
            else:
                self.current_session = "Short Break"
                
            # Auto-start break if enabled
            if self.auto_start_breaks.get():
                self.root.after(1000, self.start_timer)
            else:
                messagebox.showinfo("Session Complete", f"Work session complete! Time for a {self.current_session.lower()}.")
                
        else:  # Break finished
            self.current_session = "Work"
            
            # Auto-start work if enabled
            if self.auto_start_work.get():
                self.root.after(1000, self.start_timer)
            else:
                messagebox.showinfo("Break Complete", "Break time is over! Ready for another work session?")
        
        # Reset button state
        self.start_button.config(text="Start", state="normal")
        self.pause_button.config(state="normal")
        
        # Update display for new session
        self.reset_for_new_session()
        
    def reset_for_new_session(self):
        if self.current_session == "Work":
            self.time_left = self.work_duration.get() * 60
        elif self.current_session == "Short Break":
            self.time_left = self.short_break_duration.get() * 60
        else:  # Long Break
            self.time_left = self.long_break_duration.get() * 60
            
        self.total_time = self.time_left
        self.update_display()
        
    def play_notification_sound(self):
        try:
            # Create a simple beep sound using pygame
            sample_rate = 22050
            duration = 0.5
            frequency = 800
            
            # Generate a simple sine wave
            import numpy as np
            frames = int(duration * sample_rate)
            arr = np.zeros(frames)
            for i in range(frames):
                arr[i] = np.sin(2 * np.pi * frequency * i / sample_rate)
            
            # Convert to pygame sound
            arr = (arr * 32767).astype(np.int16)
            sound = pygame.sndarray.make_sound(np.array([arr, arr]).T)
            sound.play()
        except:
            # Fallback: system beep
            print("\a")  # ASCII bell character
            
    def update_display(self):
        # Update time display
        minutes = self.time_left // 60
        seconds = self.time_left % 60
        time_text = f"{minutes:02d}:{seconds:02d}"
        self.time_label.config(text=time_text)
        
        # Update session label and color
        session_colors = {
            "Work": "#e74c3c",
            "Short Break": "#f39c12",
            "Long Break": "#9b59b6"
        }
        
        self.session_label.config(
            text=f"{self.current_session}",
            fg=session_colors.get(self.current_session, "#ecf0f1")
        )
        
        # Update progress bar
        if self.total_time > 0:
            progress = ((self.total_time - self.time_left) / self.total_time) * 100
            self.progress['value'] = progress
            
        # Update statistics
        self.stats_label.config(
            text=f"Completed Pomodoros: {self.completed_pomodoros}\nCurrent Session: {self.session_count + 1}"
        )

def main():
    root = tk.Tk()
    app = PomodoroTimer(root)
    root.mainloop()

if __name__ == "__main__":
    main()