import requests
from pathlib import Path
from tqdm import tqdm

# Target directory
target_dir = Path.home() / "retail_pipeline_project" / "assets" / "profiles"
target_dir.mkdir(parents=True, exist_ok=True)

# Download 1000 images as C1000.jpg to C1999.jpg
for i in tqdm(range(1000, 2000), desc="Downloading customer faces"):
    filename = target_dir / f"C{i}.jpg"
    if not filename.exists():
        try:
            response = requests.get("https://thispersondoesnotexist.com", timeout=10)
            if response.status_code == 200:
                with open(filename, "wb") as f:
                    f.write(response.content)
        except Exception as e:
            print(f"❌ Error for C{i}: {e}")
