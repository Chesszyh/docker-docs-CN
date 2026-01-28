import os

def get_files(root_dir):
    file_list = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            # Get relative path from root_dir
            rel_dir = os.path.relpath(root, root_dir)
            if rel_dir == ".":
                rel_path = file
            else:
                rel_path = os.path.join(rel_dir, file)
            file_list.append(rel_path)
    return set(file_list)

def verify_structure(src_dir, dst_dir):
    print(f"Verifying structure between '{src_dir}' and '{dst_dir}'...")
    
    if not os.path.exists(src_dir):
        print(f"Error: Source directory '{src_dir}' does not exist.")
        return False
    
    if not os.path.exists(dst_dir):
        print(f"Error: Destination directory '{dst_dir}' does not exist.")
        return False

    src_files = get_files(src_dir)
    dst_files = get_files(dst_dir)

    missing_files = src_files - dst_files
    extra_files = dst_files - src_files

    if not missing_files and not extra_files:
        print("SUCCESS: Directory structure is identical.")
        return True
    else:
        if missing_files:
            print(f"FAILURE: Missing files in '{dst_dir}':")
            for f in sorted(missing_files):
                print(f"  - {f}")
        
        if extra_files:
            print(f"WARNING: Extra files in '{dst_dir}' (might be expected if manual additions):")
            for f in sorted(extra_files):
                print(f"  - {f}")
        
        return False

if __name__ == "__main__":
    # Check manuals/ vs zh/manuals/
    verify_structure("manuals", "zh/manuals")