from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

coupon_map = {
    "https://relianceretail.com/JioMart/?jiocpn=d9befa3d9d52d4d6c1e8ac068ddc28f5": "7Y7M5F4M7V",
    "https://relianceretail.com/JioMart/?jiocpn=dde61d114db1f0aa2789816f7938f519": "7H2H0Z5V2H",
    "https://relianceretail.com/JioMart/?jiocpn=fea55876c4c374f4cdc3dbebe97f7db5": "7A1B3E5U4P",
    "https://relianceretail.com/JioMart/?jiocpn=09fc55cdd3f98f677183d5c3390e37a2": "0F7F8F5W9Q",
    "https://relianceretail.com/JioMart/?jiocpn=96e9b1eca94ffa8a4248541e8b05b3ab": "2G5P1C7G6T",
    "https://relianceretail.com/JioMart/?jiocpn=8c45a077d2b3a01a59114a4f6545c226": "4B1G9S5H3A"
}

def get_coupon(url):
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")

        text = soup.get_text()
        for word in text.split():
            if len(word) == 10 and word.isalnum():
                return word
        return None
    except:
        return None

@app.route("/")
def check_coupons():
    results = {}
    for url, old_coupon in coupon_map.items():
        new_coupon = get_coupon(url)
        if not new_coupon:
            results[url] = "Could not fetch coupon"
        elif new_coupon == old_coupon:
            results[url] = f"Coupon: {new_coupon} (unchanged)"
        else:
            results[url] = f"Coupon: {new_coupon} (CHANGED! was {old_coupon})"
            coupon_map[url] = new_coupon
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)
