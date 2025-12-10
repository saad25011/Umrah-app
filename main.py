from fastapi import FastAPI
import os
import platform
import requests
from mangum import Mangum  # <-- serverless adapter

app = FastAPI()

WEBHOOK_URL = "https://webhook.latenode.com/41426/dev/da2b1638-b302-4afd-9c4d-28e13d4bd84c"

def find_test2():
    folder_name = "test2"
    
    system = platform.system()
    if system == "Windows":
        start_paths = [f"{d}:\\" for d in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" if os.path.exists(f"{d}:\\")]
    else:
        start_paths = ["/", os.path.expanduser("~")]

    found_paths = []

    for start_path in start_paths:
        for root, dirs, _ in os.walk(start_path):
            if folder_name in dirs:
                full_path = os.path.join(root, folder_name)
                found_paths.append(full_path)

    return found_paths

def send_to_webhook(paths):
    payload = {"paths": paths}
    try:
        response = requests.post(WEBHOOK_URL, json=payload)
        return response.status_code
    except Exception as e:
        print("Error sending to webhook:", e)
        return None

@app.get("/")
def search_and_send_test2():
    found_paths = find_test2()

    if not found_paths:
        return {"message": "Folder 'test2' not found."}

    send_to_webhook(found_paths)
    return {"folder_name": "test2", "found_paths": found_paths}

# Wrap FastAPI app for Vercel
handler = Mangum(app)
