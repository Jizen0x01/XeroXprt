import platform
import ctypes
import threading
import time
import os
import subprocess
import winreg
import psutil
from colorama import init, Fore
import sys


#all.bat https://pastebin.com/DjutjdK5

init(autoreset=True)

# Function to run a command
def run_command(command):
    try:
        # Execute the command
        subprocess.run(command, shell=True, check=True)
        print(f"[+] Command '{command}' executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"[-] Error executing command '{command}': {e}")

# ASCII art
art =  r"""




Y88b   d88P                      Y88b   d88P               888    
 Y88b d88P                        Y88b d88P                888    
  Y88o88P                          Y88o88P                 888    
   Y888P    .d88b. 888d888 .d88b.   Y888P   88888b. 888d888888888 
   d888b   d8P  Y8b888P"  d88""88b  d888b   888 "88b888P"  888    
  d88888b  88888888888    888  888 d88888b  888  888888    888    
 d88P Y88b Y8b.    888    Y88..88Pd88P Y88b 888 d88P888    Y88b.  
d88P   Y88b "Y8888 888     "Y88P"d88P   Y88b88888P" 888     "Y888 
                                            888                   
                                            888                   
                                            888                   



"""


if not ctypes.windll.shell32.IsUserAnAdmin():
    # Display a popup informing the user to run the script as administrator
    ctypes.windll.user32.MessageBoxW(0, "Please run this script as administrator.", "Administrator Privileges Required", 0x10)
    sys.exit()


# Function to print centered text
def print_centered(text):
    # Calculate the width of the terminal for center alignment
    terminal_width = 80  # Adjust according to your terminal width
    left_padding = (terminal_width - len(text)) // 2
    print(" " * left_padding + text)

# Function to display Windows popup for creators
def display_creators_popup():
    # Display Windows popup with the title "Credits"
    popup_text = "Winky - https://xero.gg/player/Winky\nKarthus - https://xero.gg/player/-Karthus\nDiscord: jizen"
    ctypes.windll.user32.MessageBoxW(0, popup_text, "Credits", 0x40)


def display_tool_warning():
    # Display Windows popup with a warning title
    popup_text = """
- This tool is designed to help fix common errors encountered while opening Xero, including client/launcher errors, by a high chance.
- If the issue persists, please send a ticket to the developers, as this tool is not officially verified by the game.
- Additionally, this tool sets the DNS servers to 1.1.1.1 and 8.8.8.8 for network optimization. You may change DNS manually from your PC settings if needed.
- Helps reduce ping and latency for a better experience.
"""
    ctypes.windll.user32.MessageBoxW(0, popup_text, "Warning", 0x40)


# Function to display Windows popup and ASCII art
def display_popup_and_art():
    # Print ASCII art in cyan color after a short delay
    time.sleep(1)  # Adjust the delay as needed
    print(Fore.CYAN + art.strip())  # Strip to remove trailing newline
    # Display Windows popup
    display_creators_popup()
    display_tool_warning()

# Create a new thread for displaying the popup and ASCII art
popup_thread = threading.Thread(target=display_popup_and_art)
popup_thread.start()

# Wait for the popup and art thread to complete before displaying options
popup_thread.join()




# Function to display options and prompt for user input
def display_options():
    while True:
        
        print("[*] Please Choose an Option:")
        print("[1] Fix game common errors.")
        print("[2] Start the game in optimization mode.")
        print("")
        choice = input("XeroXprt> ")

        if choice == '1':
            # Check Windows version
            check_windows_version()
            time.sleep(3)

            # Install VCRedists
            install_vc_redists()
            time.sleep(3)

            # Set DNS servers
            set_dns_servers("1.1.1.1", "8.8.8.8")
            time.sleep(3)

            # Modify registry for network throttling
            modify_registry()
            time.sleep(5)

            print("[+] Fixes applied successfully. Please reboot your pc!")
            break
        elif choice == '2':
            # Start the game
            start_game()
            print("[+] Goodbye!")
            break
        else:
            print("[-] Invalid choice. Please enter '1' or '2'.")

# Function to check Windows version
def check_windows_version():
    system, release = platform.system(), platform.release()
    if system == "Windows" and int(release) <= 7:
        print("[!] Your Windows version is Windows 7 or older.")
        print("We recommend upgrading to a newer version of Windows for better compatibility and security.")
    else:
        print("[+] Your Windows version is up-to-date.")

# Function to install VCRedists
def install_vc_redists():
    print("[!] The VCRedists are required to fix common game/client errors.")
    answer = input("[?] Do you have the VCRedists installed? (y/n): ")
    if answer.lower() == 'n':
        vcredists_folder = os.path.join(os.path.dirname(__file__), 'vcredists')
        if os.path.isdir(vcredists_folder):
            print("[+] Installing VCRedists...")
            for file_name in os.listdir(vcredists_folder):
                if file_name.endswith('.exe'):
                    print(f"[+] Installing {file_name}...")
                    subprocess.run(os.path.join(vcredists_folder, file_name), shell=True)
                    print(f"[+] {file_name} installed successfully.")
        else:
            print("[!] 'vcredists' folder not found. Please ensure it is located in the same directory as the tool.")
    elif answer.lower() == 'y':
        print("[+] Continuing with the next steps.")
    else:
        print("[-] Invalid input. Please enter 'y' or 'n'.")

# Function to set DNS servers
def set_dns_servers(primary_dns, secondary_dns):
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Services\Tcpip\Parameters", 0, winreg.KEY_ALL_ACCESS)
        winreg.SetValueEx(key, "NameServer", 0, winreg.REG_SZ, f"{primary_dns},{secondary_dns}")
        winreg.CloseKey(key)
        print("[+] DNS servers configured successfully.")
    except Exception as e:
        print("[-] Failed to configure DNS servers:", e)

# Function to modify registry for network throttling
def modify_registry():
    key_path = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile"
    value_name = "NetworkThrottlingIndex"
    value_data = 4294967295  # dword:ffffffff

    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, value_name, 0, winreg.REG_DWORD, value_data)
        print("[+] Network throttling adjusted to optimize performance for multimedia applications.")
        winreg.CloseKey(key)
    except Exception as e:
        print("[-] Error while adjusting network throttling:", e)

# Function to run a batch file as administrator
def run_batch_as_admin(batch_file):
    try:
        # Use ctypes to run the batch file as administrator
        ctypes.windll.shell32.ShellExecuteW(None, "runas", "cmd.exe", f"/c {batch_file}", None, 1)
        print(f"[+] Launching Xero with DirectX 9Ex option.")
    except Exception as e:
        print(f"[-] Error running '{batch_file}' as administrator: {e}")

# Function to start the game
def start_game():
    # Execute the start.bat file
    start_batch_file = os.path.join(os.path.dirname(__file__), "start.bat")
    if os.path.isfile(start_batch_file):
        print("[+] Starting the game...")
        run_batch_as_admin(start_batch_file)
        # Wait for xerogame.exe process to start
        while "xerogame.exe" not in (p.name() for p in psutil.process_iter()):
            time.sleep(1)
        # Change xerogame.exe process priority to high
        for process in psutil.process_iter():
            if process.name() == "xerogame.exe":
                process.nice(psutil.HIGH_PRIORITY_CLASS)
                print("[+] Priority of xerogame.exe set to high.")
                break
        print("[+] Game started successfully.")
    else:
        print("[-] 'start.bat' file not found. Please ensure it is located in the same directory as the tool.")

# Start displaying options
display_options()
input("[-] Press any key to exit.")
