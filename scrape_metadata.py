import requests
from bs4 import BeautifulSoup

""" 
This script scrapes the title, description, and keywords from a list of URLs and saves the results to a text file (metadata_output.txt).
"""

# List of URLs to scan
urls = [
    "https://www.usaelitetraining.com", # USA Elite Training -- CT -- Home base
    "https://www.stackathlete.com", # Stack Athlete for RECRUITING - Chicago based
    "https://www.ncsasports.org/softball", # NCSA Sports FOR RECRUITING - FL based
    "https://coretrainingacademy.org/",  # Core Training Academy
    "https://www.ctgrind.com/",  # CT Grind
    "https://summersoftballcamp.com/camps/connecticut/",  # Revolution Softball Camps
    "https://www.strikezone3.com/",  # Strike Zone 3
    "https://www.allstarbatting.com/",  # All Star Batting
    "https://www.dukehartsoftballacademy.com/",  # Dukehart Softball Academy
    "https://dkacademy.com/",  # Diamond Kings
    "https://battersboxct.com/",  # Batters Box CT
    "https://www.playnsports.com/organization/lauren-pitney-softball-training-2/"  # Play ‘N Sports (Lauren Pitney)
]

# Output file path
output_file = "metadata_output.txt"

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# Writing to file
with open(output_file, "w", encoding="utf-8") as f:
    for url in urls:
        try:
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')

            title = soup.title.string if soup.title else "Not found"
            description_tag = soup.find("meta", attrs={"name": "description"})
            keywords_tag = soup.find("meta", attrs={"name": "keywords"})
            og_title = soup.find("meta", property="og:title")
            og_description = soup.find("meta", property="og:description")

            h1_tags = [tag.get_text(strip=True) for tag in soup.find_all("h1")]
            h2_tags = [tag.get_text(strip=True) for tag in soup.find_all("h2")]

            # Check for analytics scripts
            scripts = soup.find_all("script")
            has_ga = any("googletagmanager" in str(tag) or "gtag(" in str(tag) for tag in scripts)
            has_fb = any("facebook" in str(tag) for tag in scripts)

            # Count links and images
            all_links = soup.find_all("a")
            images = soup.find_all("img")

            # Write to file
            f.write(f"URL: {url}\n")
            f.write(f"Title: {title}\n")
            f.write(f"Description: {description_tag['content'] if description_tag else 'Not found'}\n")
            f.write(f"Keywords: {keywords_tag['content'] if keywords_tag else 'Not found'}\n")
            f.write(f"H1 Tags: {h1_tags if h1_tags else 'None found'}\n")
            f.write(f"H2 Tags: {h2_tags if h2_tags else 'None found'}\n")
            f.write(f"OG Title: {og_title['content'] if og_title else 'Not found'}\n")
            f.write(f"OG Description: {og_description['content'] if og_description else 'Not found'}\n")
            f.write(f"Has Google Analytics: {'Yes' if has_ga else 'No'}\n")
            f.write(f"Has Facebook Pixel: {'Yes' if has_fb else 'No'}\n")
            f.write(f"Total Links on Page: {len(all_links)}\n")
            f.write(f"Total Images on Page: {len(images)}\n")
            f.write("-" * 60 + "\n")

            print(f"🟢 Done: {url}")

        except Exception as e:
            f.write(f"URL: {url}\nError: {e}\n")
            f.write("-" * 60 + "\n")
            print(f"🔴 Error scraping {url}: {e}")

print(f"\n✅ All results saved to: {output_file}")
