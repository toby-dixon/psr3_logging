# PSR3 Logging

A python implementation of a psr3 compliant logging interface.

## Basic Usage

```python
from psr3_logging import LoggingInterface

logger = LoggingInterface(log_name="testLog", filename="./logs.log")
logger.debug("This is a debug log", {"data": "this is some context information"})
```

**_./logs.log:_**

```
[2025-02-10T10:37:11.116000+00:00] testLog.DEBUG: This is a debug log {"data": "this is some context data"} []
```
