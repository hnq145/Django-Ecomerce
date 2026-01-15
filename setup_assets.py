import os
import urllib.request

base_dir = r"c:\Users\admin\Project_05\shop\static\images"
os.makedirs(base_dir, exist_ok=True)

images = {
    "hero_1.jpg": "https://placehold.co/1920x800/1e293b/ffffff?text=New+Collection+2025",
    "women.jpg": "https://placehold.co/600x800/ec4899/ffffff?text=Women",
    "children.jpg": "https://placehold.co/600x800/f59e0b/ffffff?text=Children",
    "men.jpg": "https://placehold.co/600x800/4f46e5/ffffff?text=Men",
    "cloth_1.jpg": "https://placehold.co/600x600/cbd5e1/1e293b?text=Product+1",
    "shoe_1.jpg": "https://placehold.co/600x600/cbd5e1/1e293b?text=Product+2",
    "cloth_2.jpg": "https://placehold.co/600x600/cbd5e1/1e293b?text=Product+3",
    "cloth_3.jpg": "https://placehold.co/600x600/cbd5e1/1e293b?text=Product+4"
}

print(f"Downloading images to {base_dir}...")
for filename, url in images.items():
    try:
        urllib.request.urlretrieve(url, os.path.join(base_dir, filename))
        print(f"Downloaded {filename}")
    except Exception as e:
        print(f"Failed to download {filename}: {e}")
print("Done.")
