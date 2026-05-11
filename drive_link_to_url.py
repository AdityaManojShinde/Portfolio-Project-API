import sys
import re


def extract_file_id(url):
    """Helper function to extract the unique File ID from a Google Drive URL."""
    file_id_match = re.search(r"/d/([^/]+)", url)
    if not file_id_match:
        return None
    return file_id_match.group(1)


def get_img_link(url):
    """
    Converts a Google Drive share link into a direct link
    for use in HTML <img> tags.
    """
    file_id = extract_file_id(url)
    if not file_id:
        return "Error: Invalid Google Drive URL. Make sure it contains '/d/FILE_ID'"

    return f"https://drive.google.com/uc?export=view&id={file_id}"


def get_pdf_link(url):
    """
    Converts a Google Drive share link into a preview link
    for embedding PDFs (prevents auto-download).
    """
    file_id = extract_file_id(url)
    if not file_id:
        return "Error: Invalid Google Drive URL. Make sure it contains '/d/FILE_ID'"

    return f"https://drive.google.com/file/d/{file_id}/preview"


if __name__ == "__main__":
    # Check if both a flag and a URL were provided
    if len(sys.argv) < 3:
        print(
            "Usage: python drive_converter.py [--img | --pdf] <google_drive_url>",
            file=sys.stderr,
        )
        sys.exit(1)

    # Parse arguments (Flag comes first, then URL)
    flag = sys.argv[1].lower()
    url = sys.argv[2]

    # Route to the appropriate function based on the flag
    if flag == "--img":
        result = get_img_link(url)
    elif flag == "--pdf":
        result = get_pdf_link(url)
    else:
        print("Error: Invalid flag. Please use --img or --pdf", file=sys.stderr)
        sys.exit(1)

    # Handle extraction errors
    if result.startswith("Error"):
        print(result, file=sys.stderr)
        sys.exit(1)

    # Directly print only the converted link to standard output
    print(result)
