import os
from pdf2image import convert_from_path
from pathlib import Path


def pdf_to_images(pdf_path, output_folder="pdf_images", page_number=None, dpi=300):
    """
    Convert PDF pages to images.

    Args:
        pdf_path (str): Path to the PDF file
        output_folder (str): Folder to save the images (default: 'pdf_images')
        page_number (int, optional): Specific page number to convert (1-indexed).
                                     If None, converts all pages
        dpi (int): Resolution of output images (default: 300)

    Returns:
        list: Paths of saved image files
    """
    # Create output folder if it doesn't exist
    Path(output_folder).mkdir(parents=True, exist_ok=True)

    # Get PDF filename without extension
    pdf_name = Path(pdf_path).stem

    saved_files = []

    try:
        if page_number is not None:
            # Convert specific page (pdf2image uses 1-indexed pages)
            print(f"Converting page {page_number}...")
            images = convert_from_path(
                pdf_path,
                dpi=dpi,
                first_page=page_number,
                last_page=page_number
            )

            # Save the image
            output_path = os.path.join(output_folder, f"{pdf_name}_page_{page_number}.png")
            images[0].save(output_path, "PNG")
            saved_files.append(output_path)
            print(f"Saved: {output_path}")

        else:
            # Convert all pages
            print("Converting all pages...")
            images = convert_from_path(pdf_path, dpi=dpi)

            # Save all images
            for i, image in enumerate(images, start=1):
                output_path = os.path.join(output_folder, f"{pdf_name}_page_{i}.png")
                image.save(output_path, "PNG")
                saved_files.append(output_path)
                print(f"Saved: {output_path}")

        print(f"\nTotal images saved: {len(saved_files)}")
        return saved_files

    except Exception as e:
        print(f"Error converting PDF: {e}")
        return []


# Example usage
if __name__ == "__main__":
    # Example 1: Convert all pages
    pdf_to_images("../data/0000773840-25-000105.pdf", output_folder="output_images", page_number=8)

    # Example 2: Convert only page 3
    # pdf_to_images("sample.pdf", output_folder="output_images", page_number=3)

    # Example 3: Convert with custom DPI
    # pdf_to_images("sample.pdf", output_folder="output_images", dpi=150)