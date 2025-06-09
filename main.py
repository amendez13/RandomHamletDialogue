import requests
from bs4 import BeautifulSoup
import re
import ssl
import random
from requests.adapters import HTTPAdapter

# Custom adapter to use the SSL context
class SSLContextAdapter(HTTPAdapter):
    def __init__(self, *args, **kwargs):
        self.ssl_context = ssl.create_default_context()
        self.ssl_context.set_ciphers('ECDHE-RSA-AES256-GCM-SHA384')
        super().__init__(*args, **kwargs)

    def init_poolmanager(self, *args, **kwargs):
        kwargs['ssl_context'] = self.ssl_context
        return super().init_poolmanager(*args, **kwargs)
    
def fetch_hamlet_dialogue(url, timeout=10):
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

        return dialogues

    except requests.RequestException as e:
        print(f"Error fetching the webpage: {e}")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []
 

# Example usage
if __name__ == "__main__":
    url = "https://shakespeare.mit.edu/hamlet/full.html"
    dialogues = fetch_hamlet_dialogue(url)