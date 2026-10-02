"""Week 2, Saturday: pull Zuora subscriptions to a JSON file.

Works against your Estuate partner sandbox or the mock server
(week02/mock_zuora/server.py). Settings come from .env:

    ZUORA_BASE_URL=http://localhost:8040
    ZUORA_CLIENT_ID=demo-client
    ZUORA_CLIENT_SECRET=demo-secret

Run:  python week02/zuora_pull.py
Done when: data/out/subscriptions.json holds all 25 subscriptions.

Fill in each TODO in order. Run the script after each one.
"""
import json
import os
from pathlib import Path

import httpx
from dotenv import load_dotenv

load_dotenv()
BASE = os.environ["ZUORA_BASE_URL"]


def get_token(client: httpx.Client) -> str:
    # TODO 1: POST to f"{BASE}/oauth/token" with form data (data=...)
    #   client_id, client_secret, grant_type="client_credentials".
    #   Call resp.raise_for_status(), then return resp.json()["access_token"].
    raise NotImplementedError


def fetch_all(client: httpx.Client, token: str, obj: str) -> list[dict]:
    # TODO 2: GET f"{BASE}/object-query/{obj}" with header Authorization: Bearer <token>
    #   and params pageSize=10. Collect body["data"].
    # TODO 3: While body has "nextPage", call again with params cursor=body["nextPage"].
    #   Print how many records each page returned so you can see pagination working.
    raise NotImplementedError


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
