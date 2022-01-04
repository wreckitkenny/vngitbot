[![Python 3.6](https://img.shields.io/badge/Python3-%3E%3D3.6-blue)](https://www.python.org/downloads)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-v1.2x-blue)](https://kubernetes.io/)

# VNGitbot
VNGitbot is a Python bot supporting SRE to change Image version tag after developers commit a new code version.

#
```bash
.
|-- Dockerfile
|-- README.md
|-- config
|   `-- vngitbot.conf
|-- docs
|   `-- CHANGELOG.md
|-- requirements.txt
`-- vngitbot
    |-- _common
    |   |-- __init__.py
    |   |-- common.py
    |   |-- config.py
    |   `-- version.py
    |-- _features
    |   |-- __init__.py
    |   |-- cacheManualMR.py
    |   |-- changeImageTag.py
    |   |-- checkApproval.py
    |   |-- makeMerge.py
    |   `-- revokeApproval.py
    |-- _requests
    |   |-- __init__.py
    |   `-- handle.py
    |-- _slack
    |   |-- __init__.py
    |   `-- slack.py
    |-- _telegram
    |   |-- __init__.py
    |   `-- telegram.py
    `-- launch.py
```
#
## Requirements
```bash
python3==3.6 or newer
python-gitlab==2.9.0 or newer
slack_sdk==3.11.2 or newer
pyyaml==5.4.1 or newer
```
#
## Installation
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install requirements.
```bash
pip3 install -r requirements.txt
```
#
## Usage
```python
GITBOT_CONFIG_PATH=/path/to/vngitbot.conf
python3 /path/to/vngitbot/launch.py
```
#
## Docker/Docker Compose
```bash
version: '3.7'
services:
  gitbot-test:
    image: registry.example.com/library/vngitbot:latest
    container_name: vngitbot
    volumes:
            - ./vngitbot.conf:/opt/vngitbot/config/vngitbot.conf:ro
    ports:
      - 8000:8000
    restart: on-failure
```
#
## License
[MIT](https://choosealicense.com/licenses/mit/)