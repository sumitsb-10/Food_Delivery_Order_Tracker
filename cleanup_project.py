
from pathlib import Path
import argparse
import shutil

PROJECT_ROOT = Path(__file__).resolve().parent

# Safe to regenerate: Python and pytest will recreate these.
CACHE_DIR_NAMES = {
    "__pycache__",
    ".pytest_cache",
}

# Possible manual/debug scripts. Review before removing.
OPTIONAL_FILES = [
    "database/create_order.py",
    "database/update_order.py",
    "database/view_db.py",
    "database/view_orders.py",
    "tests/check_order_items.py",
]

def main():
    parser = argparse.ArgumentParser(
        description="Clean generated files from the project."
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Actually delete files. Without this flag, only preview.",
    )
    parser.add_argument(
        "--remove-debug-scripts",
        action="store_true",
        help="Also remove the listed optional debug scripts.",
    )
    args = parser.parse_args()

    targets = []

    # Find generated cache folders.
    for path in PROJECT_ROOT.rglob("*"):
        if not path.is_dir():
            continue

        if path.name in CACHE_DIR_NAMES:
            # Do not scan inside a cache folder again.
            targets.append(path)

    # Include optional scripts only when explicitly requested.
    if args.remove_debug_scripts:
        for relative_path in OPTIONAL_FILES:
            path = PROJECT_ROOT / relative_path
            if path.is_file():
                targets.append(path)

    # Remove duplicate paths and process deepest paths first.
    targets = sorted(
        set(targets),
        key=lambda path: len(path.parts),
        reverse=True,
    )

    if not targets:
        print("Nothing to clean.")
        return

    print("Cleanup preview:" if not args.apply else "Cleaning project:")

    for path in targets:
        print(f"  {path.relative_to(PROJECT_ROOT)}")

        if args.apply:
            if path.is_dir():
                shutil.rmtree(path)
            elif path.is_file():
                path.unlink()

    if args.apply:
        print("\nCleanup complete.")
    else:
        print("\nPreview only. No files were deleted.")
        print("Run with --apply to delete the listed files.")


if __name__ == "__main__":
    main()
