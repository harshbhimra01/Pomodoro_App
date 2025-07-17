import tkinter as tk
import time
from threading import Thread
import sys
import threading
from PIL import Image, ImageTk, ImageSequence
import pystray
from pystray import MenuItem as item
import os

# Try to import platform-specific modules
try:
    import winsound
    HAS_WINSOUND = True
except ImportError:
    HAS_WINSOUND = False

try:
    from plyer import notification
    HAS_PLYER = True
except ImportError:
    HAS_PLYER = False

# ---------- Global Flags ----------
is_running = False
stop_flag = False
session_count = 0
pulse_state = True
current_theme = "dark"

# ---------- Theme Dictionary ----------
themes = {
    "dark": {
        "bg": "#2e2e2e",
        "fg": "white",
        "entry_bg": "#444444",
        "entry_fg": "white"
    },
    "light": {
        "bg": "#ffffff",
        "fg": "#000000",
        "entry_bg": "#dddddd",
        "entry_fg": "black"
    }
}

# ---------- Resource Path Function ----------
def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# ---------- Functions ----------
def update_timer_label(text):
    if 'timer_label' in globals():
        timer_label.config(text=text)
        timer_label.update_idletasks()

def play_sound():
    if HAS_WINSOUND:
        try:
            duration = 500
            freq = 1000
            winsound.Beep(freq, duration)
        except:
            # Fallback to system bell if winsound fails
            print('\a')  # System bell
    else:
        print('\a')  # System bell fallback

def show_notification(title, message):
    if HAS_PLYER:
        try:
            notification.notify(title=title, message=message, timeout=5)
        except:
            print(f"Notification: {title} - {message}")
    else:
        print(f"Notification: {title} - {message}")

def pulse_color(label_type):
    global pulse_state
    if not is_running or stop_flag:
        if 'timer_label' in globals():
            timer_label.config(fg=themes[current_theme]["fg"])
        return
    
    color1 = "#90ee90" if label_type == "work" else "#add8e6"
    color2 = themes[current_theme]["fg"]
    
    if 'timer_label' in globals():
        timer_label.config(fg=color1 if pulse_state else color2)
        pulse_state = not pulse_state
        window.after(500, lambda: pulse_color(label_type))

def countdown(minutes, label):
    global stop_flag
    pulse_color("work" if label == "🧠 Focus" else "break")
    total_seconds = int(minutes * 60)
    while total_seconds > 0:
        if stop_flag:
            update_timer_label("⏹️ Stopped early")
            break
        mins, secs = divmod(total_seconds, 60)
        time_str = f"{label} - {int(mins):02d}:{int(secs):02d}"
        update_timer_label(time_str)
        time.sleep(1)
        total_seconds -= 1
    else:
        if not stop_flag:
            update_timer_label(f"{label} - Time's up!")
            play_sound()
            show_notification("⏰ Pomodoro Finished", f"{label} session complete. Time for the next step!")

def pomodoro_loop():
    global is_running, stop_flag, session_count
    session_count = 0
    try:
        work_minutes = float(work_input.get())
        short_break = float(short_input.get())
        long_break = float(long_input.get())
    except ValueError:
        update_timer_label("❌ Invalid input")
        is_running = False
        return
    try:
        while not stop_flag:
            session_count += 1
            if 'session_label' in globals():
                session_label.config(text=f"Completed: {session_count}")
            update_timer_label(f"🔔 Session {session_count} - Work")
            countdown(work_minutes, "🧠 Focus")
            if stop_flag: break
            if session_count % 4 == 0:
                update_timer_label("🎉 Long Break Time")
                countdown(long_break, "😴 Chill")
            else:
                update_timer_label("☕ Short Break Time")
                countdown(short_break, "🛋️ Relax")
    finally:
        is_running = False

def start_pomodoro():
    global is_running, stop_flag
    if not is_running:
        is_running = True
        stop_flag = False
        Thread(target=pomodoro_loop, daemon=True).start()

def stop_pomodoro():
    global stop_flag, is_running
    stop_flag = True
    is_running = False
    update_timer_label("🛑 Stopped")

def reset_pomodoro():
    global stop_flag, is_running, session_count
    stop_flag = True
    is_running = False
    session_count = 0
    update_timer_label("🍅 50:00 Ready")
    if 'session_label' in globals():
        session_label.config(text="Completed: 0")

def toggle_theme():
    global current_theme
    current_theme = "light" if current_theme == "dark" else "dark"
    apply_theme(current_theme)

def apply_theme(theme):
    config = themes[theme]
    window.config(bg=config["bg"])
    title_label.config(bg=config["bg"], fg="#f76c6c")
    timer_label.config(bg=config["bg"], fg=config["fg"])
    session_label.config(bg=config["bg"], fg=config["fg"])
    input_frame.config(bg=config["bg"])
    button_frame.config(bg=config["bg"])
    
    # Only update if logo_label exists
    if 'logo_label' in globals():
        logo_label.config(bg=config["bg"])
    
    # Only update if cat_label exists
    if 'cat_label' in globals():
        cat_label.config(bg=config["bg"])
    
    for widget in input_frame.winfo_children():
        if isinstance(widget, tk.Entry):
            widget.config(bg=config["entry_bg"], fg=config["entry_fg"])
        elif isinstance(widget, tk.Label):
            widget.config(bg=config["bg"], fg=config["fg"])

def quit_app():
    if 'icon' in globals():
        icon.stop()
    window.destroy()
    sys.exit()

