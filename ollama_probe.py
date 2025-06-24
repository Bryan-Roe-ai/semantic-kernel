import httpx

endpoints = [
    "http://localhost:11434/api/generate",
    "http://localhost:11434/api/chat",
    "http://localhost:11434/api/tags",
    "http://localhost:11434/",
]

for url in endpoints:
    try:
        print(f"Testing: {url}")
        resp = httpx.get(url, timeout=5)
        print(f"Status: {resp.status_code}")
        print(f"Body: {resp.text[:200]}\n")
    except Exception as e:
        print(f"Error: {e}\n")
