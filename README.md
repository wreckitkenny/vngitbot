[![Python 3.6](https://img.shields.io/badge/Python3-%3E%3D3.6-blue)](https://www.python.org/downloads)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-v1.2x-blue)](https://kubernetes.io/)

# VNGitbot
VNGitbot is a Python bot supporting SRE to change Image version tag after developers commit a new code version.

#
```bash
vngitbot/
├── config
│   └── vngitbot.conf
├── Dockerfile
├── docs
│   └── CHANGELOG.md
├── README.md
├── requirements.txt
└── vngitbot
    ├── approve
    │   ├── checkApproval.py
    │   ├── __init__.py
    │   └── revokeApproval.py
    ├── changeTag
    │   ├── changeImageTag.py
    │   └── __init__.py
    ├── handleRequest
    │   ├── handle.py
    │   └── __init__.py
    ├── launch.py
    ├── merge
    │   ├── cacheManualMR.py
    │   ├── __init__.py
    │   └── makeMerge.py
    ├── slack
    │   ├── __init__.py
    │   └── slack.py
    ├── telegram
    │   ├── __init__.py
    │   └── telegram.py
    ├── utils
    │   ├── approve.py
    │   ├── change.py
    │   ├── config.py
    │   ├── deployCheck.py
    │   ├── __init__.py
    │   ├── merge.py
    │   ├── notify.py
    │   └── version.py
    └── verify
        ├── checkDeploy.py
        └── __init__.py

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
