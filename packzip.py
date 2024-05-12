import os
import shutil
import datetime
import time
import zipfile
from json_read import json_read
from tqdm import tqdm
import logging

def get_directory_size(directory):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(directory):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size

def backup_zip():
    try:
        config = json_read()

        # 源目录
        source_dir = config["backup"]["source_dir"]
        # 目标目录
        target_dir = config["backup"]["target_dir"]
        # 备份文件名
        backup_file = 'backup_{}.zip'.format(datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S'))

        # 创建一个临时目录来存储备份文件
        temp_dir = config["backup"]["temp_dir"]
        os.makedirs(temp_dir, exist_ok=True)

        # 输出源目录大小
        source_size = get_directory_size(source_dir) / (1024**3)  # 将字节转换为GB
        logging.info(f"[PACK]源目录大小: {source_size:.2f} GB")

        start_time = datetime.datetime.now()  # 记录备份开始时间

        # 创建一个压缩文件
        with zipfile.ZipFile(os.path.join(temp_dir, backup_file), 'w') as zipf:
            # 遍历源目录中的所有文件和文件夹
            logging.info("[PACK]正在添加到压缩文件...")
            for root, dirs, files in os.walk(source_dir):
                for file in tqdm(files, desc='[PACK]文件进度'):
                    file_path = os.path.join(root, file)
                    # 将文件添加到压缩文件中
                    zipf.write(file_path, os.path.relpath(file_path, source_dir))
                for dir in tqdm(dirs, desc='[PACK]文件夹进度'):
                    dir_path = os.path.join(root, dir)
                    # 将文件夹添加到压缩文件中
                    zipf.write(dir_path, os.path.relpath(dir_path, source_dir))

        end_time = datetime.datetime.now()  # 记录备份结束时间
        time_taken = end_time - start_time  # 计算备份所花费的时间


        # 确保目标目录存在，如果不存在则创建
        os.makedirs(target_dir, exist_ok=True)

        # 将压缩文件移动到目标目录
        shutil.move(os.path.join(temp_dir, backup_file), os.path.join(target_dir, backup_file))

        # 删除临时目录
        shutil.rmtree(temp_dir)
        time.sleep(3)
        end_file_size=2
        logging.info(f'[PACK]\033[92m备份完成：{format(os.path.join(target_dir, backup_file))}\033[0m')
        # 获取备份文件大小
        end_file_size = os.path.getsize(os.path.join(target_dir, backup_file)) / (1024**3)  # 备份zip文件大小（以GB为单位）
        logging.info(f"[PACK]备份文件大小:\033[93m{end_file_size:.2f}\033[0m GB")
        logging.info(f"[PACK]备份花费时间: {time_taken}")

    except Exception as e:
        logging.info(f"[PACK]\033[91m备份失败: {e}\033[0m")