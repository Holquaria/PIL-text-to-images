import os
from PIL import Image, ImageDraw, ImageFont

# Define image dimensions
width, height = 2048, 2048

# Load a font
font_size = 48
font = ImageFont.truetype("./fonts/mussels-demibold.ttf", font_size)

# Function to add line breaks every n characters
def add_line_breaks(text, max_line_length):
    lines = []
    words = text.split()  # Split the text into words
    current_line = []

    for word in words:
        if len(" ".join(current_line + [word])) <= max_line_length:
            current_line.append(word)
        else:
            lines.append(" ".join(current_line))
            current_line = [word]

    if current_line:
        lines.append(" ".join(current_line))

    return "\n".join(lines)

# Root directory containing numbered folders
root_directory = "./claire-stories-missing-2"  # Replace with the actual path to your root directory

# Traverse the numbered folders
for folder_number in range(1796, 1797):  # Assumes folders are numbered from 1 to 2136
    folder_path = os.path.join(root_directory, str(folder_number))
    story_file_path = os.path.join(folder_path, "story.txt")

    # Check if the "story.txt" file exists in the folder
    if os.path.exists(story_file_path):
        # Read text from the "story.txt" file
        with open(story_file_path, "r") as file:
            text = file.read()

        # Format text with line breaks, limiting each line to 60 characters
        formatted_text = add_line_breaks(text, 60)

        # Create three versions of the image
        for i, (text_color, background_color, output_suffix) in enumerate(
                [("black", "white", "bump-map"), ("white", "black", "alpha-map"), ("#4efef6", "white", "color-map")]):
            # Create a new image
            image = Image.new("RGB", (width, height), background_color)
            draw = ImageDraw.Draw(image)

            # Calculate text size using the font
            text_bbox = draw.textbbox((0, 0), formatted_text, font=font)

            # Calculate text position
            x = (width - text_bbox[2]) // 2
            y = (height - text_bbox[3]) // 2

            # Draw the text on the image with the specified text color
            draw.text((x, y), formatted_text, fill=text_color, font=font)

            # Save the image as a PNG file in the same folder with the desired filename
            output_filename = f"{output_suffix}.png"
            image.save(os.path.join(folder_path, output_filename))

            # Optionally, display the image
            # image.show()
    else:
        print(f"No 'story.txt' file found in folder {folder_number}. Skipping...")
