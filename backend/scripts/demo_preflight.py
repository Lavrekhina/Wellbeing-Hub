"""
Run quick backend checks before live demo.

Usage:
    python backend/scripts/demo_preflight.py
    python backend/scripts/demo_preflight.py http://localhost:8000
"""

import json
import sys
from urllib.error import HTTPError, URLError
from urllib.request import urlopen


def fetch_json(url: str) -> tuple[int, dict]:
    try:
        with urlopen(url, timeout=5) as response:
            body = response.read().decode("utf-8")
            return response.status, json.loads(body)
    except HTTPError as http_error:
        payload = http_error.read().decode("utf-8")
        try:
            return http_error.code, json.loads(payload)
        except json.JSONDecodeError:
            return http_error.code, {"raw": payload}
    except URLError as url_error:
        return 0, {"error": str(url_error)}


def main() -> int:
    base_url = sys.argv[1].rstrip("/") if len(sys.argv) > 1 else "http://localhost:8000"
    checks = [
        ("health", f"{base_url}/health", 200),
        ("readiness", f"{base_url}/health/readiness", 200),
    ]

    has_failures = False
    for name, url, expected_status in checks:
        status_code, payload = fetch_json(url)
        ok = status_code == expected_status
        if not ok:
            has_failures = True
        print(f"[{name}] status={status_code} expected={expected_status} ok={ok}")
        print(f"  payload={payload}")

    if has_failures:
        print("Demo preflight FAILED")
        return 1

    print("Demo preflight PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
