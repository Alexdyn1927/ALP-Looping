import logging
import time
from typing import Any, Dict, Optional

class ALPLogger:
    """
    Specialized logger for Adaptive Learning Process (ALP) iterations.
    Provides comprehensive logging capabilities with performance tracking.
    """
    def __init__(self, name: str = "ALP", log_level: int = logging.INFO):
        """
        Initialize the ALP logger with configurable name and log level.
        
        :param name: Name of the logger instance
        :param log_level: Logging level (default: logging.INFO)
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(log_level)
        
        # Create console handler if not already configured
        if not self.logger.handlers:
            console_handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)
    
    def log_iteration(
        self, 
        iteration: int, 
        metrics: Optional[Dict[str, Any]] = None, 
        level: int = logging.INFO
    ) -> None:
        """
        Log details of a single iteration with performance metrics.
        
        :param iteration: Current iteration number
        :param metrics: Dictionary of performance metrics
        :param level: Logging level
        """
        metrics = metrics or {}
        log_message = f"Iteration {iteration}"
        
        # Add metrics to log message
        if metrics:
            metric_str = " | ".join(f"{k}: {v}" for k, v in metrics.items())
            log_message += f" - Metrics: {metric_str}"
        
        # Log the message at specified level
        self.logger.log(level, log_message)
    
    def log_error(
        self, 
        iteration: int, 
        error: Exception, 
        context: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Log an error that occurred during an iteration.
        
        :param iteration: Iteration number when error occurred
        :param error: Exception that was raised
        :param context: Additional context about the error
        """
        context = context or {}
        error_message = (
            f"Error in iteration {iteration}: {str(error)}\n"
            f"Context: {context}"
        )
        self.logger.error(error_message, exc_info=True)
    
    def track_performance(
        self, 
        start_time: float, 
        end_time: float
    ) -> Dict[str, float]:
        """
        Calculate and log performance metrics for an iteration.
        
        :param start_time: Start time of the iteration
        :param end_time: End time of the iteration
        :return: Performance metrics dictionary
        """
        elapsed_time = end_time - start_time
        performance_metrics = {
            "elapsed_time": elapsed_time,
            "timestamp": end_time
        }
        
        # Log performance metrics
        self.log_iteration(
            iteration=0,  # Use 0 for overall performance tracking
            metrics=performance_metrics,
            level=logging.DEBUG
        )
        
        return performance_metrics