import os

# Define the directory containing your HTML files
template_folder = 'templates'

# Define the responsive meta tag and any additional CSS for responsiveness
responsive_meta = """
<meta name="viewport" content="width=device-width, initial-scale=1.0">
"""

responsive_css = """
<style>
/* Responsive images */
img {
    max-width: 100%;
    height: auto;
}

/* Responsive video */
iframe, embed, video {
    max-width: 100%;
    height: auto;
}

/* Responsive text */
body {
    font-size: 16px;
    line-height: 1.5;
}

@media screen and (max-width: 768px) {
    body {
        font-size: 14px;
    }
}

@media screen and (max-width: 480px) {
    body {
        font-size: 12px;
    }
}
</style>
"""

# Function to add responsiveness to HTML files
def add_responsiveness_to_html(file_path):
    with open(file_path, 'r+', encoding='utf-8') as file:
        content = file.read()
        if '<meta name="viewport"' not in content:
            # Insert the responsive meta tag after the opening <head> tag
            content = content.replace('<head>', f'<head>{responsive_meta}')
        if '</head>' in content:
            # Insert the responsive CSS before the closing </head> tag
            content = content.replace('</head>', f'{responsive_css}</head>')
        
        # Move the file pointer to the beginning and overwrite the content
        file.seek(0)
        file.write(content)
        file.truncate()
        
# Iterate through each HTML file in the folder
for filename in os.listdir(template_folder):
    if filename.endswith('.html'):
        file_path = os.path.join(template_folder, filename)
        add_responsiveness_to_html(file_path)

print("Responsiveness added to all HTML files.")
