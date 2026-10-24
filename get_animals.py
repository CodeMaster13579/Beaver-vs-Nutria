import os
import time
import requests


ANIMAL = input("Please input animal: ")
SAVE_DIR = f"./cc0_{ANIMAL}"
os.makedirs(SAVE_DIR, exist_ok=True)

TAXON_ID = input("Please input animal ID (if multiple, seperate with comma, no spaces): ")

print(f"Fetching CC0 {ANIMAL} image links from iNaturalist...")

url = f"https://api.inaturalist.org/v1/observations?taxon_id={TAXON_ID}&quality_grade=research&license=cc0&per_page=200"
response = requests.get(url).json()

image_urls = []
for obs in response.get('results', []):
    for photo in obs.get('photos', []):
        img_url = photo.get('url', '').replace('square', 'large').replace('medium', 'large')
        if img_url:
            image_urls.append(img_url)

print(f"Found {len(image_urls)} {ANIMAL} images. Starting download...")

for i, img_url in enumerate(image_urls):
    try:
        img_data = requests.get(img_url).content
        filename = os.path.join(SAVE_DIR, f"{ANIMAL}_{i+1}.jpg")
        
        with open(filename, 'wb') as f:
            f.write(img_data)
            
        print(f"Downloaded [{i+1}/{len(image_urls)}]: {filename}")
        time.sleep(0.1)
    except Exception as e:
        print(f"Failed to download {img_url}: {e}")

print(f"\nAll images saved to: {os.path.abspath(SAVE_DIR)}")