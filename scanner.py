import aiohttp
import asyncio
from bs4 import BeautifulSoup
import os
from twilio.rest import Client
from geopy.distance import geodesic
import random

# TWILIO SETUP (PASTE YOUR INFO)
account_sid = "AC3654ca394c70286becf08906d0d8d2bb"
auth_token = "f6d2e4ef9dc34a6be5c594f81472ecc8"
twilio_number = "+18668080993"
your_number = "+1YOURPHONENUMBER"
client = Client(account_sid, auth_token)

# Your ZIP code for multi-store (add more ZIPs for coverage)
MY_ZIP = "90210"  # Change to yours
STORES_RADIUS = 20  # Miles

# AI Flip Score (Simple: higher = better flip potential)
def flip_score(title):
    high_value_keywords = ['power tool', 'ladder', 'paint', 'vacuum', 'drill', 'saw', 'sander', 'compressor']
    score = sum(1 for k in high_value_keywords if k in title.lower())
    return score * 10  # 0-100 score

def send_sms(title, url, score):
    message = f"PENNY ALERT: {title} $0.01 (Flip Score: {score}/100) → {url}"
    client.messages.create(body=message, from_=twilio_number, to=your_number)
    print(f"🚨 SMS SENT: {message}")

async def scan_store(session, store_id, zip_code):
    url = f"https://www.homedepot.com/s/clearance?storeId={store_id}"
    headers = {"User-Agent": random.choice(["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"])}
    try:
        async with session.get(url, headers=headers, timeout=5) as r:
            soup = BeautifulSoup(await r.text(), "html.parser")
            items = []
            for a in soup.select("a[data-testid='product-title']"):
                href = a.get("href")
                text = a.get_text()
                if href and ("$0.01" in text or "0.01" in text):
                    full_url = "https://www.homedepot.com" + href if href.startswith("/") else href
                    title = text.strip()[:60]
                    score = flip_score(title)
                    items.append({"title": title, "url": full_url, "score": score, "store_id": store_id})
                    if score > 50:  # High flip potential? Alert immediately
                        send_sms(title, full_url, score)
            return items
    except:
        return []

async def get_nearby_stores(zip_code):
    # Home Depot store API (public, no auth needed)
    api_url = f"https://www.homedepot.com/l/StoreFinder?zipCode={zip_code}&radius=20"
    async with aiohttp.ClientSession() as session:
        async with session.get(api_url) as r:
            # Parse JSON for store IDs (simplified - in real, use geopy for distance)
            # For demo, return 5 dummy store IDs; replace with real API parsing
            return [1001, 1002, 1003, 1004, 1005]  # Example store IDs

async def scan_all_stores(zip_code):
    stores = await get_nearby_stores(zip_code)
    async with aiohttp.ClientSession() as session:
        tasks = [scan_store(session, store, zip_code) for store in stores]
        results = await asyncio.gather(*tasks)
    all_items = [item for store in results for item in store]
    all_items.sort(key=lambda x: x['score'], reverse=True)  # Sort by flip potential
    return all_items[:10]

# Test function (run once)
if __name__ == "__main__":
    asyncio.run(scan_all_stores(MY_ZIP))