import subprocess
import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk
import threading
import time
import os
import re
from colorama import Fore



def wait_for_device():
    print(Fore.LIGHTGREEN_EX + "[*] Waiting for device...")
    for _ in range(10):
        try:
            result = subprocess.check_output(["adb", "devices"], text=True)
            lines = result.strip().splitlines()
            if len(lines) > 1 and "device" in lines[1]:
                print(Fore.LIGHTGREEN_EX + "[*] Device found. Starting remote access...")
                return True
        except subprocess.SubprocessError:
            pass
        time.sleep(1)
    return False

def get_ip_address():
    output = subprocess.check_output(["adb", "shell", "ip", "addr"], text=True)
    interfaces = output.split("\n\n")

    for interface in interfaces:
        if "inet " in interface and "127.0.0.1" not in interface:
            match = re.search(r'inet (\d+\.\d+\.\d+\.\d+)', interface)
            if match:
                print(Fore.LIGHTGREEN_EX + f"[*] Device IP Address: {match.group(1)}")
                return match.group(1)
    raise Exception("Failed to retrieve IP address. Make sure the device is connected to WiFi.")

def launch_scrcpy_filtered(ip_address):
    process = subprocess.Popen(["scrcpy", "-s", f"{ip_address}:5555"],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT,
                                text=True)

    for line in process.stdout:
        if any(phrase in line for phrase in [
            "scrcpy", "https://github.com/Genymobile/scrcpy",
            "skipped.", "adb.exe:", "adb reverse", "WARN:"
        ]):
            continue
        print(line, end="")

