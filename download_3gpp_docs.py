import os
import requests
import zipfile
from typing import Dict

class DocumentDownloader:
    def __init__(self):
        self.base_dir = "3GPP_Documents"
        self.documents = {
            "TS_24_501": {"url": "https://www.3gpp.org/ftp/Specs/archive/24_series/24.501/24501-j11.zip", "filename": "24501-j11.zip"},
            "TS_23_501": {"url": "https://www.3gpp.org/ftp/Specs/archive/23_series/23.501/23501-j21.zip", "filename": "23501-j21.zip"},
            "TS_23_502": {"url": "https://www.3gpp.org/ftp/Specs/archive/23_series/23.502/23502-j20.zip", "filename": "23502-j20.zip"},
            "TS_38_331": {"url": "https://www.3gpp.org/ftp/Specs/archive/38_series/38.331/38331-i40.zip", "filename": "38331-i40.zip"},
            "TS_24_301": {"url": "https://www.3gpp.org/ftp/Specs/archive/24_series/24.301/24301-j10.zip", "filename": "24301-j10.zip"}
        }

    def download_file(self, url: str, save_path: str):
        """Download a file from URL"""
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Downloaded: {save_path}")

    def unzip_file(self, zip_path: str, extract_dir: str):
        """Unzip file to specified directory"""
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
        print(f"Unzipped to: {extract_dir}")

    def download_and_unzip_all(self):
        """Download and unzip all documents"""
        os.makedirs(self.unzip_dir, exist_ok=True)
        for spec_name, doc_info in self.documents.items():
            spec_dir = os.path.join(self.unzip_dir, spec_name)
            os.makedirs(spec_dir, exist_ok=True)
            zip_path = os.path.join(spec_dir, doc_info['filename'])

            if not os.path.exists(zip_path):
                print(f"Downloading {doc_info['filename']}...")
                self.download_file(doc_info['url'], zip_path)
            else:
                print(f"File already exists: {zip_path}")
            
            self.unzip_file(zip_path, spec_dir)


def main():
    downloader = DocumentDownloader()
    downloader.download_and_unzip_all()

if __name__ == "__main__":
    main()
