import logging

def setup_logger():
    # Create a logger
    logger = logging.getLogger('my_logger')
    logger.setLevel(logging.INFO)  # Set the logging level

    # Create a console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Define a format string that includes the module name
    formatter = logging.Formatter('%(asctime)s - %(module)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(console_handler)

    return logger   
