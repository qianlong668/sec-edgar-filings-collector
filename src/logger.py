import logging

from config import LOG_DIR, LOG_FILE


def setup_logger() -> logging.Logger:
    """
    创建并返回一个同时输出到控制台和文件的 logger。
    """
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger("sec_edgar_logger")
    logger.setLevel(logging.INFO)

    # 防止重复添加 handler
    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # 文件日志
    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    # 控制台日志
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger