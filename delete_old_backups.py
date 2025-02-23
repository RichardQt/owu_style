import os
import time
import logging
from datetime import datetime
from typing import List
from huggingface_hub import HfApi, login
from huggingface_hub.utils import EntryNotFoundError  # 正确导入路径
import logging
from tenacity import retry, stop_after_attempt, wait_fixed

# 日志文件配置
LOG_FILE = "delete_backups.log"  # 日志文件名
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# 初始化日志系统
def setup_logging():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # 清除之前的处理器（避免重复）
    if logger.handlers:
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)

    # 文件处理器（写入日志文件）
    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setFormatter(logging.Formatter(LOG_FORMAT))

    # 控制台处理器（输出到终端）
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
MAX_KEEP = 5
MAX_RETRIES = 3
RETRY_DELAY = 10

@retry(
    stop=stop_after_attempt(MAX_RETRIES),
    wait=wait_fixed(RETRY_DELAY),
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

def delete_old_backups():
    hf_token = os.getenv("HF_TOKEN")
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

    backup_files = sorted([f for f in current_files if f.startswith(FILE_PREFIX)])
    if not backup_files:
        logger.info("🔍 没有可删除的备份文件")
        return

    # 按数量策略删除
    if len(backup_files) > MAX_KEEP:
        files_to_delete = backup_files[:len(backup_files) - MAX_KEEP]
        for file in files_to_delete:
            logger.info(f"🔄 正在处理: {file}")
            safe_delete_file(api, file, current_files)
            time.sleep(1)

if __name__ == "__main__":
    try:
        delete_old_backups()
        logger.info("🎉 备份清理完成")
    except Exception as e:
        logger.error(f"💥 脚本异常终止: {str(e)}")
        exit(1)
