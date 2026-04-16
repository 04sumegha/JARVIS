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

CRITICAL_PROCESSES = {
    "explorer.exe",
    "taskmgr.exe",
    "lsass.exe",
    "wininit.exe",
    "winlogon.exe",
    "csrss.exe",
    "services.exe",
    "svchost.exe",
    "system",
    "smss.exe"
}

def close_app(app_name: str) -> str:
    """
    Close an application using the Windows 'taskkill' command.
    """
    try:
        app_name_lower = app_name.lower()
        
        # Check against blacklist
        if app_name_lower in CRITICAL_PROCESSES or \
           (not app_name_lower.endswith(".exe") and f"{app_name_lower}.exe" in CRITICAL_PROCESSES):
            return f"Closing {app_name} is restricted as it is a critical system process."

        # Try to kill with the provided name
        result = subprocess.run(f'taskkill /F /IM "{app_name}" /T', shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            return f"Closed {app_name}"
            
        # If it failed and doesn't end in .exe, try appending .exe
        if not app_name_lower.endswith(".exe"):
            app_name_exe = app_name + ".exe"
            if app_name_exe.lower() in CRITICAL_PROCESSES:
                return f"Closing {app_name_exe} is restricted as it is a critical system process."
                
            result = subprocess.run(f'taskkill /F /IM "{app_name_exe}" /T', shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                return f"Closed {app_name_exe}"
        
        return f"Could not close {app_name}. It might not be running."

    except Exception as e:
        return f"Error closing {app_name}: {str(e)}"