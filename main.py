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
    Generate an HTML page with a Hamlet quote in an enhanced Renaissance style.

    Args:
        quote (str): The dialogue/quote to display.
        output_file (str): Path to save the HTML file.
    """
    # Split the quote into character and dialogue
    character, dialogue = quote.split(":\n", 1) if ":\n" in quote else ("Unknown", quote)

    # Format dialogue lines with indentation
    dialogue_lines = [f"    {line}" for line in dialogue.split('\n') if line.strip()]
    formatted_dialogue = '\n'.join(dialogue_lines)

    # HTML content with enhanced styling
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hamlet Quote</title>
    <link href="https://fonts.googleapis.com/css2?family=Crimson+Text:ital,wght@0,400;0,700;1,400;1,700&family=Playfair+Display:wght@700&display=swap" rel="stylesheet">
    <style>
        body {{
            background: linear-gradient(to bottom, #f5e9d3 0%, #e8d4a2 100%); /* Subtle parchment gradient */
            margin: 0;
            padding: 40px 20px;
            font-family: 'Crimson Text', serif;
            color: #2b1e1e; /* Deep brown-black */
            display: flex;
            justify-content: center;
            align-items: flex-start;
            min-height: 100vh;
        }}
        .quote-container {{
            background: #fffef0; /* Off-white parchment */
            max-width: 700px;
            padding: 30px 40px;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
            border: 1px solid #a67c00; /* Gold accent */
            position: relative;
            transition: transform 0.3s ease;
        }}
        .quote-container:hover {{
            transform: translateY(-5px); /* Subtle lift on hover */
        }}
        h1 {{
            font-family: 'Playfair Display', serif;
            font-size: 2.5em;
            color: #5c4033; /* Rich brown */
            text-align: center;
            margin-bottom: 20px;
            letter-spacing: 1px;
        }}
        .character {{
            font-size: 1.8em;
            font-weight: 700;
            color: #a67c00; /* Gold */
            text-align: center;
            margin-bottom: 15px;
            text-transform: uppercase;
        }}
        .dialogue {{
            font-size: 1.3em;
            font-style: italic;
            line-height: 1.8;
            color: #3c2f2f;
            white-space: pre-wrap;
            margin: 0 auto;
            max-width: 90%;
        }}
        .divider {{
            width: 100px;
            height: 2px;
            background: #a67c00;
            margin: 20px auto;
            opacity: 0.5;
        }}
        footer {{
            font-size: 1em;
            color: #5c4033;
            text-align: center;
            margin-top: 30px;
            font-style: italic;
        }}
        @media (max-width: 600px) {{
            .quote-container {{
                padding: 20px;
            }}
            h1 {{
                font-size: 2em;
            }}
            .character {{
                font-size: 1.5em;
            }}
            .dialogue {{
                font-size: 1.1em;
            }}
        }}
    </style>
</head>
<body>
    <div class="quote-container">
        <h1>Random Hamlet Quote</h1>
        <div class="divider"></div>
        <div class="character">{character}</div>
        <div class="dialogue">{formatted_dialogue}</div>
        <div class="divider"></div>
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
    dialogues = fetch_hamlet_dialogue(url, timeout=30, sample_size=2, generate_html=True)