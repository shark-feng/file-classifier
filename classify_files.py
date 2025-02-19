import os
import shutil
import logging
from collections import defaultdict
import json
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm


# 加载配置文件
def load_config(config_path='config.json'):
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logging.error(f'加载配置文件失败: {str(e)}')
        return None


# 生成不重复的文件路径
def get_unique_path(target_dir, filename):
    base_name, ext = os.path.splitext(filename)
    counter = 1
    new_name = filename
    while os.path.exists(os.path.join(target_dir, new_name)):
        new_name = f'{base_name}_{counter}{ext}'
        counter += 1
    return os.path.join(target_dir, new_name)


# 检查是否为受保护项
def is_protected(item, protected_items):
    return item in protected_items or item.startswith('.')


def classify_files(directory, move_folders=True):
    current_dir = directory
    script_name = os.path.basename(__file__)

    # 加载配置文件
    config = load_config()
    if not config:
        logging.error('由于配置文件错误，程序退出。')
        return

    file_categories = config.get('categories', {})
    protected_items = set(config.get('protected_items', {}))
    script_extensions = tuple(config.get('script_extensions', []))

    # 构建扩展名映射字典
    extension_map = defaultdict(lambda: '其他')
    for category, extensions in file_categories.items():
        for ext in extensions:
            extension_map[ext.lower()] = category

    # 需要创建的目标目录（自动包含其他类别）
    target_dirs = set(file_categories.keys()) | {'其他', '文件夹'}

    # 预创建目录
    for dir_name in target_dirs:
        dir_path = os.path.join(current_dir, dir_name)
        if not os.path.exists(dir_path):
            try:
                os.makedirs(dir_path, exist_ok=True)
                logging.info(f'已创建目录: {dir_name}/')
            except Exception as e:
                logging.error(f'无法创建目录 {dir_name}: {str(e)}')

    # 多线程处理
    def process_item(item):
        item_path = os.path.join(current_dir, item)

        # 跳过条件判断
        if item == script_name or item in target_dirs or is_protected(item, protected_items):
            return 0

        try:
            # 处理文件夹
            if os.path.isdir(item_path):
                if move_folders:
                    target_dir = os.path.join(current_dir, '文件夹')
                    dest_path = get_unique_path(target_dir, item)
                    shutil.move(item_path, dest_path)
                    logging.info(f'移动文件夹: {item} -> 文件夹/')
                    return 1
                else:
                    logging.info(f'跳过文件夹（未移动）: {item}')
                    return 0

            # 处理文件
            _, ext = os.path.splitext(item)
            ext = ext.lower()

            # 跳过脚本文件
            if ext in script_extensions:
                logging.info(f'跳过脚本文件: {item}')
                return 0

            # 确定分类
            category = extension_map[ext]
            target_dir = os.path.join(current_dir, category)

            # 执行移动（带冲突解决）
            dest_path = get_unique_path(target_dir, item)
            shutil.move(item_path, dest_path)
            logging.info(f'移动文件: {item} -> {category}/')
            return 1
        except PermissionError as e:
            logging.error(f'权限不足: {item} ({str(e)})')
        except Exception as e:
            logging.error(f'处理 {item} 时出错: {str(e)}')
        return 0

    # 获取所有项目并显示进度条
    items = os.listdir(current_dir)
    processed = 0
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(tqdm(executor.map(process_item, items), total=len(items), desc='正在处理', unit='项'))
    processed = sum(results)
    logging.info(f'处理完成。共移动了 {processed} 项。')


if __name__ == '__main__':
    # 配置日志
    log_file = 'classify_files.log'
    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s] %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )

    # 用户输入目标目录
    print('欢迎使用文件分类工具！')
    target_directory = input('请输入目标目录路径（留空则使用当前目录）：').strip()
    if not target_directory:
        target_directory = os.getcwd()
    elif not os.path.exists(target_directory):
        logging.error(f'指定的目录不存在: {target_directory}')
        exit(1)

    # 切换到目标目录
    os.chdir(target_directory)
    logging.info(f'目标目录已设置为: {target_directory}')

    # 是否移动文件夹
    move_folders_input = input('是否需要移动文件夹？(y/n，默认: y): ').strip().lower()
    move_folders = True if move_folders_input in ('y', '') else False

    # 运行分类逻辑
    classify_files(target_directory, move_folders=move_folders)

    # 等待用户输入后再退出
    input('按 Enter 键退出...')
