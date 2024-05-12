from json_read import *
import time
import logging
from packzip import *

#初始化logging
logging.basicConfig(
    level=logging.NOTSET,
    format='%(asctime)s %(levelname)s %(message)s',

)
logging.info("============= Server Backup =============")
logging.info("读取配置文件...")
try:
    config = json_read()
    logging.info("读取完成!")
    logging.info(f'备份时间:{config["time"]["hour"]}:{config["time"]["minute"]}:{config["time"]["second"]}')
    logging.info(f"源目录:{config['backup']['source_dir']}")
    logging.info(f"备份目录:{config['backup']['target_dir']}")
except Exception as e:
    logging.info(f"\033[91m读取配置文件失败: {e}\033[0m")

while True:
    current_time = time.localtime()

    if (current_time.tm_hour == config["time"]["hour"] and
            current_time.tm_min == config["time"]["minute"] and
            current_time.tm_sec == config["time"]["second"]):
        logging.info("\033[92m备份时间到!触发备份...\033[0m")
        backup_zip()
        time.sleep(1)  # 防止在同一秒内多次输出