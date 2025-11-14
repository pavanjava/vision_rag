import base64
from pathlib import Path


def image_to_base64(image_path) -> str:
    """Convert local image to base64 data URI"""
    with open(image_path, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode('utf-8')

    # Determine MIME type
    extension = Path(image_path).suffix.lower()
    mime_types = {
        '.png': 'image/png',
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.gif': 'image/gif',
        '.webp': 'image/webp'
    }
    mime_type = mime_types.get(extension, 'image/jpeg')

    return f"data:{mime_type};base64,{encoded}"



# Example usage
# if __name__ == "__main__":
#     # Example 1: Convert image to base64 with data URI prefix
#     base64_str = image_to_base64(image_path="output_images/0000773840-25-000105_page_6.png")
#     if base64_str:
#         print("Base64 (first 100 chars):", base64_str[:100])
#         print(f"Total length: {len(base64_str)} characters")