def tcp_connect_wifi():
    try:
        if not wait_for_device():
            raise Exception("No ADB device detected. Make sure it's connected via USB and USB debugging is enabled.")

        subprocess.run(["adb", "tcpip", "5555"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(2)

        ip_address = get_ip_address()
        print(Fore.LIGHTGREEN_EX + f"[*] Attempting to connect to {ip_address}:5555 ..." + Fore.RESET)

        connect_result = subprocess.run(["adb", "connect", f"{ip_address}:5555"],
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.STDOUT,
                                        text=True)

        filtered_output = "\n".join(
            line for line in connect_result.stdout.splitlines()
            if not any(skip in line for skip in [
                "skipped.", "adb.exe:", "adb reverse", "WARN:"
            ])
        )
        if "connected" not in connect_result.stdout.lower():
            raise Exception(f"ADB connection failed:\n{filtered_output.strip()}")

        # Launch scrcpy with filtered output
        launch_scrcpy_filtered(ip_address)

        messagebox.showinfo("TCP Connection", f"Successfully connected to {ip_address}:5555")

    except subprocess.CalledProcessError as e:
        messagebox.showerror("ADB Error", f"Command failed:\n{e}")
    except Exception as e:
        messagebox.showerror("Connection Error", str(e))

def tcp_disconnect_wifi():
    try:
        target_ip = simpledialog.askstring("TCP Disconnect", "Enter the device IP (e.g., 192.168.1.123):")
        if target_ip:
            subprocess.run(["adb", "disconnect", f"{target_ip}:5555"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            messagebox.showinfo("TCP Disconnect", f"Disconnected from {target_ip}:5555")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to disconnect:\n{e}")



def check_device():
    result = subprocess.run(["adb", "devices"], capture_output=True, text=True)
    lines = result.stdout.strip().splitlines()
    if len(lines) > 1 and "device" in lines[1]:
        messagebox.showinfo("Success", "Device detected!")
    else:
        messagebox.showerror("Error", "No connected device.")

def send_popup_message():
    msg = simpledialog.askstring("Send Message", "Enter the message to send to the phone:")
    if not msg:
        return
    msg_sanitized = msg.replace(" ", "_")
    subprocess.run(["adb", "shell", "input", "text", msg_sanitized])
    messagebox.showinfo("Done", "Message sent.")

def take_screenshot():
    subprocess.run(["adb", "shell", "screencap", "-p", "/sdcard/screen.png"])
    subprocess.run(["adb", "pull", "/sdcard/screen.png", "./screen.png"])
    messagebox.showinfo("Done", "Screenshot saved as screen.png")

def open_terminal():
    subprocess.Popen(["adb", "shell"], creationflags=subprocess.CREATE_NEW_CONSOLE)



def extract_contacts():
    try:
        output = subprocess.check_output(["adb", "shell", "content", "query", "--uri", "content://contacts/phones/"], text=True)
        with open("contacts.txt", "w", encoding="utf-8") as f:
            f.write(output)
        messagebox.showinfo("Contacts", "Contacts extracted and saved to contacts.txt")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to extract contacts.\n{e}")

def extract_gallery():
    try:
        save_folder = "gallery_images"
        os.makedirs(save_folder, exist_ok=True)
        subprocess.run(["adb", "shell", "su", "-c", f"ls /sdcard/DCIM/Camera/"], stdout=subprocess.DEVNULL)
        files = subprocess.check_output(["adb", "shell", "ls", "/sdcard/DCIM/Camera/"], text=True).splitlines()
        pulled = 0
        for file in files:
            if file.lower().endswith((".jpg", ".jpeg", ".png")):
                subprocess.run(["adb", "pull", f"/sdcard/DCIM/Camera/{file}", f"{save_folder}/{file}"])
                pulled += 1
        messagebox.showinfo("Gallery", f"Downloaded {pulled} images to folder: {save_folder}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to extract images.\n{e}")
        
def start_activity():
    full_str = simpledialog.askstring("Start Activity", "Enter in form: package/activity")
    if full_str:
        subprocess.run(["adb", "shell", "am", "start", "-n", full_str])
        messagebox.showinfo(f"Started: {full_str}")

def open_url():
    url = simpledialog.askstring("Open URL", "Enter URL to open (e.g. https://example.com)")
    if url:
        subprocess.run(["adb", "shell", "am", "start", "-a", "android.intent.action.VIEW", "-d", url])
        messagebox.showinfo(f"Opened URL: {url}")

def input_text():
    txt = simpledialog.askstring("Input Text", "Enter text to send to device:")
    if txt:
        subprocess.run(["adb", "shell", "input", "text", txt.replace(" ", "%s")])
        messagebox.showinfo(f"Text sent: {txt}")

def simulate_tap():
    coords = simpledialog.askstring("Tap", "Enter X,Y coordinates (e.g., 300 800):")
    if coords:
        subprocess.run(["adb", "shell", "input", "tap"] + coords.split())
        messagebox.showinfo(f"Tapped at: {coords}")

def simulate_swipe():
    coords = simpledialog.askstring("Swipe", "Enter x1 y1 x2 y2 duration (ms):")
    if coords:
        subprocess.run(["adb", "shell", "input", "swipe"] + coords.split())
        messagebox.showinfo(f"Swipe: {coords}")

def list_packages():
    output = subprocess.check_output(["adb", "shell", "pm", "list", "packages"], text=True)
    with open("packages.txt", "w", encoding="utf-8") as f:
        f.write(output)
    messagebox.showinfo("Packages", "Package list saved to packages.txt")

def uninstall_package():
    package = simpledialog.askstring("Uninstall App", "Enter package name to uninstall:")
    if package:
        subprocess.run(["adb", "shell", "pm", "uninstall", package])
        messagebox.showinfo(f"Uninstalled: {package}")

def view_logcat():
    subprocess.Popen(["adb", "logcat"], creationflags=subprocess.CREATE_NEW_CONSOLE)

def toggle_wifi():
    state = simpledialog.askstring("WiFi", "Enter: enable or disable")
    if state in ("enable", "disable"):
        subprocess.run(["adb", "shell", "svc", "wifi", state])
        messagebox.showinfo("WiFi", f"WiFi {state}d")

def toggle_data():
    state = simpledialog.askstring("Mobile Data", "Enter: enable or disable")
    if state in ("enable", "disable"):
        subprocess.run(["adb", "shell", "svc", "data", state])
        messagebox.showinfo("Data", f"Mobile data {state}d")

        
def start_camera(front=True):
    camera_id = 1 if front else 0
    subprocess.run([
        "adb", "shell", "am", "start", 
        "-a", "android.media.action.VIDEO_CAMERA", 
        "--ez", "android.intent.extra.USE_FRONT_CAMERA", str(front).lower()
    ])
    messagebox.showinfo("Camera", f"{'Front' if front else 'Rear'} camera launched.")


def reboot_device():
    subprocess.run(["adb", "reboot"])
    messagebox.showinfo("Device is rebooting...")

def power_off_device():
    subprocess.run(["adb", "shell", "reboot", "-p"])
    messagebox.showinfo("Device is shutting down...")

def lock_screen():
    subprocess.run(["adb", "shell", "input", "keyevent", "26"])
    messagebox.showinfo("Screen locked.")

def show_battery_info():
    result = subprocess.run(["adb", "shell", "dumpsys", "battery"], capture_output=True, text=True)
    print("Battery Info:\n" + result.stdout)

def launch_app():
    package = simpledialog.askstring("Launch App", "Enter package name (e.g., com.android.chrome):")
    if package:
        subprocess.run(["adb", "shell", "monkey", "-p", package, "-c", "android.intent.category.LAUNCHER", "1"])
        messagebox.showinfo("", f"Launched: {package}")
        
def start_scrcpy():
    try:
        subprocess.Popen(["scrcpy"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except FileNotFoundError:
        messagebox.showerror("Error", "scrcpy is not installed or not in PATH.")


app = tk.Tk()
app.title("Fsociety Control Toolkit")
app.iconbitmap('fsociety.ico')
app.geometry("1080x720")
app.configure(bg="#000000")


font_title = ("Consolas", 18, "bold")
font_button = ("Consolas", 12, "bold")

center_frame = tk.Frame(app, bg="#000000")
center_frame.pack(pady=20, expand=True)

if os.path.exists("fsociety.jpg"):
    logo_img = Image.open("fsociety.jpg").resize((300, 300))
    logo_photo = ImageTk.PhotoImage(logo_img)
    tk.Label(center_frame, image=logo_photo, bg="#000000").pack()


menubar = tk.Menu(app, bg="black", fg="red", tearoff=0, font=font_button)

device_menu = tk.Menu(menubar, tearoff=0, bg="black", fg="red")
device_menu.add_command(label="Check Device", command=check_device)
device_menu.add_command(label="TCP Connect over WiFi", command=tcp_connect_wifi)
device_menu.add_command(label="TCP Disconnect", command=tcp_disconnect_wifi)
menubar.add_cascade(label="Device", menu=device_menu)

actions_menu = tk.Menu(menubar, tearoff=0, bg="black", fg="red")
actions_menu.add_command(label="Send Message", command=send_popup_message)
actions_menu.add_command(label="Take Screenshot", command=take_screenshot)
actions_menu.add_command(label="Screenshare", command=start_scrcpy)
actions_menu.add_command(label="Front Camera Preview", command=lambda: start_camera(front=True))
actions_menu.add_command(label="Rear Camera Preview", command=lambda: start_camera(front=False))
actions_menu.add_separator()
actions_menu.add_command(label="Extract Contacts", command=extract_contacts)
actions_menu.add_command(label="Extract Gallery Images", command=extract_gallery)
actions_menu.add_separator()
actions_menu.add_command(label="Battery Info", command=show_battery_info)
actions_menu.add_command(label="Launch App by Package", command=launch_app)
actions_menu.add_command(label="Lock Screen", command=lock_screen)
actions_menu.add_command(label="Reboot Device", command=reboot_device)
actions_menu.add_command(label="Power Off", command=power_off_device)
actions_menu.add_separator()
actions_menu.add_command(label="Start App Activity", command=start_activity)
actions_menu.add_command(label="Open URL in Browser", command=open_url)
actions_menu.add_command(label="Input Text to Device", command=input_text)
actions_menu.add_command(label="Simulate Tap", command=simulate_tap)
actions_menu.add_command(label="Simulate Swipe", command=simulate_swipe)
actions_menu.add_separator()
actions_menu.add_command(label="List Installed Packages", command=list_packages)
actions_menu.add_command(label="Uninstall App by Package", command=uninstall_package)
actions_menu.add_separator()
actions_menu.add_command(label="Show Logcat", command=view_logcat)
actions_menu.add_command(label="Toggle WiFi", command=toggle_wifi)
actions_menu.add_command(label="Toggle Mobile Data", command=toggle_data)
menubar.add_cascade(label="Actions", menu=actions_menu)

terminal_menu = tk.Menu(menubar, tearoff=0, bg="black", fg="red")
terminal_menu.add_command(label="Open Android Terminal", command=open_terminal)
menubar.add_cascade(label="Terminal", menu=terminal_menu)

app.config(menu=menubar)
app.mainloop()
