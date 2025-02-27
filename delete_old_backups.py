import os
import time
import logging
from datetime import datetime, timedelta
from typing import List
from huggingface_hub import HfApi, login
from huggingface_hub.utils import EntryNotFoundError
from tenacity import (
    retry,
    stop_after_attempt,
    wait_fixed,
    retry_if_exception_type
)

# 日志配置
# 日志配置
REPO_ROOT = os.getenv("GITHUB_WORKSPACE", os.getcwd())  # 关键修改点
LOG_FILE = os.path.join(REPO_ROOT, "delete_backups.log")  # 强制写入根目录
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

def setup_logging():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    if logger.handlers:
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)

    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setFormatter(logging.Formatter(LOG_FORMAT))
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(LOG_FORMAT))

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger

logger = setup_logging()

# 常量配置
REPO_ID = "Richardlsr/owu_db"
REPO_TYPE = "dataset"
FILE_PREFIX = "webui_backup_"
TIME_FORMAT = "%Y%m%d_%H%M%S"  # 文件名中的时间戳格式
MAX_HOURS = 12                 # 保留24小时内的备份

@retry(
    stop=stop_after_attempt(3),
    wait=wait_fixed(10),
    retry=retry_if_exception_type(EntryNotFoundError),
    before_sleep=lambda _: logger.warning("文件删除失败，准备重试...")
)
def safe_delete_file(api: HfApi, file: str, current_files: List[str]):
    """安全删除文件（带存在性检查）"""
    if file not in current_files:
        logger.warning(f"跳过不存在的文件: {file}")
        return

    try:
        api.delete_file(
            path_in_repo=file,
            repo_id=REPO_ID,
            repo_type=REPO_TYPE,
            commit_message=f"自动删除旧备份: {file}"
        )
        logger.info(f"✅ 成功删除: {file}")
    except EntryNotFoundError as e:
        logger.error(f"❌ 永久删除失败: {file} ({str(e)})")
        raise

def parse_file_time(filename: str) -> datetime:
    """从文件名解析时间戳"""
    time_str = filename[len(FILE_PREFIX):].replace(".db", "")
    return datetime.strptime(time_str, TIME_FORMAT)

def delete_old_backups():
    hf_token = "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"
    if not hf_token:
        logger.critical("❌ 未设置 HF_TOKEN！")
        raise ValueError("HF_TOKEN 未配置")

    login(token=hf_token)
    api = HfApi()

    try:
        current_files = api.list_repo_files(repo_id=REPO_ID, repo_type=REPO_TYPE)
    except Exception as e:
        logger.error(f"获取文件列表失败: {str(e)}")
        raise

    # 获取当前时间（UTC）
    now = datetime.utcnow()
    threshold = now - timedelta(hours=MAX_HOURS)

    # 处理备份文件
    deleted_count = 0
    for file in current_files:
        if not file.startswith(FILE_PREFIX):
            continue

        try:
            file_time = parse_file_time(file)
        except ValueError:
            logger.warning(f"⚠️ 忽略无效文件名: {file}")
            continue

        if file_time < threshold:
            logger.info(f"🔄 准备删除过期备份: {file} (创建于 {file_time})")
            safe_delete_file(api, file, current_files)
            deleted_count += 1
            time.sleep(1)  # API速率限制

    logger.info(f"🎉 清理完成，共删除 {deleted_count} 个过期备份")

if __name__ == "__main__":
    try:
        delete_old_backups()
    except Exception as e:
        logger.error(f"💥 脚本异常终止: {str(e)}")
        exit(1)
