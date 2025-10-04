"""Top-level entrypoint so pygbag can package the whole repository.

This simply delegates to the existing project.main() function so the
packager includes all modules and assets that live at the repo root.
"""
import os
import sys

# Ensure repo root is on sys.path (it should already be)
ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

try:
    # project.py exposes a main() entry we can call
    from project import main
except Exception as e:
    # Provide a clear message for pygbag logs if import fails
    sys.stderr.write(f"Failed to import project.main: {e}\n")
    raise


if __name__ == '__main__':
    main()
