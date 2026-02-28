"""Basic healthcheck utility for container/runtime probes."""

import argparse
import sys
import urllib.request


def probe(url: str, timeout_seconds: int) -> int:
    try:
        with urllib.request.urlopen(url, timeout=timeout_seconds) as response:  # nosec B310
            return 0 if response.status == 200 else 1
    except Exception:
        return 1


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default="http://127.0.0.1:8501/_stcore/health")
    parser.add_argument("--timeout", type=int, default=5)
    args = parser.parse_args()
    sys.exit(probe(args.url, args.timeout))


if __name__ == "__main__":
    main()
