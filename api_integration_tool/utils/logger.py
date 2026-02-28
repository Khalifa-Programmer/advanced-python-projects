import logging

def setup_logging():
    logging.basicConfig(
        filename="logs/api.log",
        level=logging.ERROR
    )
