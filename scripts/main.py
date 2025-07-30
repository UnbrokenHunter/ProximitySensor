import sys
import os

# Add the 'src' directory to the import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from tracker.Window import run

if __name__ == "__main__":
    run()
