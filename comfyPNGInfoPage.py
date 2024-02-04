import os
import json
from PIL import Image
import webbrowser

# Directory containing the images
image_directory = '.'
html_file_path = os.path.join(image_directory, 'index.html')

# Start the HTML content
html_content = '<html><head><title>Image Gallery</title></head><body>'
html_content += '<h1>Image Gallery</h1>'

# Function to extract and format all metadata
def extract_and_format_all_metadata(metadata):
    try:
        data = json.loads(metadata)
        formatted_metadata = "<ul>"
        def format_metadata(data, prefix=""):
            nonlocal formatted_metadata
            for key, value in data.items():
                if isinstance(value, dict):
                    format_metadata(value, prefix=prefix + key + " → ")
                else:
                    formatted_metadata += f"<li>{prefix}{key}: {value}</li>"
        format_metadata(data)
        formatted_metadata += "</ul>"
        return formatted_metadata
    except json.JSONDecodeError:
        return "<p>Error parsing metadata.</p>"

# Sort files by modification time in descending order
image_files = [f for f in os.listdir(image_directory) if f.lower().endswith('.png')]
sorted_files = sorted(image_files, key=lambda x: os.path.getmtime(os.path.join(image_directory, x)), reverse=True)

# Iterate over sorted files
for filename in sorted_files:
    image_path = os.path.join(image_directory, filename)
    image = Image.open(image_path)

    # Add image to HTML
    html_content += f'<div><h2>{filename}</h2>'
    html_content += f'<img src="{filename}" alt="{filename}" style="width:300px;"><br>'

    # Extract PNG text chunks as metadata
    metadata = image.text.get("prompt", "{}")
    formatted_metadata = extract_and_format_all_metadata(metadata)
    html_content += formatted_metadata

    html_content += '</div>'

# Close the HTML content
html_content += '</body></html>'

# Write the HTML content to a file with utf-8 encoding
with open(html_file_path, 'w', encoding='utf-8') as html_file:
    html_file.write(html_content)

# Automatically open the HTML page in the default browser
webbrowser.open('file://' + os.path.realpath(html_file_path))

print(f'HTML file created and opened at {html_file_path}')
