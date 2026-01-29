# Telegram @cleverestech

import requests
import os
import xml.etree.ElementTree as ET
from cryptography import x509
import argparse
from colorama import Fore, Style, init
from typing import List, Optional, Dict, Any
import logging
import sys
import shutil
import time
import concurrent.futures

# Initialize colorama
init(autoreset=True)

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(message)s')

# ANSI escape codes for bold text
BOLD = Style.BRIGHT

# Constants
CRL_URL = 'https://android.googleapis.com/attestation/status'
TIMEOUT = 10

# Global variable for workers
REVOKED_SERIALS_WORKER = set()

def fetch_crl(url: str, timeout: int = TIMEOUT) -> Optional[dict]:
    """Fetch Certificate Revocation List (CRL) with cache and cookies disabled."""
    try:
        timestamp = int(time.time())
        headers = {
            "Cache-Control": "max-age=0, no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0"
        }
        params = {"ts": timestamp}
        
        response = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=timeout
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logging.error(f"Failed to fetch or parse CRL: {e}")
        return None

def parse_cert(cert: str) -> Optional[str]:
    """Parse a certificate and return its serial number."""
    try:
        cert = "\n".join(line.strip() for line in cert.strip().split("\n"))
        parsed = x509.load_pem_x509_certificate(cert.encode())
        return f'{parsed.serial_number:x}'
    except ValueError:
        logging.error("Error parsing certificate.")
        return None

def extract_certs(file_path: str) -> Optional[List[str]]:
    """Extract certificates from Keybox files (only .xml files)."""
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        return [elem.text for elem in root.iter() if elem.tag == 'Certificate']
    except ET.ParseError:
        return None

def init_worker(revoked_serials: set):
    """Initialize worker process with revoked serial numbers."""
    global REVOKED_SERIALS_WORKER
    REVOKED_SERIALS_WORKER = revoked_serials

def process_file(file_path: str) -> Dict[str, Any]:
    """Process a single keybox file."""
    filename = os.path.basename(file_path)
    certs = extract_certs(file_path)

    if certs is None:
        return {
            'status': 'INVALID',
            'filename': filename,
            'file_path': file_path,
            'reason': 'File could not be parsed as XML.'
        }

    # Handle invalid keyboxes (insufficient certificates)
    if len(certs) < 4:
        return {
            'status': 'INVALID',
            'filename': filename,
            'file_path': file_path,
            'reason': 'Not enough certificate data.'
        }

    # Parse certificates
    ec_cert_sn = parse_cert(certs[0])
    rsa_cert_sn = parse_cert(certs[3])

    # Handle parsing errors
    if not ec_cert_sn or not rsa_cert_sn:
        return {
            'status': 'ERROR',
            'filename': filename,
            'file_path': file_path,
            'reason': 'Certificate parsing failed.'
        }

    # Check revocation status
    # Use the global set populated by init_worker
    is_revoked = False
    if ec_cert_sn in REVOKED_SERIALS_WORKER or rsa_cert_sn in REVOKED_SERIALS_WORKER:
        is_revoked = True

    return {
        'status': 'REVOKED' if is_revoked else 'VALID',
        'filename': filename,
        'file_path': file_path,
        'ec_sn': ec_cert_sn,
        'rsa_sn': rsa_cert_sn
    }

