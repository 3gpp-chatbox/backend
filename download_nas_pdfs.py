import os
import requests
from urllib.parse import urlsplit

# List of URLs containing the NAS and relevant spec PDFs
urls = [
    "",
    # Add more URLs here as needed
]

# Directory where PDFs will be saved
download_dir = "nas_specs_pdfs"

# Create download directory if it doesn't exist
os.makedirs(download_dir, exist_ok=True)

# Function to download a file only if it doesn't exist
def download_pdf(url):
    # Extract the file name from the URL
    file_name = os.path.basename(urlsplit(url).path)
    file_path = os.path.join(download_dir, file_name)

    # Check if the file already exists
    if os.path.exists(file_path):
        print(f"Skipping {file_name}, already exists.")
        return
    
    try:
        # Send a GET request to fetch the file
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Check if the request was successful
        
        # Write the content to the local file
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"Downloaded: {file_name}")
    
    except requests.exceptions.RequestException as e:
        print(f"Failed to download {url}: {e}")

# Loop through each URL and download only missing PDFs
for url in urls:
    download_pdf(url)

print("Download process completed.")
