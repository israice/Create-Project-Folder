#!/usr/bin/env python3
import os
import re
import json
import yaml

# Settings
# Define the descriptive name for the new folder
FOLDER_NAME = 'NEW-FOLDER'
# Number of digits for the numeric prefix (e.g., 2 -> '01', 3 -> '001')
PREFIX_WIDTH = 2
# Name of the core backend directory inside the base directory
CORE_BACKEND_DIR = os.path.join('core', 'BACKEND')

def get_base_directory():
    """
    Read the base directory from settings.yaml if it exists.
    Otherwise, use the current working directory.
    """
    settings_path = 'settings.yaml'
    if os.path.exists(settings_path):
        with open(settings_path, 'r', encoding='utf-8') as f:
            settings = yaml.safe_load(f)
            if settings and 'base_directory' in settings:
                return settings['base_directory']
    return '.'

# Additional files in the base directory with minimal content
ADDITIONAL_FILES_CONTENTS = {
    '.env': """
PORT=5039
STATIC_FOLDER=core/FRONTEND
""",

    'requirements.txt': """
flask
requests
python-dotenv
""",

    'docker-compose.yaml': """
""",

    '.gitignore': """
""",

    'README.md': """
<!-- -------------------------------------------------- -->
<!-- README.md • Project_Name • ©israice • MIT License - -->
<!-- -------------------------------------------------- -->

<h1 align="center">🧩 Project_Name</h1>

<p align="center">
  Minimalistic <b>HLS dashboard</b> built with pure&nbsp;HTML, CSS & JS.<br/>
  Click any tile to <i>unmute + fullscreen</i>; click again to exit.<br/>
  Based on m3u8 links only • No backend • No build step<br/>
</p>

<!-- -------------------------------------------------- -->
<!-- -----------------GitHub badges-------------------- -->
<!-- -------------------------------------------------- -->

<p align="center">
  <a href="https://github.com/israice/Project_Name/stargazers">
    <img alt="GitHub stars" src="https://img.shields.io/github/stars/israice/Project_Name?style=for-the-badge&logo=github" />
  </a>
  <a href="https://github.com/israice/Project_Name/forks">
    <img alt="GitHub forks" src="https://img.shields.io/github/forks/israice/Project_Name?style=for-the-badge&logo=github" />
  </a>
  <img alt="Last commit" src="https://img.shields.io/github/last-commit/israice/Project_Name?style=for-the-badge" />
</p>


<!-- -------------------------------------------------- -->
<!-- ----------------link to DEMO---------------------- -->
<!-- -------------------------------------------------- -->

## 🚀 Live Demo

> **Try it instantly:**  
> https://israice.github.io/Project_Name/

<!-- -------------------------------------------------- -->
<!-- ----------------Screenshot Preview---------------- -->
<!-- -------------------------------------------------- -->

## 📸 Preview

<p align="center">
  <img src="https://i.postimg.cc/nr8PwWmk/screenshot.png" alt="Project_Name screenshot">
</p>

<!-- -------------------------------------------------- -->
<!-- ----------------Features Table-------------------- -->
<!-- -------------------------------------------------- -->

## ✨ Features

| Check | Capability |
| :---- | :--------- |
| 🔥 **Instant setup** | clone → open `index.html` |
| 📺 **Few screens** | grid auto-fills, adapts to screen |
| 🎙 **One-click sound** | click tile: unmute + fullscreen; click again: mute + exit |
| 📡 **HLS support** | powered by <a href="https://github.com/video-dev/hls.js/">hls.js</a> |
| 🖥 **No pauses** | custom handler cancels native play/pause toggle |
| ⚡ **Zero backend**   | works on any static host / CDN |

<!-- -------------------------------------------------- -->
<!-- ----------------Configuration--------------------- -->
<!-- -------------------------------------------------- -->

## ⚙️ Configuration

connected.txt

<!-- -------------------------------------------------- -->
<!-- ----------------Contributing---------------------- -->
<!-- -------------------------------------------------- -->

## 🤝 Contributing

Fork → branch → commit feat/fix

<!-- -------------------------------------------------- -->
<!-- ----------------hide log-------------------------- -->
<!-- -------------------------------------------------- -->

<details>
  <summary>DEV Log</summary>

### v0.0.1

- Project Started date 2025.06.17
- added index.html
- added README.md with all needed
- added screenshot.png to README.md
- v0.0.1 all tested and works

### v0.0.2

- name of the repo updated in README.md
- screenshot uploaded to free hosting
- 2 dead links replaced

### FUTURE PLANS

- create and connect github pages for deployment 
- add scrolling to move all screen left and right
- create script to get all m3u8 from the source at once

### SOURCE

https://github.com/Free-TV/IPTV/tree/master/lists


<!-- -------------------------------------------------- -->
<!-- ----------------Github CHEATSHEET----------------- -->
<!-- -------------------------------------------------- -->

<details>
  <summary>Github CHEATSHEET</summary>

## Load last updates and replace existing local files

git fetch origin; git reset --hard origin/master; git clean -fd

## Select a hash from the last 10 commits

git log --oneline -n 10

## Use the hash to get that exact version locally

git fetch origin; git checkout master; git reset --hard 1eaef8b; git clean -fdx

## Update repository

git add .  
git commit -m "2 dead links replaced"  
git push

</details>

</details>

<!-- -------------------------------------------------- -->
<!-- ----------------License--------------------------- -->
<!-- -------------------------------------------------- -->

## 📄 License

Licensed under the MIT License.

<p align="center"><sub>Made with ❤️ for realtime news junkies.</sub></p>

""",

    'run.py': """
#!/usr/bin/env python3
import subprocess
import sys
import os
from dotenv import load_dotenv
from flask import Flask, send_from_directory

load_dotenv()

PORT = int(os.getenv('PORT'))
STATIC_FOLDER = os.getenv('STATIC_FOLDER')

static_path = os.path.abspath(STATIC_FOLDER)
app = Flask(__name__, static_folder=None)

@app.route('/')
def index():
    return send_from_directory(static_path, 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(static_path, filename)

for script in ("core/BACKEND/A_run.py", "core/BACKEND/B_run.py"):
    code = subprocess.call([sys.executable, script])
    if code != 0:
        sys.exit(code)

if __name__ == '__main__':
    app.run(port=PORT)
""",

    'settings.yaml': """
""",
}

