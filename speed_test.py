import speedtest
import threading
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import customtkinter as ctk
import time

# ---------- Setup ----------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("🌐 SpeedTest Dial")
app.geometry("600x600")
app.resizable(False, False)

# ---------- Dial Drawing ----------
fig, ax = plt.subplots(figsize=(4.5, 4.5), subplot_kw={'projection': 'polar'})
fig.patch.set_facecolor("#2c3e50")
ax.set_facecolor("#34495e")

def draw_dial(value=0, label="Testing...", color="deepskyblue", max_speed=100):
    ax.clear()
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_xticks([])
    ax.set_yticks([])
    
    # Static background arc
    arc = np.linspace(0, np.pi, 100)
    ax.plot(arc, [1]*len(arc), lw=20, color="#7f8c8d", zorder=1)

    # Dynamic dial arc
    angle = np.pi * min(value / max_speed, 1)
    ax.plot([0, angle], [0, 1], lw=4, color=color, zorder=2)

    ax.text(0, -0.2, f"{label}\n{value:.2f} Mbps", ha="center", va="center", fontsize=15, color="white", fontweight="bold")
    canvas.draw()

canvas = FigureCanvasTkAgg(fig, master=app)
canvas.get_tk_widget().pack(pady=20)

# ---------- Labels ----------
result_label = ctk.CTkLabel(app, text="Click start to test speed", font=("Segoe UI", 16))
result_label.pack(pady=5)

download_label = ctk.CTkLabel(app, text="⬇️ Download: -- Mbps", font=("Segoe UI", 14))
upload_label = ctk.CTkLabel(app, text="⬆️ Upload: -- Mbps", font=("Segoe UI", 14))
ping_label = ctk.CTkLabel(app, text="📡 Ping: -- ms", font=("Segoe UI", 14))

download_label.pack(pady=2)
upload_label.pack(pady=2)
ping_label.pack(pady=2)

# ---------- Simulate Animation ----------
def animate_speed(label_widget, dial_label, speed_value, color):
    max_display = min(speed_value, 100)  # cap at 100 Mbps
    step = max_display / 50  # smooth steps

    current = 0
    def step_update():
        nonlocal current
        if current < max_display:
            current += step
            draw_dial(current, dial_label, color)
            label_widget.configure(text=f"{dial_label}: {current:.2f} Mbps")
            app.after(20, step_update)
        else:
            draw_dial(speed_value, dial_label, color)
            label_widget.configure(text=f"{dial_label}: {speed_value:.2f} Mbps")

    step_update()

# ---------- Speed Test ----------
def perform_speedtest():
    result_label.configure(text="Testing... Please wait ⏳")
    draw_dial(0, "Testing...", color="gray")
    app.update()

    try:
        st = speedtest.Speedtest()
        st.get_best_server()

        # Download test
        download_speed = st.download() / 1_000_000
        animate_speed(download_label, "⬇️ Download", download_speed, "deepskyblue")
        time.sleep(2.5)

        # Upload test
        upload_speed = st.upload() / 1_000_000
        animate_speed(upload_label, "⬆️ Upload", upload_speed, "limegreen")
        time.sleep(2.5)

        ping = st.results.ping
        ping_label.configure(text=f"📡 Ping: {ping:.0f} ms")

        result_label.configure(text="✅ Test Complete!")
    except Exception as e:
        result_label.configure(text="❌ Test Failed")
        draw_dial(0, "Error", "red")
        download_label.configure(text="⬇️ Download: --")
        upload_label.configure(text="⬆️ Upload: --")
        ping_label.configure(text="📡 Ping: --")

# ---------- Thread Wrapper ----------
def start_test():
    threading.Thread(target=perform_speedtest).start()

# ---------- Buttons ----------
start_btn = ctk.CTkButton(app, text="🚀 Start Speed Test", command=start_test, width=200, font=("Segoe UI", 14, "bold"))
start_btn.pack(pady=10)

exit_btn = ctk.CTkButton(app, text="❌ Exit", command=app.quit, width=100, fg_color="red", hover_color="#aa0000")
exit_btn.pack(pady=10)

app.mainloop()
