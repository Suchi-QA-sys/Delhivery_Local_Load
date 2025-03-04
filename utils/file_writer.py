import os

def write_to_file(file_name, content):
    """
    Writes the given content to a .txt file.
    - If the file does not exist, it creates one.
    - Appends content to the existing file.

    :param file_name: Name of the file (without extension).
    :param content: String content to write.
    """
    file_path = f"{file_name}.txt"

    with open(file_path, "a") as file:  # Open in append mode
        file.write(content + "\n")

    print(f"✅ Content written to {file_path}")
