import os

def get_files(root_dir, exclude_dirs=None, exclude_files=None):
    if exclude_dirs is None:
        exclude_dirs = []
    if exclude_files is None:
        exclude_files = []
    
    file_list = []
    for root, dirs, files in os.walk(root_dir):
        # 排除指定的目录（如 zh 目录本身）
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        
        for file in files:
            # 排除指定的文件（如脚本自身）
            if file in exclude_files:
                continue
            
            # 获取相对于 root_dir 的相对路径
            rel_dir = os.path.relpath(root, root_dir)
            if rel_dir == ".":
                rel_path = file
            else:
                rel_path = os.path.join(rel_dir, file)
            file_list.append(rel_path)
    return set(file_list)

def verify_structure(src_dir, dst_dir):
    print(f"正在验证源目录 '{src_dir}' 与 目标目录 '{dst_dir}' 的一致性...")
    
    if not os.path.exists(src_dir):
        print(f"错误: 源目录 '{src_dir}' 不存在。")
        return False
    
    # 获取源文件列表，排除 zh 目录和脚本自身
    src_files = get_files(src_dir, exclude_dirs=[dst_dir], exclude_files=["verify_translation.py"])
    
    if not os.path.exists(dst_dir):
        print(f"警告: 目标目录 '{dst_dir}' 不存在。")
        dst_files = set()
    else:
        dst_files = get_files(dst_dir)

    missing_files = src_files - dst_files
    extra_files = dst_files - src_files

    if not missing_files and not extra_files:
        print("\n✅ 成功: 目录结构完全一致，没有缺失文件。")
        return True
    else:
        if missing_files:
            print(f"\n❌ 失败: 'zh/' 目录中缺失以下文件 ({len(missing_files)} 个):")
            for f in sorted(missing_files):
                print(f"  - {f}")
        
        if extra_files:
            print(f"\n⚠️ 提示: 'zh/' 目录中存在额外的文件 ({len(extra_files)} 个):")
            for f in sorted(extra_files):
                print(f"  - {f}")
        
        return False

if __name__ == "__main__":
    # 检查当前目录下所有内容是否已同步到 zh/
    verify_structure(".", "zh")