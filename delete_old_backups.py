import os
import time
from datetime import datetime
from huggingface_hub import HfApi, login
import logging

# 配置日志
# 配置日志同时输出到控制台和文件
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("delete_backups.log"),  # 输出到文件
        logging.StreamHandler()                     # 输出到控制台
    ]
)
logger = logging.getLogger(__name__)

# 常量配置（根据你的需求修改）
REPO_ID = "Richardlsr/owu_db"        # 数据集仓库ID
REPO_TYPE = "dataset"                # 仓库类型为数据集
FILE_PREFIX = "webui_backup_"        # 备份文件前缀
MAX_KEEP = 5                         # 最大保留数量（按数量删除）
MAX_HOURS = 24                       # 最大保留小时数（按时间删除）

def delete_old_backups():
    # 从环境变量获取HF Token
    hf_token = "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"
    if not hf_token:
        raise ValueError("HF_TOKEN 未设置！请检查GitHub Secrets或环境变量")

    # 登录Hugging Face
    login(token=hf_token)
    api = HfApi()

    # 获取仓库文件列表（关键修复：指定repo_type为dataset）
    try:
        files = api.list_repo_files(repo_id=REPO_ID, repo_type=REPO_TYPE)
    except Exception as e:
        logger.error(f"获取仓库文件失败: {str(e)}")
        raise

    # 筛选备份文件
    backup_files = [f for f in files if f.startswith(FILE_PREFIX)]
    if not backup_files:
        logger.info("没有找到可删除的备份文件")
        return

    # 按时间排序（旧文件在前）
    backup_files.sort()

    # 按数量删除策略
    if len(backup_files) > MAX_KEEP:
        files_to_delete = backup_files[:len(backup_files) - MAX_KEEP]
        for file in files_to_delete:
            logger.info(f"删除旧备份（数量策略）: {file}")
            api.delete_file(
                path_in_repo=file,
                repo_id=REPO_ID,
                repo_type=REPO_TYPE,
                commit_message=f"自动删除旧备份: {file}"
            )

    # 按时间删除策略（可选）
    # current_time = datetime.now()
    # for file in backup_files:
    #     file_time = datetime.strptime(file, f"{FILE_PREFIX}%Y%m%d_%H%M%S.db")
    #     if (current_time - file_time).total_seconds() > MAX_HOURS * 3600:
    #         logger.info(f"删除旧备份（时间策略）: {file}")
    #         api.delete_file(...)

if __name__ == "__main__":
    try:
        delete_old_backups()
        logger.info("备份清理完成")
    except Exception as e:
        logger.error(f"脚本运行失败: {str(e)}")
        exit(1)
