import os
import shutil
import datetime
import time
import zipfile
from json_read import json_read
import logging


def get_directory_size(directory):
    total_size = 0
    if not os.path.exists(directory):
        return total_size

    for dirpath, dirnames, filenames in os.walk(directory):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            file_size_in_bytes = os.path.getsize(fp)
            total_size += file_size_in_bytes / (1024 ** 2)  # 转换为MB
    return total_size


def backup_zip():
    try:
        config = json_read()

        source_dir = config["backup"]["source_dir"]
        target_dir = config["backup"]["target_dir"]
        backup_file = 'backup_{}.zip'.format(datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S'))

        temp_dir = config["backup"]["temp_dir"]
        os.makedirs(temp_dir, exist_ok=True)

        source_size = get_directory_size(source_dir)

        start_time = datetime.datetime.now()

        file_count = sum([len(files) for _, _, files in os.walk(source_dir)])
        processed_size = 0
        last_progress = -1

        with zipfile.ZipFile(os.path.join(temp_dir, backup_file), 'w') as zipf:
            logging.info("[PACK]正在添加到压缩文件...")
            for root, _, files in os.walk(source_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, os.path.relpath(file_path, source_dir))
                    processed_size += os.path.getsize(file_path)
                    progress = min(int((processed_size / (source_size * 1024)) * 100), 100)  # 防止进度大于100%

                    if progress != last_progress:
                        logging.info(f"[PACK]备份进度: {progress}%")
                        last_progress = progress

        end_time = datetime.datetime.now()
        time_taken = end_time - start_time

        os.makedirs(target_dir, exist_ok=True)

        shutil.move(os.path.join(temp_dir, backup_file), os.path.join(target_dir, backup_file))

        shutil.rmtree(temp_dir)
        time.sleep(3)

        logging.info(f'[PACK]\033[92m备份完成：{format(os.path.join(target_dir, backup_file))}\033[0m')
        end_file_size = os.path.getsize(os.path.join(target_dir, backup_file)) / (1024 ** 2)
        logging.info(f"[PACK]备份文件大小:\033[93m{end_file_size:.2f}\033[0m MB")
        logging.info(f"[PACK]备份花费时间: {time_taken}")

    except Exception as e:
        logging.info(f"[PACK]\033[91m备份失败: {e}\033[0m")