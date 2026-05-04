import os
import shutil
from pathlib import Path

def copy_configs_to_root():
    project_root = Path(__file__).parent
    config_root = project_root / "config_root"
    
    if config_root.exists():
        shutil.rmtree(config_root)
    config_root.mkdir()
    
    toml_files = list(project_root.rglob("*.toml"))
    
    for toml_file in toml_files:
        relative_path = toml_file.relative_to(project_root)
        
        parts = [p for p in relative_path.parts[:-1] if p != "config"]
        filename = relative_path.name
        
        if parts:
            new_filename = "_".join(parts) + "_" + filename
        else:
            new_filename = filename
        
        dest_path = config_root / new_filename
        
        shutil.copy2(toml_file, dest_path)
        print(f"Copied: {relative_path} -> {new_filename}")
    
    print(f"\nTotal files copied: {len(toml_files)}")
    print(f"Destination: {config_root}")

if __name__ == "__main__":
    copy_configs_to_root()
