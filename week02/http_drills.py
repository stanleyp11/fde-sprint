"""Week 2, Wednesday: HTTP drills with httpx against the mock Zuora server.

Start the mock first (repo root):  uvicorn week02.mock_zuora.server:app --port 8040
Learn: https://www.python-httpx.org/quickstart/

Do each drill in order, printing what you get. Answers to write in your notes:
  - What status code does an unauthenticated call return? Why?
  - What is in the response headers?
"""
import httpx

BASE = "http://localhost:8040"

# Drill 1: GET /object-query/accounts with no token. Print status code and body.

# Drill 2: GET /this-does-not-exist. Print the status code. Use resp.raise_for_status()
#          inside try/except httpx.HTTPStatusError and print a friendly message.

# Drill 3: POST /oauth/token with WRONG credentials. Handle the 401 without crashing.

# Drill 4: Get a real token (client_id=demo-client, client_secret=demo-secret,
#          grant_type=client_credentials). Call /object-query/accounts?pageSize=3. Print the names.

# Drill 5: Call any endpoint with timeout=0.001 and catch httpx.TimeoutException.
