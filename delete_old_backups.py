from huggingface_hub import HfApi, login
import os
import re
import logging
from datetime import datetime, timedelta
import pytz
from tenacity import retry, stop_after_attempt, wait_exponential

# 配置参数
HF_TOKEN = "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"
REPO_ID = "Richardlsr/owu_db"
BACKUP_PREFIX = "webui_backup"
RETENTION_MODE = "count"  # 或 "time"
MAX_KEEP = 10
MAX_HOURS = 24
TIMEZONE = "Asia/Shanghai"  # 设置你的时区

# 日志配置
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("delete_backups.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def extract_timestamp(filename):
    """从文件名提取时间戳（带时区）"""
    match = re.search(rf"{BACKUP_PREFIX}_(\d{{8}}_\d{{6}})\.db", filename)
    if match:
        naive_time = datetime.strptime(match.group(1), "%Y%m%d_%H%M%S")
        return pytz.timezone(TIMEZONE).localize(naive_time)
    return None

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10),
    before=lambda _: logger.warning("删除失败，正在重试...")
)
def delete_file_with_retry(api, file):
    """带重试机制的删除操作"""
    api.delete_file(
        path_in_repo=file,
        repo_id=REPO_ID,
        commit_message=f"Auto delete old backup: {file}"
    )

def main():
    # 登录 Hugging Face
    login(token=HF_TOKEN)
    api = HfApi()

    # 获取仓库中所有备份文件
    logger.info("开始获取仓库文件列表...")
    files = api.list_repo_files(REPO_ID)
    backups = []
    for file in files:
        timestamp = extract_timestamp(file)
        if timestamp:
            backups.append((timestamp, file))
    logger.info(f"找到 {len(backups)} 个备份文件")

    # 按时间倒序排序
    backups.sort(reverse=True, key=lambda x: x[0])

    # 计算保留截止时间（带时区）
    now = datetime.now(pytz.timezone(TIMEZONE))
    if RETENTION_MODE == "time":
        cutoff_time = now - timedelta(hours=MAX_HOURS)
        logger.info(f"保留截止时间: {cutoff_time.strftime('%Y-%m-%d %H:%M:%S %Z')}")

    # 确定需要删除的文件
    to_delete = []
    if RETENTION_MODE == "count":
        to_delete = backups[MAX_KEEP:]
    elif RETENTION_MODE == "time":
        to_delete = [b for b in backups if b[0] < cutoff_time]

    # 执行删除
    if not to_delete:
        logger.info("无需删除旧备份")
        return

    logger.info(f"准备删除 {len(to_delete)} 个旧备份")
    for timestamp, file in to_delete:
        try:
            logger.info(f"正在删除: {file} (创建于 {timestamp.strftime('%Y-%m-%d %H:%M:%S %Z')})")
            delete_file_with_retry(api, file)
        except Exception as e:
            logger.error(f"删除失败: {file} - {str(e)}")

if __name__ == "__main__":
    main()
