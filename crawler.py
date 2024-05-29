#!/usr/bin/env python

import requests

def fetch_url(url):
    """Send a HTTP GET request to the specified URL."""
    try:
        return requests.get("http://" + url)
    except requests.exceptions.ConnectionError:
        pass

target_domain = "central.arubanetworks.com"

with open("/subdomains-list", "r") as wordlist_file:
    for line in wordlist_file:
        word = line.strip()
        test_url = target_domain + "/" + word
        response = fetch_url(test_url)
        if response:
            print("[+] Discovered URL >> " + test_url)

