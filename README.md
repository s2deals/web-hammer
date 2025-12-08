

# Web Hammer (Refactored)

> **⚠️ CRITICAL WARNING ⚠️**
>
> This tool is a Denial-of-Service (DoS) script, designed to overwhelm a target server with traffic. **Using this script against any website, server, or network that you do not own or have explicit, written permission to test is ILLEGAL in most jurisdictions and highly unethical.**
>
> Unauthorized use can lead to severe legal consequences, including fines and imprisonment. It can also cause significant harm to services, businesses, and individuals who rely on the targeted resource.
>
> **This code is provided for EDUCATIONAL PURPOSES ONLY.** It is intended to be used as a learning tool for understanding application-layer attacks, network security, and Python programming. The author of this repository and the platform hosting it are **not responsible for any misuse or damage** caused by this script. **Use responsibly and at your own risk.**

---

A refactored version of the original "Hammer Dos Script" by [shuvo-halder](https://github.com/shuvo-halder/web-hammer). Upgrade by [BinRecon](https://github.com/BinRecon) This version has been updated to follow modern Python 3 best practices, improve efficiency, and enhance robustness.

It is a Layer 7 (Application Layer) stress-testing tool that uses two primary methods to generate traffic:
1.  **Direct Socket Connections:** Sends raw HTTP GET requests directly to the target server.
2.  **Proxy Bot Requests:** Leverages third-party web services to send requests on behalf of the script.

## Features

-   **Modern Python 3:** Uses up-to-date syntax and standard library modules.
-   **Class-Based Structure:** Encapsulates logic and state for better code organization and readability.
-   **Efficient Threading:** Implements a stable threading model that correctly manages worker threads.
-   **Robust Error Handling:** Includes specific exception handling for network errors, timeouts, and user interruption.
-   **Command-Line Interface:** Uses `argparse` for a powerful and user-friendly CLI.
-   **Configurable:** Easily specify the target, port, and number of threads.
-   **Clean Logging:** Utilizes Python's `logging` module for clear, timestamped output with different verbosity levels.

## Installation

No external libraries are required. This script uses only Python's standard library.

1.  Clone or download this repository.
2.  Ensure you have Python 3.6+ installed.
3.  (Optional) Create a `headers.txt` file in the same directory to add custom HTTP headers to your requests.

## Usage

Run the script from your terminal. The only required argument is the target server.

### Basic Usage

```bash
python3 hammer.py -s example.com
```

This will start the attack against `example.com` on port 80 with the default number of threads.

### Command-Line Arguments

-   `-s`, `--server`: **(Required)** Target server IP address or domain name.
-   `-p`, `--port`: Target port (default: `80`).
-   `-t`, `--threads`: Number of threads to start for *each* hammering method. The total number of threads will be double this number (default: `50`).
-   `-q`, `--quiet`: Suppress informational messages, only show errors.
-   `-h`, `--help`: Show the help message and exit.

### Examples

**Attack a specific domain on port 443 (HTTPS) with 100 threads per method (200 total):**

```bash
python3 hammer.py -s my-target-site.com -p 443 -t 100
```

**Run in quiet mode, showing only errors:**

```bash
python3 hammer.py -s 192.168.1.10 -q
```

## Configuration

You can optionally provide a `headers.txt` file in the same directory as the script. Each line in this file should be a valid HTTP header (e.g., `Accept-Language: en-US,en;q=0.5`). These headers will be added to the raw socket requests to make them appear more legitimate.

**Example `headers.txt`:**

```
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Connection: keep-alive
```

If the file is not found, the script will use a sensible default set of headers and continue running.

## How It Works

1.  **Argument Parsing:** The script first parses the command-line arguments to get the target and configuration.
2.  **Connection Check:** It performs a quick check to ensure the target is reachable before starting the attack.
3.  **Thread Initialization:** It starts a specified number of daemon threads for each of the two attack methods.
4.  **Attack Loop:**
    *   The **socket threads** continuously open TCP connections to the target, craft a raw HTTP GET request with a random User-Agent, and send it.
    *   The **proxy threads** continuously send requests to third-party services (like the W3C validator), instructing them to fetch a page from the target URL.
5.  **Shutdown:** The main thread waits until the user presses `CTRL+C`, which gracefully signals the worker threads to stop and exits the program.

## Ethical Considerations

-   **Authorization:** Never run this script against a system you do not own or have explicit, written permission to test.
-   **Controlled Environment:** The only ethical use case is in a lab environment, testing your own systems to understand their performance limits and vulnerability to such attacks.
-   **Collateral Damage:** A DoS attack doesn't just affect the target server. It can impact shared hosting infrastructure, network providers, and other innocent users. Be aware of the potential for widespread harm.

## Original Author

This is a refactored version of the original script by [shuvo-halder](https://github.com/shuvo-halder).

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.