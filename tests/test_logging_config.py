import os
import pytest
import logging
from typing import List

from src.logging import LoggingConfig, LogLevel, LogOutputType

def test_default_logging_configuration():
    """Test default logging configuration."""
    config = LoggingConfig()
    assert config.get_level() == logging.INFO
    assert config.get_output_type() == LogOutputType.CONSOLE
    assert config.log_file_path is None

def test_logging_level_configuration():
    """Test setting different logging levels."""
    config = LoggingConfig(level=LogLevel.DEBUG)
    assert config.get_level() == logging.DEBUG
    
    config.set_level(LogLevel.ERROR)
    assert config.get_level() == logging.ERROR

def test_file_logging_configuration(tmp_path):
    """Test file logging configuration."""
    log_file = os.path.join(tmp_path, 'test.log')
    
    config = LoggingConfig(
        level=LogLevel.INFO, 
        output_type=LogOutputType.FILE, 
        log_file_path=log_file
    )
    
    assert config.get_output_type() == LogOutputType.FILE
    assert config.log_file_path == log_file
    assert os.path.exists(os.path.dirname(log_file))

def test_invalid_file_logging_configuration():
    """Test that an error is raised when file logging is misconfigured."""
    with pytest.raises(ValueError):
        LoggingConfig(output_type=LogOutputType.FILE)

def test_logging_output_types(tmp_path):
    """Test different logging output configurations."""
    log_file = os.path.join(tmp_path, 'combined.log')
    
    # Test BOTH output type
    config = LoggingConfig(
        level=LogLevel.WARNING, 
        output_type=LogOutputType.BOTH, 
        log_file_path=log_file
    )
    
    assert config.get_output_type() == LogOutputType.BOTH
    assert config.log_file_path == log_file

def test_log_creation(tmp_path, caplog):
    """Test that logs are actually created."""
    log_file = os.path.join(tmp_path, 'activity.log')
    
    config = LoggingConfig(
        level=LogLevel.INFO, 
        output_type=LogOutputType.FILE, 
        log_file_path=log_file
    )
    
    # Log some messages
    logging.info("Test log message")
    logging.error("Error log message")
    
    # Check file logging
    assert os.path.exists(log_file)
    with open(log_file, 'r') as f:
        log_contents = f.read()
        assert "Test log message" in log_contents
        assert "Error log message" in log_contents