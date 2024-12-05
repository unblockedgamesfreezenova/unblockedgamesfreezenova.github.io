import os
import re
import requests
from urllib.parse import urlparse
from PIL import Image
from io import BytesIO

# Đường dẫn thư mục gốc của dự án
project_root = r"D:\WORK\WEB-TU\new-github\pha838766\unblockedgamesfreezenova.github.io"

# Thư mục để lưu ảnh
output_folder = os.path.join(project_root, "img")
os.makedirs(output_folder, exist_ok=True)

# Mẫu URL ảnh cần tìm
image_url_pattern = r"https://math711\.github\.io/img/class-\d+\.webp"

# Hàm tìm tất cả file HTML trong thư mục
def find_html_files(root_path):
    html_files = []
    for root, _, files in os.walk(root_path):
        for file in files:
            if file.endswith(".html"):
                html_files.append(os.path.join(root, file))
    return html_files

# Hàm tải và chuyển đổi ảnh sang định dạng .webp
def download_and_convert_image(url, output_dir):
    try:
        filename = os.path.basename(urlparse(url).path).replace(".webp", ".webp")
        filepath = os.path.join(output_dir, filename)

        if os.path.exists(filepath):
            print(f"Skipped (already exists): {filename}")
            return

        # Tải ảnh từ URL
        response = requests.get(url, stream=True, timeout=10)  # Thêm timeout
        response.raise_for_status()

        # Chuyển đổi sang định dạng .webp
        image = Image.open(BytesIO(response.content))
        image.save(filepath, "webp", quality=85)
        print(f"Downloaded and converted: {filename}")

    except requests.exceptions.RequestException as e:
        print(f"Network error for {url}: {e}")
    except Exception as e:
        print(f"Failed to process {url}: {e}")

# Hàm chính để tìm và tải ảnh
def main():
    html_files = find_html_files(project_root)
    found_images = set()

    for html_file in html_files:
        try:
            with open(html_file, "r", encoding="utf-8", errors="ignore") as file:  # Bỏ qua lỗi mã hóa
                content = file.read()
                matches = re.findall(image_url_pattern, content)
                found_images.update(matches)
        except Exception as e:
            print(f"Failed to read {html_file}: {e}")

    print(f"Found {len(found_images)} unique images.")
    
    for image_url in found_images:
        download_and_convert_image(image_url, output_folder)

if __name__ == "__main__":
    main()
