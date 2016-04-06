Evtx Info Extractor
--------------------
by @j84255801912

## Dependency
```
$ pip install python-evtx
```

## Usage example

Use it as a module
```python
from parse import parse_evtx

parse_evtx('Test.evtx', [4624, 4625])
```

Use it as a script
```bsh
$ python parse.py Test.evtx 4624 4625
```

## TODO
* Support more informations.