def main(directory=None, crl_data=None):
    if directory is None:
        # Setup argument parser
        parser = argparse.ArgumentParser(description='Check keybox files for certificate validity against CRL (only processes .xml files).')
        parser.add_argument('path', type=str, nargs='?', default=os.getcwd(),
                            help='Path to the directory containing keybox files (default: current directory)')
        args = parser.parse_args()
        directory = args.path

    if crl_data:
        crl = crl_data
    else:
        crl = fetch_crl(CRL_URL)
        if crl is None:
            logging.critical("Unable to proceed without a valid CRL.")
            sys.exit(1)

    # Convert CRL entries to a set of hex serial numbers for O(1) lookup
    revoked_serial_numbers = set()
    if crl and "entries" in crl:
        for sn in crl["entries"]:
            try:
                revoked_serial_numbers.add(f'{int(sn):x}')
            except ValueError:
                revoked_serial_numbers.add(sn.lower())

    total_keyboxes = revoked_keyboxes = valid_keyboxes = invalid_keyboxes = 0

    strong_keyboxes_dir = os.path.join(directory, "Strong Keyboxes")
    revoked_keyboxes_dir = os.path.join(directory, "Revoked Keyboxes")
    
    # Create target directories if they don't exist
    os.makedirs(strong_keyboxes_dir, exist_ok=True)
    os.makedirs(revoked_keyboxes_dir, exist_ok=True)

    files_to_process = []
    for filename in os.listdir(directory):
        if filename.lower().endswith('.xml'):
            files_to_process.append(os.path.join(directory, filename))

    # Parallel processing
    # Using ProcessPoolExecutor to parallelize CPU-bound tasks (XML parsing, cert loading)
    # Note: For small number of files, ThreadPoolExecutor might be faster due to lower overhead,
    # and cryptography releases GIL. However, ProcessPoolExecutor scales better for CPU heavy tasks.
    # We use ProcessPoolExecutor but fallback to ThreadPoolExecutor could be an option if spawn is too slow.
    with concurrent.futures.ProcessPoolExecutor(initializer=init_worker, initargs=(revoked_serial_numbers,)) as executor:
        # map returns results in order, but we can use as_completed if we didn't care about order.
        # Order doesn't strictly matter here, but let's just use map for simplicity or submit.
        # submit allows us to count as we go.

        futures = [executor.submit(process_file, f) for f in files_to_process]

        for future in concurrent.futures.as_completed(futures):
            total_keyboxes += 1
            try:
                result = future.result()
                filename = result['filename']
                file_path = result['file_path']
                status = result['status']

                if status == 'INVALID':
                    logging.info(f"\n{Fore.YELLOW}{BOLD}[INVALID] {filename}")
                    logging.info(f"  Reason: {result['reason']}")
                    invalid_keyboxes += 1
                    shutil.move(file_path, os.path.join(revoked_keyboxes_dir, filename))

                elif status == 'ERROR':
                    logging.info(f"\n{Fore.RED}{BOLD}[ERROR] {filename}")
                    logging.info(f"  Reason: {result['reason']}")
                    invalid_keyboxes += 1
                    shutil.move(file_path, os.path.join(revoked_keyboxes_dir, filename))

                elif status == 'REVOKED':
                    logging.info(f"\n{Fore.RED}{BOLD}[REVOKED] {filename}")
                    logging.info(f"  EC Cert Serial Number: {result['ec_sn']}")
                    logging.info(f"  RSA Cert Serial Number: {result['rsa_sn']}")
                    revoked_keyboxes += 1
                    shutil.move(file_path, os.path.join(revoked_keyboxes_dir, filename))

                elif status == 'VALID':
                    logging.info(f"\n{Fore.GREEN}{BOLD}[VALID] {filename}")
                    logging.info(f"  EC Cert Serial Number: {result['ec_sn']}")
                    logging.info(f"  RSA Cert Serial Number: {result['rsa_sn']}")
                    valid_keyboxes += 1
                    shutil.copy2(file_path, os.path.join(strong_keyboxes_dir, filename))

            except Exception as e:
                logging.error(f"Error processing file: {e}")

    # Summary Results
    logging.info("\n" + "=" * 40)
    logging.info(f"{Fore.CYAN}{BOLD}Summary:")
    logging.info(f"  Total XML files examined: {total_keyboxes}")
    logging.info(f"  Valid Certificates: {valid_keyboxes}")
    logging.info(f"  Revoked Certificates: {revoked_keyboxes}")
    logging.info(f"  Invalid Keyboxes: {invalid_keyboxes}")
    logging.info("=" * 40)

if __name__ == "__main__":
    main()
