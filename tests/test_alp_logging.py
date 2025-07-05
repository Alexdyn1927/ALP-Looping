import logging
import time
import pytest
from src.alp.logging import ALPLogger

def test_alp_logger_initialization():
    """Test logger initialization with default and custom parameters."""
    logger = ALPLogger()
    assert logger.logger.name == "ALP"
    assert logger.logger.level == logging.INFO

    custom_logger = ALPLogger(name="CustomALP", log_level=logging.DEBUG)
    assert custom_logger.logger.name == "CustomALP"
    assert custom_logger.logger.level == logging.DEBUG

def test_log_iteration(caplog):
    """Test logging of iteration with metrics."""
    logger = ALPLogger()
    caplog.set_level(logging.INFO)

    metrics = {"loss": 0.5, "accuracy": 0.95}
    logger.log_iteration(iteration=10, metrics=metrics)

    assert "Iteration 10" in caplog.text
    assert "loss: 0.5" in caplog.text
    assert "accuracy: 0.95" in caplog.text

def test_log_error(caplog):
    """Test error logging with context."""
    logger = ALPLogger()
    caplog.set_level(logging.ERROR)

    try:
        raise ValueError("Test error")
    except ValueError as e:
        logger.log_error(iteration=5, error=e, context={"model": "test_model"})

    assert "Error in iteration 5" in caplog.text
    assert "Test error" in caplog.text
    assert "model: test_model" in caplog.text

def test_track_performance():
    """Test performance tracking method."""
    logger = ALPLogger()
    
    start_time = time.time() - 1.0  # Simulate 1 second elapsed
    end_time = time.time()

    performance = logger.track_performance(start_time, end_time)

    assert "elapsed_time" in performance
    assert "timestamp" in performance
    assert performance["elapsed_time"] >= 1.0