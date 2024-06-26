# -*- coding: utf-8 -*-
"""proxy_checker.pyipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1hCGsw-gRceGa2qlpjwtCwzeIeswi375E
"""

# Importing Required Libraries
import feedparser
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import random
import time
from tqdm import tqdm

# Function to Generate User-Agent Headers
def generate_user_agents():
    platforms = [
        'Windows NT 10.0; Win64; x64',
        'Macintosh; Intel Mac OS X 10_15_7',
        'Macintosh; Intel Mac OS X 13_1',
        'X11; Linux x86_64',
        'X11; Ubuntu; Linux x86_64',
        'Windows NT 10.0',
        'Windows NT 6.1; Win64; x64',
    ]

    browsers = [
        'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{version} Safari/537.36',
        'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{version} Safari/537.36 Edg/{edge_version}',
        'AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
        'AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15',
    ]

    versions = ['109.0.0.0', '108.0.0.0', '107.0.0.0', '106.0.0.0', '105.0.0.0']
    edge_versions = ['109.0.1518.70', '108.0.1462.54', '107.0.1418.62']

    platform = random.choice(platforms)
    browser = random.choice(browsers)
    version = random.choice(versions)
    edge_version = random.choice(edge_versions)
    user_agent = f'Mozilla/5.0 ({platform}) ' + browser.format(version=version, edge_version=edge_version)
    return user_agent

# Function to Get Proxy List
def get_proxy_list():
    url ='https://hasdata.com/free-proxy-list'
    print(f'==>Fetching proxy list from {url}<==')
    response = requests.get(url, headers={'User-Agent': generate_user_agents()})
    soup = BeautifulSoup(response.content, 'html.parser')
    proxies = []
    proxy_table = soup.find('table', {'class': 'richtable'})
    for row in proxy_table.find('tbody').find_all('tr'):
        cells = row.find_all('td')
        protocol = cells[2].text.strip()
        if protocol == 'HTTP':
            ip = cells[0].text.strip()
            port = cells[1].text.strip()
            proxies.append(f'{ip}:{port}')
    print(f"Fetched {len(proxies)} proxies.")
    return proxies

# Function to Check and Sort Proxy Speeds
def check_proxy_speed(proxies):
    print("Checking proxy speeds ...")
    proxy_speeds = []
    for proxy in tqdm(proxies, desc="Checking proxy speeds"):
        try:
            start_time = time.time()
            response = requests.get('https://httpbin.org/ip', proxies={'http': proxy, 'https': proxy}, timeout=1, headers={'User-Agent': generate_user_agents()})
            response.raise_for_status()  # Raise an exception for HTTP errors
            end_time = time.time()
            proxy_speeds.append((proxy, end_time - start_time))
        except requests.RequestException:
            proxy_speeds.append((proxy, float('inf')))  # Assign infinity for unusable proxies

    # Sort proxies by speed (ascending order)
    sorted_proxy_speeds = sorted([p for p, speed in proxy_speeds if speed != float('inf')])
    print("Finished checking proxy speeds.")
    return sorted_proxy_speeds

# Function to Create a Session with Retry Mechanism
def create_session():
    session = requests.Session()
    retry = Retry(
        total=5,
        backoff_factor=1,
        status_forcelist=[403, 500, 502, 503, 504],  # Retry for these HTTP status codes
        allowed_methods=["HEAD", "GET", "OPTIONS"]  # Retry for these methods
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session

# Generator Function to Cycle Through Proxies
def get_next_proxy(proxies):
    for proxy in proxies:
        yield proxy
    yield None  # No proxy
