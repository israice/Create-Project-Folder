#!/usr/bin/env python3
import os
import re
import json
import yaml

# Settings
FOLDER_NAME = 'NEW-FOLDER'
PREFIX_WIDTH = 2

def get_base_directory():
    '''
    Read the base directory from settings.yaml if it exists.
    Otherwise, use the current working directory.
    '''
    settings_path = 'settings.yaml'
    if os.path.exists(settings_path):
        with open(settings_path, 'r', encoding='utf-8') as f:
            settings = yaml.safe_load(f)
            if settings and 'base_directory' in settings:
                return settings['base_directory']
    return '.'

# --- Root files ---

ROOT_FILES = {
    'run.py': '''import hashlib
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse

from SETTINGS import APP_TITLE, HOST, PORT, RELOAD, LIVE_RELOAD, LIVE_RELOAD_INTERVAL

app = FastAPI(title=APP_TITLE)

FRONTEND_DIR = Path(__file__).parent / "FRONTEND"


@app.get("/", response_class=HTMLResponse)
async def index():
    html = (FRONTEND_DIR / "index.html").read_text(encoding="utf-8")
    html = html.replace("{{APP_TITLE}}", APP_TITLE)
    if LIVE_RELOAD:
        script = f'<script>(async()=>{{let h=null;while(true){{try{{const r=await fetch("/api/hash");const{{hash}}=await r.json();if(h&&hash!==h)location.reload();h=hash}}catch{{}}await new Promise(r=>setTimeout(r,{LIVE_RELOAD_INTERVAL * 1000}))}}}})();</script>'
        html = html.replace("</body>", script + "</body>")
    return html


if LIVE_RELOAD:
    def _hash_frontend():
        h = hashlib.md5()
        for f in sorted(FRONTEND_DIR.rglob("*")):
            if f.is_file():
                h.update(f.read_bytes())
        return h.hexdigest()

    @app.get("/api/hash")
    async def frontend_hash():
        return {"hash": _hash_frontend()}


@app.get("/favicon.ico")
async def favicon():
    return FileResponse(FRONTEND_DIR / "favicon.svg", media_type="image/svg+xml")


if __name__ == "__main__":
    uvicorn.run("run:app", host=HOST, port=PORT, reload=RELOAD)
''',

    'SETTINGS.py': '''import os

APP_TITLE = "Tailscale Apps"
HOST = os.environ.get("HOST", "127.0.0.1")
PORT = int(os.environ.get("PORT", 8000))
RELOAD = True
LIVE_RELOAD = True
LIVE_RELOAD_INTERVAL = 3
''',

    'README.md': '''
''',

    'requirements.txt': '''fastapi
uvicorn
''',

    'docker-compose.yml': '''services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - HOST=0.0.0.0
    volumes:
      - ./FRONTEND:/app/FRONTEND
      - ./run.py:/app/run.py
    restart: unless-stopped
''',

    'Dockerfile': '''FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "run.py"]
''',

    'TASKS.md': '''# DONE

# TASKS

# FUTURE
''',

    'VERSION.md': '''# START
pip install -r requirements.txt

python run.py

# RECOVERY
git log --oneline -n 5

Copy-Item .env $env:TEMP\\.env.backup
git reset --hard 80f714fc
git clean -fd
Copy-Item $env:TEMP\\.env.backup .env -Force
git push origin master --force
python run.py

# UPDATE
git add .
git commit -m "v0.0.1 - first commit 01.03.2026"
git push
python run.py


# DEV LOG
v0.0.1 - first commit 01.03.2026
''',
}

# --- FRONTEND files ---

FRONTEND_FILES = {
    'index.html': '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{APP_TITLE}}</title>
    <link rel="icon" href="/favicon.ico" type="image/svg+xml">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            background: #0f172a;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }

        .buttons {
            display: flex;
            gap: 24px;
        }

        .btn {
            padding: 16px 48px;
            font-size: 18px;
            font-weight: 600;
            border: none;
            border-radius: 12px;
            cursor: pointer;
            transition: transform 0.15s, box-shadow 0.15s;
        }

        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
        }

        .btn:active {
            transform: translateY(0);
        }

        .btn-primary {
            background: #3b82f6;
            color: #fff;
        }

        .btn-secondary {
            background: #1e293b;
            color: #e2e8f0;
            border: 1px solid #334155;
        }
    </style>
</head>
<body>
    <div class="buttons">
        <button class="btn btn-primary">Button 1</button>
        <button class="btn btn-secondary">Button 2</button>
    </div>
</body>
</html>
''',

    'favicon.svg': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
  <rect width="32" height="32" rx="8" fill="#3b82f6"/>
  <text x="16" y="23" font-size="20" font-weight="bold" fill="#fff" text-anchor="middle" font-family="sans-serif">T</text>
</svg>
''',
}

# --- Empty directories ---

EMPTY_DIRS = ['BACKEND', 'DATA']


def get_next_prefix_number(base_dir):
    '''
    Scan the specified directory for folders with numeric prefixes and return the
    smallest positive integer not yet used.
    '''
    entries = os.listdir(base_dir)
    nums = []
    for e in entries:
        if os.path.isdir(os.path.join(base_dir, e)):
            m = re.match(r'^(\d+)-', e)
            if m:
                try:
                    nums.append(int(m.group(1)))
                except ValueError:
                    pass
    n = 1
    used = set(nums)
    while n in used:
        n += 1
    return n

def create_project_structure():
    base_dir = get_base_directory()

    num = get_next_prefix_number(base_dir)
    prefix = f"{num:0{PREFIX_WIDTH}d}"
    folder_name = f"{prefix}-{FOLDER_NAME}"

    full_path = os.path.join(base_dir, folder_name)
    os.makedirs(full_path, exist_ok=True)

    # Create root files
    for name, content in ROOT_FILES.items():
        path = os.path.join(full_path, name)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)

    # Create empty directories
    for d in EMPTY_DIRS:
        os.makedirs(os.path.join(full_path, d), exist_ok=True)

    # Create FRONTEND files
    fe_dir = os.path.join(full_path, 'FRONTEND')
    os.makedirs(fe_dir, exist_ok=True)
    for name, content in FRONTEND_FILES.items():
        with open(os.path.join(fe_dir, name), 'w', encoding='utf-8') as f:
            f.write(content)

    result = {
        "success": True,
        "folder_name": folder_name,
        "path": full_path,
        "message": f'Project "{folder_name}" created successfully'
    }
    print(json.dumps(result))


if __name__ == '__main__':
    create_project_structure()
