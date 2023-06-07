import logging


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)

    c_handler = logging.StreamHandler()
    f_handler = logging.FileHandler(f"{name}.monitor.log")

    cf_format = logging.Formatter('%(process)d - %(asctime)s - %(levelname)s - %(message)s')

    c_handler.setFormatter(cf_format)
    f_handler.setFormatter(cf_format)

    f_handler.setLevel(logging.INFO)

    logger.addHandler(c_handler)
    logger.addHandler(f_handler)

    logger.setLevel(logging.INFO)

    return logger
