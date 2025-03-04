"""
Centralized logging configuration for the application.
"""
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def get_logger(name):
    """
    Get a logger instance with the specified name.
    
    Args:
        name (str): Name for the logger, typically __name__ of the calling module
        
    Returns:
        logging.Logger: Configured logger instance
    """
    return logging.getLogger(name)
