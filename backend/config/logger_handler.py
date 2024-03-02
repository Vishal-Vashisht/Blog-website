import logging

logger = logging.getLogger()
# Set parent's level to INFO and assign a new handler
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s:%(name)s:%(levelname)s:%(message)s"))
logger.setLevel(logging.INFO)
logger.addHandler(handler)
