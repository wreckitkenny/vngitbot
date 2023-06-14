FROM python:3.8-slim

RUN mkdir -p /opt/vngitbot
WORKDIR /opt/vngitbot
COPY . /opt/vngitbot
ENV GITBOT_CONFIG_PATH=/opt/vngitbot/config/vngitbot.conf

# RUN mkdir -p /root/.config/pip
# RUN cp ./pip.conf /root/.config/pip
# RUN sed -i 's/http:\/\/deb.debian.org/https:\/\/artifact.vnpay.vn\/nexus\/repository\/apt-proxy_deb.debian.org/g' /etc/apt/sources.list
RUN apt update -y
RUN apt install openssh-server -y

RUN pip install -r requirements.txt
EXPOSE 8000

CMD [ "python3", "/opt/vngitbot/vngitbot/launch.py"]