# Core backend files with minimal Python code
CORE_BACKEND_FILES = {
    'A_run.py': """
#!/usr/bin/env python3
import subprocess, sys

for script in (
    "core/BACKEND/test.py",
    ):
    if subprocess.call([sys.executable, script]) != 0:
        sys.exit(1)
""",

    'B_run.py': """
#!/usr/bin/env python3
import subprocess, sys

for script in (
    "core/BACKEND/test.py",
    ):
    if subprocess.call([sys.executable, script]) != 0:
        sys.exit(1)
""",

    'test.py': """
print('- - - ✅ Test')
""",
}

# Data files under core/DATA with minimal CSV headers
DATA_FILES = {
    'data_db.csv': """
""",

    'users_db.csv': """
""",
}

# Frontend files under core/FRONTEND with minimal boilerplate
FRONTEND_FILES = {
    'index.html': """
""",

    'script.js': """
""",

    'styles.css': """
""",
}

def get_next_prefix_number(base_dir):
    """
    Scan the specified directory for folders with numeric prefixes and return the
    smallest positive integer not yet used.
    """
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
    # Get base directory from settings.yaml or use current directory
    base_dir = get_base_directory()
    
    # Next prefix and base directory name
    num = get_next_prefix_number(base_dir)
    prefix = f"{num:0{PREFIX_WIDTH}d}"
    folder_name = f"{prefix}-{FOLDER_NAME}"
    
    # Full path for the new project folder
    full_path = os.path.join(base_dir, folder_name)

    # Create base directory
    os.makedirs(full_path, exist_ok=True)

    # Create additional files
    for name, content in ADDITIONAL_FILES_CONTENTS.items():
        path = os.path.join(full_path, name)
        # Ensure parent dirs exist (for .gitignore etc.)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)

    # Create core backend dir and files
    backend_dir = os.path.join(full_path, CORE_BACKEND_DIR)
    os.makedirs(backend_dir, exist_ok=True)
    for name, content in CORE_BACKEND_FILES.items():
        with open(os.path.join(backend_dir, name), 'w', encoding='utf-8') as f:
            f.write(content)

    # Create DATA directory and CSV files
    data_dir = os.path.join(full_path, 'core', 'DATA')
    os.makedirs(data_dir, exist_ok=True)
    for name, header in DATA_FILES.items():
        with open(os.path.join(data_dir, name), 'w', encoding='utf-8') as f:
            f.write(header)

    # Create FRONTEND directory and files
    fe_dir = os.path.join(full_path, 'core', 'FRONTEND')
    os.makedirs(fe_dir, exist_ok=True)
    for name, content in FRONTEND_FILES.items():
        with open(os.path.join(fe_dir, name), 'w', encoding='utf-8') as f:
            f.write(content)

    # Output result as JSON for programmatic parsing
    result = {
        "success": True,
        "folder_name": folder_name,
        "path": full_path,
        "message": f'Project "{folder_name}" created successfully'
    }
    print(json.dumps(result))


if __name__ == '__main__':
    create_project_structure()

