#!/usr/bin/env python3
import json
from pathlib import Path

MANIFEST_PATH = "../pocca/target/manifest.json"
CUBES_DIR = Path("./model/cubes")

def main():
    with open(MANIFEST_PATH) as f:
        manifest = json.load(f)

    cube_files = list(CUBES_DIR.glob("*.js"))

    for sm_id, sm_data in manifest.get("semantic_models", {}).items():
        sm_name = sm_data.get("name")
        if not sm_name:
            continue

        # Case-insensitive file matching
        cube_file = next(
            (f for f in cube_files if f.stem.lower() == sm_name.lower()),
            None
        )
        if not cube_file:
            continue

        meta = sm_data.get("config", {}).get("meta", {})
        if not meta:
            continue

        # Format: Owner: CBS | Steward: Jelle | Email: j@j.nl | Contains Pii: false
        meta_str = " | ".join(f"{k.replace('_', ' ').title()}: {v}" for k, v in meta.items())

        with open(cube_file) as f:
            content = f.read()

        # Simple string replacement - no regex
        old_line = "  dimensions: {"
        new_line = f"description: `{meta_str}`, \n  dimensions: {{"

        if old_line in content:
            content = content.replace(old_line, new_line, 1)

        with open(cube_file, "w") as f:
            f.write(content)

        print(f"✅ Updated: {cube_file.name}")

if __name__ == "__main__":
    main()