import os
from pathlib import Path

def validate_env():
    print("🔍 Scanning environment configuration...\n")
    
    if not Path(".env.example").exists() or not Path(".env").exists():
        print("Error: Missing .env or .env.example file.")
        return

    example_keys = set()
    with open(".env.example", "r") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                key = line.split("=")[0].strip()
                example_keys.add(key)

    local_keys = set()
    with open(".env", "r") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                key = line.split("=")[0].strip()
                local_keys.add(key)

    missing = example_keys - local_keys
    extra = local_keys - example_keys

    if not missing and not extra:
        print("✅ Environment configuration is fully synchronized and valid!")
    else:
        if missing:
            print(f"❌ Missing keys in your local .env: {list(missing)}")
        if extra:
            print(f"⚠️ Extra keys in your local .env not found in example: {list(extra)}")

if __name__ == "__main__":
    validate_env()
