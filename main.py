import requests
import logging
from bs4 import BeautifulSoup
import re
import ssl
import random
from requests.adapters import HTTPAdapter

# Set up logging
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

# Custom adapter to use the SSL context
class SSLContextAdapter(HTTPAdapter):
    def __init__(self, *args, **kwargs):
        self.ssl_context = ssl.create_default_context()
        self.ssl_context.set_ciphers('ECDHE-RSA-AES256-GCM-SHA384')
        super().__init__(*args, **kwargs)

    def init_poolmanager(self, *args, **kwargs):
        kwargs['ssl_context'] = self.ssl_context
        return super().init_poolmanager(*args, **kwargs)
    
def fetch_hamlet_dialogue(url, timeout=10, sample_size=1, generate_html=False, html_output="hamlet_quote.html"):
    try:
        session = requests.Session()
        session.mount('https://', SSLContextAdapter())
        response = session.get(url, verify=True, timeout=timeout, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()
        html_content = response.text

        # Parse HTML with BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        dialogues = []

        # Find all <b> tags that are direct children of <a> tags with NAME starting with 'speech'
        for speech_anchor in soup.find_all('a', attrs={'name': re.compile(r'^speech', re.I)}):
            b_tag = speech_anchor.find('b')
            if not b_tag:
                continue
            character = b_tag.get_text(strip=True)
            # The next sibling should be the <blockquote> with the lines
            blockquote = speech_anchor.find_next_sibling('blockquote')
            if not blockquote:
                continue
            # Collect all lines in the blockquote
            lines = []
            for a in blockquote.find_all('a'):
                line = a.get_text(strip=True)
                if line:
                    lines.append(line + "\n")
            if lines:
                dialogues.append(f"{character}:\n {' '.join(lines)}")
        
        #size of dialogues
        print(f"Total dialogues found: {len(dialogues)}" + "\n")

        # Print a sample dialogue piece (first 5 lines)
        if dialogues:
            print("Sample Dialogue from Hamlet:\n")
            print("\t" + random.choice(dialogues))
        else:
            print("No dialogue found. Check the HTML structure or URL.")
        
        print(f"Total dialogues found: {len(dialogues)}\n")
        if dialogues and sample_size > 0:
            print("Sample Dialogue from Hamlet:\n")
            for dialogue in random.sample(dialogues, min(sample_size, len(dialogues))):
                print(f"\t{dialogue}\n")
        elif not dialogues:
            print("No dialogue found. Check the HTML structure or URL.")
        
        # Generate HTML if requested
        if generate_html and dialogues:
            random_quote = random.choice(dialogues)
            generate_html_quote(random_quote, html_output)

        return dialogues

    except requests.RequestException as e:
        print(f"Error fetching the webpage: {e}")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []
 
def generate_html_quote(quote, output_file="hamlet_quote.html"):
    """
    Generate an HTML page with a Hamlet quote in a Renaissance style.

    Args:
        quote (str): The dialogue/quote to display.
        output_file (str): Path to save the HTML file.
    """
    # Split the quote into character and dialogue
    character, dialogue = quote.split(":\n", 1) if ":\n" in quote else ("Unknown", quote)

    # HTML content with Renaissance styling
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hamlet Quote</title>
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Garamond&display=swap" rel="stylesheet">
    <style>
        body {{
            background: url('https://www.transparenttextures.com/patterns/parchment.png');
            background-color: #f4e4bc;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
            font-family: 'Garamond', serif;
            color: #3c2f2f;
        }}
        .quote-container {{
            background: rgba(255, 245, 220, 0.9);
            border: 3px solid #8b6f47;
            border-radius: 10px;
            padding: 40px;
            max-width: 600px;
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
            text-align: center;
            position: relative;
        }}
        .quote-container::before {{
            content: '';
            position: absolute;
            top: -15px;
            left: 50%;
            transform: translateX(-50%);
            width: 50px;
            height: 50px;
            background: url('https://www.transparenttextures.com/patterns/fancy-deboss.png');
            border: 2px solid #8b6f47;
            border-radius: 50%;
        }}
        h1 {{
            font-family: 'Cinzel', serif;
            font-size: 2.2em;
            color: #6b4e31;
            margin-bottom: 10px;
        }}
        .character {{
            font-weight: bold;
            font-size: 1.5em;
            color: #8b6f47;
            margin-bottom: 15px;
        }}
        .dialogue {{
            font-size: 1.2em;
            line-height: 1.6;
            white-space: pre-wrap;
            text-align: left;
        }}
        footer {{
            margin-top: 20px;
            font-size: 0.9em;
            color: #6b4e31;
        }}
    </style>
</head>
<body>
    <div class="quote-container">
        <h1>A Quote from Hamlet</h1>
        <div class="character">{character}</div>
        <div class="dialogue">{dialogue}</div>
        <footer>William Shakespeare, Hamlet</footer>
    </div>
</body>
</html>
"""

    # Write to file
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"HTML file generated: {output_file}")
    except IOError as e:
        logging.error(f"Error writing HTML file: {e}")

# Example usage
if __name__ == "__main__":
    url = "https://shakespeare.mit.edu/hamlet/full.html"
    dialogues = fetch_hamlet_dialogue(url, timeout=30, sample_size=1, generate_html=True)