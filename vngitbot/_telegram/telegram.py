from _common import *
import requests

def notifyTagChange(oldTag, newTag, cluster, env, repoName, proxy, proxyInfo, token, channel):
    # Check Proxy enabled
    if proxy == "true": enableProxy(proxyInfo)

    bot_token = token 
    bot_chatID = '@' + channel #'@vngitbotchannel'
    bot_message = """
<b>Service</b>: {}
<b>Cluster</b>: {}-{}-workload
<b>Old tag</b>: {}  ==>  <b>New tag</b>: {}
""".format(repoName.split("/")[-1], cluster, env, oldTag, newTag,)
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=HTML&text=' + bot_message
    response = requests.get(send_text)
    # return response.json()
    if proxy == "true": disableProxy(proxyInfo)
