import requests
from bs4 import BeautifulSoup
import re
from time import sleep
import os
import random
from platform import release, node, system; Release, Node, System = release(), node(), system()

r = "\033[1;31;40m"
g = "\033[1;32;40m"
w = "\033[3;37;40m"
y = "\033[1;33;40m"

#Banner
def lightDanceEffect(text):
    colors = [
        '\033[96m', '\033[94m', '\033[92m'
    ]

    for _ in range(20):
        os.system('cls' if os.name == 'nt' else 'clear') 
        colored_text = ''.join(random.choice(colors) + char for char in text)
        print(colored_text + '\033[0m')
        sleep(0.1)

lightDanceEffect(
    f'''
    
██████╗ ██╗   ██╗ ██████╗       ███████╗██╗███╗   ██╗██████╗ ███████╗██████╗ 
██╔══██╗██║   ██║██╔════╝       ██╔════╝██║████╗  ██║██╔══██╗██╔════╝██╔══██╗
██████╔╝██║   ██║██║  ███╗█████╗█████╗  ██║██╔██╗ ██║██║  ██║█████╗  ██████╔╝
██╔══██╗██║   ██║██║   ██║╚════╝██╔══╝  ██║██║╚██╗██║██║  ██║██╔══╝  ██╔══██╗
██████╔╝╚██████╔╝╚██████╔╝      ██║     ██║██║ ╚████║██████╔╝███████╗██║  ██║
╚═════╝  ╚═════╝  ╚═════╝       ╚═╝     ╚═╝╚═╝  ╚═══╝╚═════╝ ╚══════╝╚═╝  ╚═╝
                        Made by: @Amirprx3
System:
    [+]Realese==> {Release}
    [+]Platform==> {System}
    [+]node==> {Node}

    '''
)

def find_bugs(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Check for insecure JavaScript files
        scripts = soup.find_all('script', src=True)
        for script in scripts:
            script_url = script['src']
            if not script_url.startswith(('http://', 'https://')):
                script_url = url.rstrip('/') + '/' + script_url.lstrip('/')
            try:
                script_response = requests.get(script_url)
                script_response.raise_for_status()
                script_content = script_response.text
                if re.search(r'(eval\(|Function\()', script_content):
                    print(f"{g}[✓]Potential XSS vulnerability found in {w}{script_url}")
            except requests.exceptions.RequestException as e:
                print(f"{r}[✕]Failed to fetch script {script_url}: {e}")
        
        # Check for insecure links
        links = soup.find_all('a', href=True)
        for link in links:
            href = link['href']
            if not href.startswith(('http://', 'https://')):
                href = url.rstrip('/') + '/' + href.lstrip('/')
            if href.startswith('http://'):
                print(f"{g}[✓]Insecure link found: {y}{href}")
                print(f"{r}Link Text: {w}{link.text.strip()}")
                print(f"{r}Link Location: {w}{url}")

    # Add more security checks as needed    
    except requests.exceptions.RequestException as e:
        print(f"{r}[✕]Error fetching {url}: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

def main():
    url = input(f"{g}[+]{w}Please enter the URLs you want to check: ")
        

    if not url:
        print(f"{r}[✕]No URLs provided. Exiting.")
        return
    print(f"\n{y}Checking {w}{url}")
    find_bugs(url)
    print("-" * 40)

if __name__ == "__main__":
    main()

#@Amirprx3