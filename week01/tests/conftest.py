import os
import sys
from pathlib import Path

# Lets the tests import your week01 files. Set CHECK_SOLUTIONS=1 to run them against the reference solutions instead.
week = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(week / "solutions" if os.environ.get("CHECK_SOLUTIONS") else week))
