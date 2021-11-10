FROM python
RUN mkdir -p /opt/vngitbot
WORKDIR /opt/vngitbot
COPY . /opt/vngitbot
RUN pip3 install -r requirements.txt
EXPOSE 8000
ENV GITBOT_CONFIG_PATH=/opt/vngitbot/config/vngitbot.conf
CMD [ "python3", "/opt/vngitbot/vngitbot/launch.py"]