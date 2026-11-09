"""Check whether the Jupyter HTTP server is reachable."""

import argparse
import sys
import urllib.error
import urllib.request


def check_jupyter_health(url="http://localhost:8888", timeout=5):
    """Return True when the server responds successfully."""
    try:
        request = urllib.request.Request(
            url,
            method="GET",
        )

        with urllib.request.urlopen(
            request, timeout=timeout
        ) as response:
            return 200 <= response.status < 400

    except (
        urllib.error.URLError,
        TimeoutError,
        ValueError,
    ):
        return False


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--url",
        default="http://localhost:8888",
        help="Jupyter server URL",
    )
    args = parser.parse_args()

    if check_jupyter_health(args.url):
        print("Jupyter server is responding")
        return 0

    print("Jupyter server is unavailable")
    return 1


if __name__ == "__main__":
    sys.exit(main())
