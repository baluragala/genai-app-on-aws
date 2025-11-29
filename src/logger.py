"""Logging configuration for RAG application."""
import logging
import sys
from pathlib import Path
from typing import Optional

import colorlog

from src.config import Config


class Logger:
    """Custom logger with color support and file output."""
    
    _loggers = {}
    
    @classmethod
    def get_logger(cls, name: str, log_file: Optional[str] = None) -> logging.Logger:
        """
        Get or create a logger instance.
        
        Args:
            name: Logger name
            log_file: Optional log file path
            
        Returns:
            Configured logger instance
        """
        if name in cls._loggers:
            return cls._loggers[name]
        
        logger = logging.getLogger(name)
        logger.setLevel(getattr(logging, Config.LOG_LEVEL))
        
        # Prevent duplicate handlers
        if logger.handlers:
            return logger
        
        # Console handler with colors
        console_handler = colorlog.StreamHandler(sys.stdout)
        console_handler.setLevel(getattr(logging, Config.LOG_LEVEL))
        
        console_format = colorlog.ColoredFormatter(
            "%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white',
            }
        )
        console_handler.setFormatter(console_format)
        logger.addHandler(console_handler)
        
        # File handler
        if log_file:
            log_path = Config.LOGS_DIR / log_file
        else:
            log_path = Config.LOGS_DIR / f"{name}.log"
        
        file_handler = logging.FileHandler(log_path)
        file_handler.setLevel(getattr(logging, Config.LOG_LEVEL))
        
        file_format = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        file_handler.setFormatter(file_format)
        logger.addHandler(file_handler)
        
        cls._loggers[name] = logger
        return logger


# Create default logger
logger = Logger.get_logger("rag_app", "application.log")

