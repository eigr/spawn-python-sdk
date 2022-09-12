# Spawn Python SDK

Python User Language Support for [Spawn](https://github.com/eigr/spawn).

## Installation via source

```
> git clone https://github.com/eigr-labs/spawn-python-sdk.git
Cloning into 'spawn-python-sdk'...

> cd spawn-python-sdk
> python3 -m venv env 
> source ./env/bin/activate
> python --version     
Python 3.7.3
> pip --version 
> pip install wheel
> pip install .
```

### Generate installer
```
python setup.py bdist_wheel
```

### Local install
```
python -m pip install dist/spawn-python-sdk-0.1.0-py3-none-any.whl
```