import os

def get_structure(root_dir):
    structure = set()
    for root, dirs, files in os.walk(root_dir):
        for name in files:
            rel_dir = os.path.relpath(root, root_dir)
            structure.add(os.path.join(rel_dir, name))
    return structure

guides_structure = get_structure('guides')
zh_guides_structure = get_structure('zh/guides')

missing_in_zh = guides_structure - zh_guides_structure
extra_in_zh = zh_guides_structure - guides_structure

if not missing_in_zh and not extra_in_zh:
    print("Verification successful: zh/guides structure matches guides/")
else:
    if missing_in_zh:
        print(f"Missing in zh/guides: {missing_in_zh}")
    if extra_in_zh:
        print(f"Extra in zh/guides: {extra_in_zh}")
