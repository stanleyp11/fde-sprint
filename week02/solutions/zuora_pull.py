import json
import os
import time
from pathlib import Path

import httpx
from dotenv import load_dotenv

load_dotenv()
BASE = os.environ.get("ZUORA_BASE_URL", "http://localhost:8040")


def get_token(client):
    resp = client.post(f"{BASE}/oauth/token", data={
        "client_id": os.environ.get("ZUORA_CLIENT_ID", "demo-client"),
        "client_secret": os.environ.get("ZUORA_CLIENT_SECRET", "demo-secret"),
        "grant_type": "client_credentials",
    })
    resp.raise_for_status()
    return resp.json()["access_token"]


def fetch_all(client, token, obj):
    headers = {"Authorization": f"Bearer {token}"}
    rows, params = [], {"pageSize": 10}
    while True:
        resp = client.get(f"{BASE}/object-query/{obj}", headers=headers, params=params)
        if resp.status_code == 429:  # Week 4 upgrade: respect Retry-After
            time.sleep(float(resp.headers.get("Retry-After", "1")))
            continue
        resp.raise_for_status()
        body = resp.json()
        rows.extend(body["data"])
        print(f"page: {len(body['data'])} {obj}")
        if "nextPage" not in body:
            return rows
        params = {"pageSize": 10, "cursor": body["nextPage"]}


def main():
    with httpx.Client(timeout=10) as client:
        token = get_token(client)
        subs = fetch_all(client, token, "subscriptions")
    out = Path("data/out")
    out.mkdir(parents=True, exist_ok=True)
    (out / "subscriptions.json").write_text(json.dumps(subs, indent=2))
    print(f"Saved {len(subs)} subscriptions")


if __name__ == "__main__":
    main()
