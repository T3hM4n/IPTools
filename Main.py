import subprocess
import platform
import time
import msvcrt
import requests
import shutil
import os
import webbrowser

# ANSI color codes
GREEN = "\033[92m"
RED = "\033[91m"
PURPLE = "\033[95m"
RESET = "\033[0m"

def clear_screen():
    os.system('cls' if platform.system().lower() == 'windows' else 'clear')

def intro_screen():
    width = shutil.get_terminal_size((80, 20)).columns
    title = "CHOOSE YOUR POISON"
    options = "1. DESTROY IP     2. CHECK WEBSITE"
    title_pos = (width - len(title)) // 2
    options_pos = (width - len(options)) // 2

    clear_screen()
    print("\n" * 5)
    print(" " * title_pos + f"{GREEN}{title}{RESET}\n")
    print("\n" * 2)
    print(" " * options_pos + f"{RED}{options}{RESET}")
    print("\n" * 2)
    print(f"{GREEN}Press 1 or 2 to choose your poison...{RESET}")

    while True:
        if msvcrt.kbhit():
            key = msvcrt.getch().decode('utf-8')
            if key in ["1", "2"]:
                return key
        time.sleep(0.1)

def is_ip_reachable(ip):
    param = "-n" if platform.system().lower() == "windows" else "-c"
    if platform.system().lower() == "windows":
        command = ["ping", param, "1", ip, "-w", "100"]
    else:
        command = ["ping", param, "1", "-W", "1", ip]

    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            print(f"{PURPLE}[+]{RESET} {PURPLE}{ip}{RESET} is {GREEN}REACHABLE ✅{RESET}")
            return True
        else:
            print(f"{RED}[-] {ip} is NOT REACHABLE ❌{RESET}")
            return False
    except Exception as e:
        print(f"{RED}Error pinging {ip}: {e}{RESET}")
        return False

def destroy_ip():
    print(f"{RED}ENTER THE IP YOU WANT TO DESTROY (press '|' to return to menu):{RESET} ", end="", flush=True)
    ip_input = ""
    while True:
        if msvcrt.kbhit():
            key = msvcrt.getch().decode('utf-8')
            if key == '|':
                print(f"\n{GREEN}Returning to main menu...{RESET}")
                time.sleep(0.5)
                clear_screen()
                return
            elif key in ('\r', '\n'):
                ip = ip_input.strip()
                if ip == "":
                    continue
                break
            elif key == '\b':
                if ip_input:
                    ip_input = ip_input[:-1]
                    print("\b \b", end="", flush=True)
            else:
                ip_input += key
                print("*", end="", flush=True)  # optional: show a placeholder instead of actual key

    print(f"\n{GREEN}Started pinging {ip} continuously. Press '|' to return to main menu.\n{RESET}")
    while True:
        start = time.time()
        is_ip_reachable(ip)
        elapsed = time.time() - start
        time.sleep(max(0, 0.1 - elapsed))  # ~10 pings/sec
        if msvcrt.kbhit():
            key = msvcrt.getch().decode('utf-8')
            if key == '|':
                print(f"\n{GREEN}Returning to main menu...{RESET}")
                time.sleep(0.5)
                clear_screen()
                break

def check_website():
    while True:
        url_input = input(f"{RED}ENTER THE WEBSITE URL (e.g., youtube.com): {RESET}").strip()
        if not url_input.startswith(("http://", "https://")):
            url = "http://" + url_input
        else:
            url = url_input

        try:
            response = requests.get(url, timeout=3)
            if response.status_code == 200:
                print(f"{GREEN}[+] Website {url_input} is UP ✅{RESET}  {PURPLE}PRESS G TO GO TO WEBSITE{RESET}  {GREEN}Do you want to check another website? (Y/N): {RESET}", end="", flush=True)
                while True:
                    if msvcrt.kbhit():
                        key = msvcrt.getch().decode('utf-8').upper()
                        # no printing of key
                        if key == 'G':
                            webbrowser.open(url)
                        elif key == 'Y':
                            clear_screen()
                            break
                        elif key == 'N' or key == '|':
                            clear_screen()
                            return
                    time.sleep(0.1)
            else:
                print(f"{RED}[-] Website {url_input} responded with status code {response.status_code} ❌{RESET}")
                print(f"{GREEN}Do you want to check another website? (Y/N): {RESET}", end="", flush=True)
                while True:
                    if msvcrt.kbhit():
                        key = msvcrt.getch().decode('utf-8').upper()
                        if key == 'Y':
                            clear_screen()
                            break
                        elif key == 'N' or key == '|':
                            clear_screen()
                            return
                    time.sleep(0.1)
        except requests.RequestException:
            print(f"{RED}[-] Website {url_input} is NOT UP ❌{RESET}")
            print(f"{GREEN}Do you want to check another website? (Y/N): {RESET}", end="", flush=True)
            while True:
                if msvcrt.kbhit():
                    key = msvcrt.getch().decode('utf-8').upper()
                    if key == 'Y':
                        clear_screen()
                        break
                    elif key == 'N' or key == '|':
                        clear_screen()
                        return
                time.sleep(0.1)

def main():
    while True:
        choice = intro_screen()
        clear_screen()
        if choice == "1":
            destroy_ip()
        elif choice == "2":
            check_website()

if __name__ == "__main__":
    main()
    