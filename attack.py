import requests
import time
import random

url = "https://jinucloudwaf.space/function/image-resize"

# Load image once
with open("image.txt", "rb") as f:
    payload = f.read()

# min and max delay as vars ?

# counters
sent = 0
blocked = 0
success = 0

# print stuff here

try:
    while True:
        try:
            response = requests.post(url, data=payload, timeout=30)
            sent += 1

            if response.status_code == 200:
                success += 1
            elif response.status_code in (403, 429, 503):
                blocked += 1   # blocked by waf
            else:
                errors += 1    # 502 etc

            print(f"Sent: {sent} | Success: {success} | Blocked: {blocked} | Last status: {response.status_code}")

        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")

        # random delay
        delay = random.uniform(3.0, 8.0)
        time.sleep(delay)

except KeyboardInterrupt:
    print("results")