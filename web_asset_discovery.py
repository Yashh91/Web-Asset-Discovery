#!/usr/bin/env python3

import argparse
import socket
import requests
from concurrent.futures import ThreadPoolExecutor

from banner import show_banner


def get_page_title(response):
    """Extract the page title from an HTTP response."""

    text = response.text
    lower_text = text.lower()

    start = lower_text.find("<title>")
    end = lower_text.find("</title>")

    if start != -1 and end != -1 and end > start:
        title = text[start + 7:end].strip()
        return title[:100]

    return "N/A"


def scan_asset(subdomain, domain):
    """Resolve a subdomain and check its web service."""

    hostname = f"{subdomain}.{domain}"

    # DNS resolution
    try:
        ip_address = socket.gethostbyname(hostname)
    except socket.gaierror:
        return None

    # Check HTTPS first, then HTTP
    for scheme in ["https", "http"]:

        url = f"{scheme}://{hostname}"

        try:
            response = requests.get(
                url,
                timeout=5,
                allow_redirects=True,
                headers={
                    "User-Agent": "Web-Asset-Discovery-Tool/1.0"
                }
            )

            title = get_page_title(response)

            return {
                "hostname": hostname,
                "ip": ip_address,
                "url": response.url,
                "status": response.status_code,
                "title": title
            }

        except requests.RequestException:
            continue

    # Host resolves but no HTTP/HTTPS response
    return {
        "hostname": hostname,
        "ip": ip_address,
        "url": "No HTTP/HTTPS response",
        "status": "N/A",
        "title": "N/A"
    }


def main():

    # Display banner
    show_banner()

    parser = argparse.ArgumentParser(
        description="Web Asset Discovery Tool"
    )

    parser.add_argument(
        "-d",
        "--domain",
        required=True,
        help="Target domain"
    )

    parser.add_argument(
        "-w",
        "--wordlist",
        default="wordlist.txt",
        help="Path to subdomain wordlist"
    )

    parser.add_argument(
        "-t",
        "--threads",
        type=int,
        default=20,
        help="Number of threads (default: 20)"
    )

    parser.add_argument(
        "-o",
        "--output",
        help="Save results to a text file"
    )

    args = parser.parse_args()

    domain = args.domain.strip()

    print(f"[*] Target   : {domain}")
    print(f"[*] Wordlist : {args.wordlist}")
    print(f"[*] Threads  : {args.threads}")

    if args.output:
        print(f"[*] Output   : {args.output}")

    print("-" * 70)

    # Load wordlist
    try:
        with open(
            args.wordlist,
            "r",
            encoding="utf-8"
        ) as file:

            subdomains = [
                line.strip()
                for line in file
                if line.strip() and not line.startswith("#")
            ]

    except FileNotFoundError:
        print(f"[-] Wordlist not found: {args.wordlist}")
        return

    print(f"[*] Loaded {len(subdomains)} subdomains")
    print("[*] Starting discovery...\n")

    discovered_assets = []

    # Multithreaded scanning
    with ThreadPoolExecutor(
        max_workers=args.threads
    ) as executor:

        results = executor.map(
            lambda subdomain: scan_asset(
                subdomain,
                domain
            ),
            subdomains
        )

        for result in results:

            if result:

                discovered_assets.append(result)

                print(
                    f"[+] {result['hostname']:<30} "
                    f"| IP: {result['ip']:<15} "
                    f"| Status: {result['status']:<3} "
                    f"| {result['title']}"
                )

    print("\n" + "=" * 70)
    print("[*] Discovery completed")
    print(
        f"[*] Web assets discovered: "
        f"{len(discovered_assets)}"
    )
    print("=" * 70)

    # Save results
    if args.output:

        try:
            with open(
                args.output,
                "w",
                encoding="utf-8"
            ) as file:

                file.write(
                    "WEB ASSET DISCOVERY RESULTS\n"
                )
                file.write("=" * 70 + "\n\n")

                for asset in discovered_assets:

                    file.write(
                        f"Host   : {asset['hostname']}\n"
                    )

                    file.write(
                        f"IP     : {asset['ip']}\n"
                    )

                    file.write(
                        f"URL    : {asset['url']}\n"
                    )

                    file.write(
                        f"Status : {asset['status']}\n"
                    )

                    file.write(
                        f"Title  : {asset['title']}\n"
                    )

                    file.write("-" * 70 + "\n")

            print(
                f"[+] Results saved to {args.output}"
            )

        except OSError as error:
            print(
                f"[-] Could not save results: {error}"
            )


if __name__ == "__main__":
    main()
