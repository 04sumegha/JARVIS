import subprocess
import os
from difflib import get_close_matches

def discover_apps():
    app_map = {}

    paths = [
        "C:\\Program Files",
        "C:\\Program Files (x86)"
    ]

    for base in paths:
        for root, dirs, files in os.walk(base):
            for file in files:
                if file.endswith(".exe"):
                    name = file.replace(".exe", "").lower()
                    full_path = os.path.join(root, file)

                    if name not in app_map:
                        app_map[name] = full_path

    return app_map

def find_best_match(app_name, app_map):
    matches = get_close_matches(app_name.lower(), app_map.keys(), n=1, cutoff=0.6)
    if matches:
        return app_map[matches[0]]
    return None

def open_app(app_name: str) -> str:
    try:
        subprocess.Popen(f'start "" "{app_name}"', shell=True)
        return f"Opening {app_name}"
    except Exception:
        pass

    try:
        app_map = discover_apps()
        path = find_best_match(app_name, app_map)

        if path:
            subprocess.Popen(path)
            return f"Opening {app_name}"
        else:
            return f"Could not find application: {app_name}"

    except Exception as e:
        return f"Error opening {app_name}: {str(e)}"