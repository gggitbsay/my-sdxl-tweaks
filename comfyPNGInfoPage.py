import os
import json
from PIL import Image
import webbrowser

# Use in current directory
image_directory = '.'
html_file_path = os.path.join(image_directory, 'index.html')

# Create the HTML content
html_content = '<html><head><title>Image Gallery</title></head><body>'
html_content += '<h1>Image Gallery</h1>'

def extract_and_format_all_metadata(metadata):
    try:
        # Parse the metadata, which is expected to be in JSON format
        data = json.loads(metadata)
        formatted_metadata = "<ul>"

        # Define the recursive function to format metadata
        def format_metadata(data, prefix=""):
            nonlocal formatted_metadata  # This line makes formatted_metadata accessible and modifiable within format_metadata
            for key, value in data.items():
                if isinstance(value, dict):
                    # Recurse into sub-dictionaries
                    format_metadata(value, prefix=prefix + key + " → ")
                else:
                    # Add the key-value pair to the list
                    formatted_metadata += f"<li>{prefix}{key}: {value}</li>"

        format_metadata(data)
        formatted_metadata += "</ul>"
        return formatted_metadata
    except json.JSONDecodeError:
        return "<p>Error parsing metadata.</p>"

# Iterate over images in the directory
for filename in os.listdir(image_directory):
    if filename.lower().endswith('.png'):
        image_path = os.path.join(image_directory, filename)
        image = Image.open(image_path)

        # Add image to HTML
        html_content += f'<div><h2>{filename}</h2>'
        html_content += f'<img src="{filename}" alt="{filename}" style="width:300px;"><br>'

        # Extract PNG text chunks as metadata
        metadata = image.text.get("prompt", "{}")  # Assuming 'prompt' is the key for your metadata
        formatted_metadata = extract_and_format_all_metadata(metadata)
        html_content += formatted_metadata

        html_content += '</div>'

# Close the HTML content
html_content += '</body></html>'

# Write the HTML content to a file with utf-8 encoding
with open(html_file_path, 'w', encoding='utf-8') as html_file:
    html_file.write(html_content)

# Automatically open page in the default browser
webbrowser.open('file://' + os.path.realpath(html_file_path))

print(f'HTML file created and opened at {html_file_path}')
