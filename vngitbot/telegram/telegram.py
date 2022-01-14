from utils import BasicConfig, enableProxy, disableProxy
import requests

class Telegram:
    def __init__(self):
        bc = BasicConfig()
        self.parser = bc.parser
        self.proxy = self.parser.get('PROXY','ENABLED')
        self.proxyInfo = self.parser.get('PROXY','PROXY_ADDRESS')
        self.token=self.parser.get('TELEGRAM', 'TELEGRAM_TOKEN')
        self.channel=self.parser.get('TELEGRAM', 'TELEGRAM_CHANNEL')

    def notifyTagChange(self, oldTag, newTag, cluster, env, repoName):
        # Check Proxy enabled
        if self.proxy == "true": enableProxy(self.proxyInfo)
        bot_message = """
<b>VNGITBOT has changed version tag for deployment.</b>
<b>Service</b>: <code>{}</code>
<b>Cluster</b>: <code>{}-{}-workload</code>
<b>Old tag</b>: <code>{}</code>  ==>  <b>New tag</b>: <code>{}</code>
""".format(repoName.split("/")[-1], cluster, env, oldTag, newTag)
        send_text = 'https://api.telegram.org/bot' + self.token + '/sendMessage?chat_id=@' + self.channel + '&parse_mode=HTML&text=' + bot_message
        response = requests.get(send_text)
        if self.proxy == "true": disableProxy(self.proxyInfo)


    def notifySuccess(self, imageName, startedTime):
        # Check Proxy enabled
        if self.proxy == "true": enableProxy(self.proxyInfo)
        bot_message = """
    <b>Service [<code>{}</code>] with new version [<code>{}</code>] has been successfully deployed at [<code>{}</code>].</b>
    """.format(imageName.split(':')[0].split('/')[-1], imageName.split(':')[-1], startedTime)
        send_text = 'https://api.telegram.org/bot' + self.token + '/sendMessage?chat_id=@' + self.channel + '&parse_mode=HTML&text=' + bot_message
        response = requests.get(send_text)
        # return response.json()
        if self.proxy == "true": disableProxy(self.proxyInfo)
