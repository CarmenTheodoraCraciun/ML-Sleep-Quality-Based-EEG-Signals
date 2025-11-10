import csv
import re
import requests
from bs4 import BeautifulSoup

def fetch_files(base_url, study):
    response = requests.get(base_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    
    files = []
    for link in soup.find_all('a', href=True):
        href = link['href']
        if href.endswith(('.edf', '.hypnogram', '.txt', '.rec')):
            file_type = "psg" if "PSG" in href.upper() else "hypnogram" if "HYP" in href.upper() else "other"
            files.append({
                "filename": href,
                "link": base_url + href,
                "study": study,
                "type": file_type
            })
    return files

def main():
    urls = {
        "sc": "https://physionet.org/content/sleep-edfx/1.0.0/sleep-cassette/",
        "st": "https://physionet.org/content/sleep-edfx/1.0.0/sleep-telemetry/"
    }

    all_files = []
    for study, url in urls.items():
        print(f"Fetching files from: {url}")
        all_files.extend(fetch_files(url, study))

    with open("sleep_edf_files.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["filename", "link", "study", "type"])
        writer.writeheader()
        writer.writerows(all_files)

    print(f"Saved {len(all_files)} entries to sleep_edf_files.csv")

if __name__ == "__main__":
    main()