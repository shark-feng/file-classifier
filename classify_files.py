import os
import shutil
import logging
from collections import defaultdict
import json
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

# -------------------- 工具函数 --------------------
def load_config(config_path="config.json"):
    """加载配置文件"""
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
        return config
    except Exception as e:
        logging.error(f"诶呀~加载配置文件失败了呢: {str(e)}")
        return None

def get_unique_path(target_dir, filename):
    """生成不重复的文件路径"""
    base_name, ext = os.path.splitext(filename)
    counter = 1
    new_name = filename
    while os.path.exists(os.path.join(target_dir, new_name)):
        new_name = f"{base_name}_{counter}{ext}"
        counter += 1
    return os.path.join(target_dir, new_name)

def is_protected(item, protected_items):
    """检查是否为受保护项"""
    return item in protected_items or item.startswith('.')

# -------------------- 主逻辑 --------------------
def classify_files(directory, move_folders=True):
    """主分类逻辑"""
    current_dir = directory
    script_name = os.path.basename(__file__)
    
    # 加载配置文件
    config = load_config()
    if not config:
        logging.error("呜呜~配置文件好像出问题了呢，我要走了~")
        return
    
    FILE_CATEGORIES = config.get("categories", {})
    PROTECTED_ITEMS = set(config.get("protected_items", {}))
    SCRIPT_EXTENSIONS = tuple(config.get("script_extensions", []))
    
    # 构建扩展名映射字典
    EXTENSION_MAP = defaultdict(lambda: OTHER_CATEGORY)
    for category, extensions in FILE_CATEGORIES.items():
        for ext in extensions:
            EXTENSION_MAP[ext.lower()] = category
    
    # 需要创建的目标目录（自动包含其他类别）
    target_dirs = set(FILE_CATEGORIES.keys()) | {OTHER_CATEGORY, DEFAULT_FOLDER_CATEGORY}
    
    # 预创建目录
    for dir_name in target_dirs:
        dir_path = os.path.join(current_dir, dir_name)
        if not os.path.exists(dir_path):
            try:
                os.makedirs(dir_path, exist_ok=True)
                logging.info(f"成功创建了目录: {dir_name}/ ~")
            except Exception as e:
                logging.error(f"诶？好像无法创建目录 {dir_name} 呢~ 错误信息: {str(e)}")
    
    # 多线程处理
    def process_item(item):
        item_path = os.path.join(current_dir, item)
        
        # 跳过条件判断
        if item == script_name or item in target_dirs or is_protected(item, PROTECTED_ITEMS):
            return 0
        
        try:
            # 处理文件夹
            if os.path.isdir(item_path):
                if move_folders:
                    target_dir = os.path.join(current_dir, DEFAULT_FOLDER_CATEGORY)
                    dest_path = get_unique_path(target_dir, item)
                    shutil.move(item_path, dest_path)
                    logging.info(f"把文件夹 {item} 移动到 {DEFAULT_FOLDER_CATEGORY}/ 啦~")
                    return 1
                else:
                    logging.info(f"跳过了文件夹 {item}（没有移动哦~）")
                    return 0
            
            # 处理文件
            _, ext = os.path.splitext(item)
            ext = ext.lower()  # 统一小写处理
            
            # 跳过脚本文件
            if ext in SCRIPT_EXTENSIONS:
                logging.info(f"发现了一个脚本文件 {item}，帮你跳过啦~")
                return 0
            
            # 确定分类
            category = EXTENSION_MAP[ext]
            target_dir = os.path.join(current_dir, category)
            
            # 执行移动（带冲突解决）
            dest_path = get_unique_path(target_dir, item)
            shutil.move(item_path, dest_path)
            logging.info(f"把文件 {item} 移动到 {category}/ 啦~")
            return 1
        except PermissionError as e:
            logging.error(f"咦~你权限呢?我问你权限呢?不然怎么会无法处理 {item} 呢~ 错误信息: {str(e)}")
        except Exception as e:
            logging.error(f"唔...处理 {item} 的时候出错啦~ 错误信息: {str(e)}")
        return 0

    # 获取所有项目并显示进度条
    items = os.listdir(current_dir)
    processed = 0
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(tqdm(executor.map(process_item, items), total=len(items), desc="正在努力分类中~", unit="项"))
    processed = sum(results)
    logging.info(f"分类完成啦~ 共计移动了 {processed} 项~")

# -------------------- 初始化 --------------------
if __name__ == "__main__":
    # 配置日志
    log_file = "classify_files.log"
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler()
        ]
    )
    
    # 默认配置
    OTHER_CATEGORY = "其他"
    DEFAULT_FOLDER_CATEGORY = "文件夹"
    
    # 用户输入目标目录
    print("欢迎使用文件分类工具~ (｡･ω･｡)ﾉ")
    target_directory = input("请输入目标目录路径（留空则使用当前目录哦~）：").strip()
    if not target_directory:
        target_directory = os.getcwd()
    elif not os.path.exists(target_directory):
        logging.error(f"诶？你说的目录好像不存在呢~ 路径: {target_directory}")
        exit(1)
    
    # 切换到目标目录
    os.chdir(target_directory)
    logging.info(f"目标目录已设置为: {target_directory} 呐~")
    
    # 是否移动文件夹
    move_folders_input = input("需要移动文件夹吗？(y/n，默认: y)：").strip().lower()
    move_folders = True if move_folders_input in ("y", "") else False
    
    # 运行分类逻辑
    classify_files(target_directory, move_folders=move_folders)
    
    # 等待用户输入后再退出
    input("分类完成啦~ 按 Enter 键退出吧~ (｡･ω･｡)ﾉ")