import requests
from bs4 import BeautifulSoup
from urllib.robotparser import RobotFileParser
from urllib.parse import urljoin, urlparse
import time
import json
from pathlib import Path
import logging
from typing import List, Dict, Set

class EthicalWebScraper:
    def __init__(self, base_url: str, output_dir: str = "scraped_data"):
        self.base_url = base_url
        self.domain = urlparse(base_url).netloc
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.visited_urls: Set[str] = set()
        self.rate_limit = 1  # Delay between requests in seconds
        
        # Setup logging
        logging.basicConfig(
            filename=self.output_dir / "scraping.log",
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
        # Setup robots.txt parser
        self.rp = RobotFileParser()
        self.rp.set_url(urljoin(base_url, "/robots.txt"))
        try:
            self.rp.read()
        except Exception as e:
            self.logger.error(f"Error reading robots.txt: {e}")

    def is_allowed(self, url: str) -> bool:
        """Check if scraping is allowed for this URL according to robots.txt"""
        return self.rp.can_fetch("*", url)

    def get_page_content(self, url: str) -> tuple[str, List[str]]:
        """Retrieve page content and extract links"""
        headers = {
            'User-Agent': 'Ethical Web Scraper for Document Creation/1.0 (Respects robots.txt)',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9',
        }
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove unwanted elements
        for element in soup.find_all(['script', 'style', 'nav', 'footer', 'header']):
            element.decompose()
        
        # Extract main content
        content = ' '.join(soup.get_text().split())
        
        # Extract links
        links = []
        for link in soup.find_all('a', href=True):
            full_url = urljoin(url, link['href'])
            if self.domain in full_url and full_url not in self.visited_urls:
                links.append(full_url)
                
        return content, links

    def create_document(self, url: str, content: str) -> Dict:
        """Create a structured document from the scraped content"""
        return {
            'url': url,
            'content': content,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'title': urlparse(url).path,
            'domain': self.domain
        }

    def scrape_site(self, max_pages: int = 100) -> List[Dict]:
        """Main scraping function that crawls the website and creates documents"""
        documents = []
        urls_to_visit = [self.base_url]
        
        while urls_to_visit and len(documents) < max_pages:
            url = urls_to_visit.pop(0)
            
            if url in self.visited_urls:
                continue
                
            if not self.is_allowed(url):
                self.logger.warning(f"Scraping not allowed for: {url}")
                continue
                
            try:
                self.logger.info(f"Scraping: {url}")
                content, new_links = self.get_page_content(url)
                
                # Create and save document
                doc = self.create_document(url, content)
                documents.append(doc)
                
                # Save individual documents as JSON
                doc_filename = self.output_dir / f"doc_{len(documents)}.json"
                with open(doc_filename, 'w', encoding='utf-8') as f:
                    json.dump(doc, f, ensure_ascii=False, indent=2)
                
                # Update tracking
                self.visited_urls.add(url)
                urls_to_visit.extend(new_links)
                
                # Respect rate limiting
                time.sleep(self.rate_limit)
                
            except Exception as e:
                self.logger.error(f"Error scraping {url}: {e}")
                continue
        
        # Save full dataset
        dataset_path = self.output_dir / "full_dataset.json"
        with open(dataset_path, 'w', encoding='utf-8') as f:
            json.dump(documents, f, ensure_ascii=False, indent=2)
            
        return documents

def main():
    # Example usage
    website_url = "https://example.com"  # Replace with target website
    scraper = EthicalWebScraper(website_url, "scraped_documents")
    documents = scraper.scrape_site(max_pages=50)
    print(f"Successfully scraped {len(documents)} pages")

if __name__ == "__main__":
    main()
