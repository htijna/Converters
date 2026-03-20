import os
import shutil
from datetime import datetime, timedelta

def cleanup_old_files(directory, max_age_minutes=30):
    """Deletes files in the directory that are older than max_age_minutes."""
    if not os.path.exists(directory):
        return
    
    now = datetime.now()
    for f in os.listdir(directory):
        path = os.path.join(directory, f)
        if os.path.isfile(path):
            file_age = datetime.fromtimestamp(os.path.getmtime(path))
            if now - file_age > timedelta(minutes=max_age_minutes):
                try:
                    os.remove(path)
                except Exception:
                    pass

def safe_remove(path):
    """Safely removes a file if it exists."""
    if os.path.exists(path):
        try:
            os.remove(path)
        except Exception:
            pass