def create_tray_icon():
    global icon
    # Create a simple colored image for the tray icon
    image = Image.new('RGB', (64, 64), color='red')
    icon = pystray.Icon("Pomodoro", image, "Pomodoro Pro", menu=pystray.Menu(
        item('Start', lambda: start_pomodoro()),
        item('Stop', lambda: stop_pomodoro()),
        item('Reset', lambda: reset_pomodoro()),
        item('Quit', lambda: quit_app())
    ))
    threading.Thread(target=icon.run, daemon=True).start()

def load_image_safely(filename, size=None, default_color='red'):
    """Safely load an image file with fallback to colored rectangle"""
    try:
        img_path = resource_path(filename)
        if os.path.exists(img_path):
            img = Image.open(img_path)
            if size:
                img = img.resize(size)
            return ImageTk.PhotoImage(img)
        else:
            # Create a colored rectangle as fallback
            img = Image.new('RGB', size or (100, 100), color=default_color)
            return ImageTk.PhotoImage(img)
    except Exception as e:
        print(f"Error loading image {filename}: {e}")
        # Create a colored rectangle as fallback
        img = Image.new('RGB', size or (100, 100), color=default_color)
        return ImageTk.PhotoImage(img)

def setup_animated_gif():
    """Setup animated GIF with fallback"""
    global frames, frame_index, cat_label
    
    try:
        gif_path = resource_path(r"C:\Users\bhimr\Documents\Visual Studio 2022 Preview\Pomodoro_App\cat-cat-snore.gif")
        if os.path.exists(gif_path):
            cat_gif = Image.open(gif_path)
            frames = []
            for frame in ImageSequence.Iterator(cat_gif):
                resized = frame.resize((200, 200))
                tk_image = ImageTk.PhotoImage(resized)
                frames.append(tk_image)
        else:
            # Create a simple animated fallback
            frames = []
            colors = ['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4', '#ffeaa7']
            for color in colors:
                img = Image.new('RGB', (200, 200), color=color)
                tk_image = ImageTk.PhotoImage(img)
                frames.append(tk_image)
    except Exception as e:
        print(f"Error loading animated GIF: {e}")
        # Create a simple animated fallback
        frames = []
        colors = ['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4', '#ffeaa7']
        for color in colors:
            img = Image.new('RGB', (200, 200), color=color)
            tk_image = ImageTk.PhotoImage(img)
            frames.append(tk_image)
    
    frame_index = 0
    cat_label = tk.Label(window, bg=themes[current_theme]["bg"])
    cat_label.pack(pady=10)

def animate_gif():
    global frame_index
    if 'cat_label' in globals() and frames:
        cat_label.config(image=frames[frame_index])
        frame_index = (frame_index + 1) % len(frames)
        window.after(100, animate_gif)

# ---------- GUI Setup ----------
window = tk.Tk()
window.title("🍅 Pomodoro Pro")
window.geometry("660x700")

# Load and show logo image with fallback
try:
    logo_photo = load_image_safely(r"C:\Users\bhimr\Documents\Visual Studio 2022 Preview\Pomodoro_App\cats.png", (100, 120), '#ff6b6b')
    logo_label = tk.Label(window, image=logo_photo)
    logo_label.image = logo_photo  # Keep a reference
    logo_label.pack(pady=10)
except Exception as e:
    print(f"Could not load logo: {e}")
    # Continue without logo

title_label = tk.Label(window, text="Pomodoro Timer", font=("Segoe UI", 24, "bold"))
title_label.pack(pady=10)

timer_label = tk.Label(window, text="🍅 50:00 Ready", font=("Courier New", 36))
timer_label.pack(pady=10)

session_label = tk.Label(window, text="Completed: 0", font=("Segoe UI", 12))
session_label.pack()

input_frame = tk.Frame(window)
input_frame.pack(pady=10)

tk.Label(input_frame, text="Work (min):").grid(row=0, column=0, padx=5)
work_input = tk.Entry(input_frame, width=5)
work_input.insert(0, "50")
work_input.grid(row=0, column=1)

tk.Label(input_frame, text="Short Break:").grid(row=0, column=2, padx=5)
short_input = tk.Entry(input_frame, width=5)
short_input.insert(0, "10")
short_input.grid(row=0, column=3)

tk.Label(input_frame, text="Long Break:").grid(row=0, column=4, padx=5)
long_input = tk.Entry(input_frame, width=5)
long_input.insert(0, "30")
long_input.grid(row=0, column=5)

button_frame = tk.Frame(window)
button_frame.pack(pady=20)

start_button = tk.Button(button_frame, text="▶ Start", width=10, bg="#4caf50", fg="white", command=start_pomodoro)
start_button.grid(row=0, column=0, padx=5)

stop_button = tk.Button(button_frame, text="■ Stop", width=10, bg="#f44336", fg="white", command=stop_pomodoro)
stop_button.grid(row=0, column=1, padx=5)

reset_button = tk.Button(button_frame, text="⟳ Reset", width=10, bg="#607d8b", fg="white", command=reset_pomodoro)
reset_button.grid(row=0, column=2, padx=5)

theme_button = tk.Button(button_frame, text="🌗 Toggle Theme", width=15, command=toggle_theme)
theme_button.grid(row=1, column=1, pady=10)

# ---------- Animated Cat Setup ----------
setup_animated_gif()
animate_gif()

# ---------- Final Init ----------
apply_theme(current_theme)
create_tray_icon()

# Handle window closing
window.protocol("WM_DELETE_WINDOW", quit_app)

window.mainloop()