import logging
import sys

if __name__ == "__main__":
    # example config for logging
    logger = logging.getLogger("quant_frame")

    handler = logging.StreamHandler(sys.stdout)

    formatter = logging.Formatter("%(asctime)s - %(module)s - %(levelname)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

