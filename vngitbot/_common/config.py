import os, configparser, logging, gitlab

class BasicConfig:
    # def __init__(self):
    configPath = os.getenv('GITBOT_CONFIG_PATH')
    # configPath = 'D:\\Code\\7.VNPAY\\CI\\gitbot\\gitbot.conf'
    binPath = '/'.join(configPath.split('/')[:-1])

    # Config file module
    parser = configparser.ConfigParser()
    parser.read(configPath)

    # Gitlab module
    gl = gitlab.Gitlab(parser.get('GITLAB', 'GITLAB_ADDRESS'), private_token=parser.get('GITLAB', 'GITLAB_TOKEN'))

    # Logging module
    def logConfig(parser):
        level = parser.get('LOG', 'LOG_LEVEL')
        if level == 'INFO': lvl = logging.INFO
        if level == 'DEBUG': lvl = logging.DEBUG
        logging.basicConfig(filename=parser.get('LOG', 'LOG_PATH')+'/'+parser.get('LOG', 'LOG_FILENAME'), 
                            level=lvl,
                            format='%(asctime)s | %(levelname)s | %(message)s',
                            datefmt='%d/%m/%Y | %I:%M:%S')