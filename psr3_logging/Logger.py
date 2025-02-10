import logging
import json
import datetime

class PSR3Formatter(logging.Formatter):
    def formatTime(self, record, date_fmt = None):
        dt = datetime.datetime.fromtimestamp(record.created, datetime.UTC).replace(microsecond=int(record.msecs * 1000))
        return dt.strftime('%Y-%m-%dT%H:%M:%S.%f+00:00')  # UTC time with microseconds

class LoggingInterface:
    """A PSR-3 compliant logger wrapper around Python's logging module."""
    
    LEVEL_MAP = {
        "emergency": logging.CRITICAL,
        "alert": logging.CRITICAL,
        "critical": logging.CRITICAL,
        "error": logging.ERROR,
        "warning": logging.WARNING,
        "notice": logging.INFO,
        "info": logging.INFO,
        "debug": logging.DEBUG,
    }

    def __init__(self, log_name: str = "logger", filename: str = None):
        self.logger = logging.getLogger(log_name)
        self.logger.setLevel(logging.DEBUG)  # Set to the lowest level to allow all logs

        # Formatter
        formatter = PSR3Formatter(f'[%(asctime)s] {log_name}.%(levelname)s: %(message)s')
        
        # Set handler to file if filename passed
        if filename:
            handler = logging.FileHandler(filename)
        else:
            handler = logging.StreamHandler()
        
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def log(self, level: str, message: str, context: dict = None):
        """Logs a message at the given level with optional context."""
        if level not in self.LEVEL_MAP:
            raise ValueError(f"Invalid log level: {level}")

        log_level = self.LEVEL_MAP[level]
        
        if context:
            message = f"{message} {json.dumps(context)} []"
        else:
            message = f"{message} [] []"
        
        self.logger.log(log_level, message)

    def __getattr__(self, level):
        """Allows calling log levels as methods, e.g., logger.info('message')"""
        if level in self.LEVEL_MAP:
            return lambda message, context=None: self.log(level, message, context)
        raise AttributeError(f"{self.__class__.__name__} has no attribute '{level}'")