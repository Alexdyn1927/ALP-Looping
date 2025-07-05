import logging
import os
from typing import Dict, Any, Optional, Union
from enum import Enum, auto

class LogLevel(Enum):
    """Enum representing standard logging levels."""
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL

class LogOutputType(Enum):
    """Enum representing log output types."""
    CONSOLE = auto()
    FILE = auto()
    BOTH = auto()

class LoggingConfig:
    """
    A flexible logging configuration management class.
    
    Allows dynamic control of logging behavior with support for:
    - Setting log levels
    - Configuring output destinations
    - Enabling/disabling logging
    - Customizing log formats
    """
    
    def __init__(
        self, 
        level: Union[LogLevel, int] = LogLevel.INFO, 
        output_type: LogOutputType = LogOutputType.CONSOLE,
        log_file_path: Optional[str] = None
    ):
        """
        Initialize logging configuration.
        
        Args:
            level (LogLevel): Logging level. Defaults to INFO.
            output_type (LogOutputType): Where to output logs. Defaults to CONSOLE.
            log_file_path (Optional[str]): Path for file logging. Required if output_type is FILE or BOTH.
        
        Raises:
            ValueError: If file logging is selected but no file path is provided.
        """
        self._level = level.value if isinstance(level, LogLevel) else level
        self._output_type = output_type
        self._log_file_path = log_file_path
        
        # Validate log file path for file-based logging
        if (output_type in [LogOutputType.FILE, LogOutputType.BOTH]) and not log_file_path:
            raise ValueError("Log file path must be provided for file-based logging.")
        
        # Ensure log directory exists for file logging
        if log_file_path:
            os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
        
        # Configure logging
        self._configure_logging()
    
    def _configure_logging(self):
        """Configure logging based on current settings."""
        # Reset any existing loggers
        logging.getLogger().handlers.clear()
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Root logger setup
        root_logger = logging.getLogger()
        root_logger.setLevel(self._level)
        
        # Console handler
        if self._output_type in [LogOutputType.CONSOLE, LogOutputType.BOTH]:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            root_logger.addHandler(console_handler)
        
        # File handler
        if self._output_type in [LogOutputType.FILE, LogOutputType.BOTH]:
            if not self._log_file_path:
                raise ValueError("Log file path not specified.")
            
            file_handler = logging.FileHandler(self._log_file_path)
            file_handler.setFormatter(formatter)
            root_logger.addHandler(file_handler)
    
    def set_level(self, level: Union[LogLevel, int]):
        """
        Dynamically change the logging level.
        
        Args:
            level (Union[LogLevel, int]): New logging level to set.
        """
        self._level = level.value if isinstance(level, LogLevel) else level
        self._configure_logging()
    
    def get_level(self) -> int:
        """
        Get current logging level.
        
        Returns:
            int: Current logging level.
        """
        return self._level
    
    def get_output_type(self) -> LogOutputType:
        """
        Get current log output type.
        
        Returns:
            LogOutputType: Current log output configuration.
        """
        return self._output_type
    
    @property
    def log_file_path(self) -> Optional[str]:
        """
        Get the current log file path.
        
        Returns:
            Optional[str]: Path to the log file, if configured.
        """
        return self._log_file_path