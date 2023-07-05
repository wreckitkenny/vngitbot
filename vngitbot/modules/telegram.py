from utils import BasicConfig
import requests, json

class Telegram:
    def __init__(self):
        bc = BasicConfig()
        self.parser = bc.parser
        self.token=self.parser.get('TELEGRAM', 'TELEGRAM_TOKEN')
        self.channel=self.parser.get('TELEGRAM', 'TELEGRAM_CHANNEL')
        self.cluster = self.parser.get('GENERAL', 'CLUSTER')

    def notifyTagChange(self, oldTag, newTag, env, repoName):
        channel = json.loads(self.channel)
        bot_message = """
<b>VNGITBOT has changed version tag for deployment.</b>
<b>Service</b>: <code>{}</code>
<b>Cluster</b>: <code>{}-{}-workload</code>
<b>Old tag</b>: <code>{}</code>  ==>  <b>New tag</b>: <code>{}</code>
""".format(repoName.split("/")[-1], self.cluster, env, oldTag, newTag)
        send_text = 'https://api.telegram.org/bot{}/sendMessage?chat_id={}&parse_mode=HTML&text={}'.format(self.token, channel[env], bot_message)
        requests.get(send_text)


#     def notifySuccess(self, imageName, startedTime):
#         channel = json.loads(self.channel)
#         bot_message = """
# <b>Service [<code>{}</code>] with new version [<code>{}</code>] has been successfully deployed at [<code>{}</code>].</b>
#     """.format(imageName.split(':')[0].split('/')[-1], imageName.split(':')[-1], startedTime)
#         send_text = 'https://api.telegram.org/bot{}/sendMessage?chat_id={}&parse_mode=HTML&text={}'.format(self.token, channel[self.cluster], bot_message)
#         requests.get(send_text)


#     def notifyFailure(self, imageName):
#         channel = json.loads(self.channel)
#         bot_message = """
# <b>Service [<code>{}</code>] with new version [<code>{}</code>] has failed to deploy.</b>
#     """.format(imageName.split(':')[0].split('/')[-1], imageName.split(':')[-1])
#         send_text = 'https://api.telegram.org/bot{}/sendMessage?chat_id={}&parse_mode=HTML&text={}'.format(self.token, channel[self.cluster], bot_message)
#         requests.get(send_text)


#     def notifyPipelineFailure(self, namespace, project, commitMsg):
#         # Check Proxy enabled
#         if self.proxy == "true": enableProxy(self.proxyInfo)
#         channel = json.loads(self.channel)
#         bot_message = """
# <b>There is a failure in CD pipeline: </b>
# <b>Group</b>: <code>{}</code>
# <b>Project</b>: <code>{}</code>
# <b>Commit message</b>: <code>{}</code>
#     """.format(namespace, project, commitMsg)
#         send_text = 'https://api.telegram.org/bot{}/sendMessage?chat_id=-1001670740257&parse_mode=HTML&text={}'.format(self.token, bot_message)
#         requests.get(send_text)
#         # return response.json()
#         if self.proxy == "true": disableProxy(self.proxyInfo)
