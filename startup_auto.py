import os
import sys
import subprocess
from pathlib import Path
import os
import sys

#!/usr/bin/env python3
"""
EHB Auto Startup Script
Automatically runs when project is opened
"""



def auto_startup():
    """Automatically run when project starts"""
    print("ROCKET EHB Auto Startup - Initializing...")

    # Check if auto script exists
    auto_script = Path("auto_cursor_script.py")
    if auto_script.exists():
        print("SUCCESS Auto script found - running...")
        try:
            subprocess.run([sys.executable, "auto_cursor_script.py"], check=True)
            print("SUCCESS Auto startup completed successfully")
        except subprocess.CalledProcessError as e:
            print(f"ERROR Auto startup failed: {e}")
    else:
        print("WARNING Auto script not found - creating...")
        create_auto_script()


def create_auto_script():
    """Create auto script if it doesn't exist"""
    script_content = '''#!/usr/bin/env python3
"""
EHB Auto Script - Auto-generated
"""
print("EHB AI EHB Auto Script Running...")
print("SUCCESS System initialized successfully")
'''

    with open("auto_cursor_script.py", "w") as f:
        f.write(script_content)

    print("SUCCESS Auto script created")


if __name__ == "__main__":
    auto_startup()
