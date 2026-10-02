"""Mock Zuora API for practice when you don't have sandbox access yet.

It copies the shape of the real Zuora REST API for the calls you need in
Week 2 to Week 4: OAuth token, Object Query (cursor pagination), and
subscriptions by account. Data comes from data/zuora_dataset.json (synthetic).

Run it (from the repo root):
    pip install fastapi uvicorn
    uvicorn week02.mock_zuora.server:app --port 8040 --reload

Then open http://localhost:8040/docs to see every endpoint.

Credentials: client_id=demo-client  client_secret=demo-secret

Practice failures (Week 4 Thursday): start it with
    MOCK_FAIL_RATE=0.3 uvicorn week02.mock_zuora.server:app --port 8040
and about 30% of data calls return 429 Too Many Requests with a Retry-After header.

Differences from real Zuora: one fixed data set, no writes, no field
filtering. Real base URLs depend on your tenant's data center; check the
Zuora docs or your Estuate partner sandbox login.
"""
import base64
import json
import os
import random
import secrets
import time
from pathlib import Path

from fastapi import Depends, FastAPI, Form, Header, HTTPException, Query
from fastapi.responses import JSONResponse

DATA = json.loads((Path(__file__).resolve().parents[2] / "data" / "zuora_dataset.json").read_text())
CLIENT_ID, CLIENT_SECRET = "demo-client", "demo-secret"
TOKENS: dict[str, float] = {}
FAIL_RATE = float(os.environ.get("MOCK_FAIL_RATE", "0"))

app = FastAPI(title="Mock Zuora API", version="1.0")


@app.post("/oauth/token")
def token(client_id: str = Form(...), client_secret: str = Form(...), grant_type: str = Form(...)):
    if grant_type != "client_credentials":
        raise HTTPException(400, detail="unsupported_grant_type")
    if client_id != CLIENT_ID or client_secret != CLIENT_SECRET:
        raise HTTPException(401, detail="invalid_client")
    tok = secrets.token_hex(16)
    TOKENS[tok] = time.time() + 3600
    return {"access_token": tok, "token_type": "bearer", "expires_in": 3599, "scope": "mock"}


def auth(authorization: str = Header(default="")):
    if not authorization.lower().startswith("bearer "):
        raise HTTPException(401, detail="Missing bearer token. Call POST /oauth/token first.")
    tok = authorization.split(" ", 1)[1]
    if TOKENS.get(tok, 0) < time.time():
        raise HTTPException(401, detail="Token invalid or expired.")
    if FAIL_RATE and random.random() < FAIL_RATE:
        raise HTTPException(429, detail="Too many requests", headers={"Retry-After": "1"})


def _page(rows, page_size, cursor):
    start = int(base64.b64decode(cursor).decode()) if cursor else 0
    chunk = rows[start:start + page_size]
    nxt = start + page_size
    body = {"data": chunk}
    if nxt < len(rows):
        body["nextPage"] = base64.b64encode(str(nxt).encode()).decode()
    return body


@app.get("/object-query/accounts", dependencies=[Depends(auth)])
def list_accounts(pageSize: int = Query(10, le=99), cursor: str | None = None):
    return _page(DATA["accounts"], pageSize, cursor)


@app.get("/object-query/subscriptions", dependencies=[Depends(auth)])
def list_subscriptions(pageSize: int = Query(10, le=99), cursor: str | None = None):
    return _page(DATA["subscriptions"], pageSize, cursor)


@app.get("/object-query/invoices", dependencies=[Depends(auth)])
def list_invoices(pageSize: int = Query(20, le=99), cursor: str | None = None):
    return _page(DATA["invoices"], pageSize, cursor)


@app.get("/v1/subscriptions/accounts/{account_key}", dependencies=[Depends(auth)])
def subscriptions_by_account(account_key: str):
    acct = next((a for a in DATA["accounts"] if account_key in (a["id"], a["accountNumber"])), None)
    if not acct:
        return JSONResponse({"success": False, "reasons": [{"code": 50000040, "message": f"Cannot find entity by key: '{account_key}'."}]})
    subs = [s for s in DATA["subscriptions"] if s["accountNumber"] == acct["accountNumber"]]
    return {"success": True, "subscriptions": subs}
