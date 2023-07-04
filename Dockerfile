FROM python:3.8-slim

RUN mkdir -p /opt/vngitbot
WORKDIR /opt/vngitbot
COPY . /opt/vngitbot
ENV GITBOT_CONFIG_PATH=/opt/vngitbot/config/vngitbot.conf
RUN apt update -y
RUN apt install openssh-server -y
RUN pip install -r requirements.txt
EXPOSE 8000

CMD [ "python3", "/opt/vngitbot/vngitbot/main.py"]
