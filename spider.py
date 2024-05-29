import requests
import re
import urllib.parse as urlparse

# Define the target URL
target_url = "central.arubanetworks.com"
# List to store discovered links
target_links = []

# Function to extract links from a webpage
def extract_links_from(url):
    # Send a GET request to the URL
    response = requests.get(url)
    # Use regular expression to find all href attributes in anchor tags
    return re.findall('(?:href=")(.*?)"', response.content.decode(errors="ignore"))

# Function to crawl and discover links recursively
def crawl(url):
    # Extract links from the current URL
    href_links = extract_links_from(url)
    # Iterate over each extracted link
    for link in href_links:
        # Join the base URL with the link
        link = urlparse.urljoin(url, link)

        # Remove any fragment identifier from the link
        if "#" in link:
            link = link.split("#")[0]

        # Check if the target URL is in the link and the link has not been visited before
        if target_url in link and link not in target_links:
            # Add the link to the list of discovered links
            target_links.append(link)
            # Print the discovered link
            print(link)
            # Recursively crawl the discovered link
            crawl(link)

# Start crawling from the target URL
crawl(target_url)

