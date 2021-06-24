# LoggerGenerator

## What is LoggerGenerator?
LoggerGenerator is a class for sharing the same log object with multiple python files.

## Install
You can install using pip.
`pip install .`


## How to use?
```python
from LoggerGenerator import logger_gen

logger_gen(globals())
log.info("...")
```
