import os, configparser, logging, gitlab

class BasicConfig:
    def __init__(self):
        self.configPath = os.getenv('GITBOT_CONFIG_PATH')
        # configPath = 'D:\\Code\\7.VNPAY\\CI\\gitbot\\gitbot.conf'
        self.binPath = '/'.join(self.configPath.split('/')[:-2])

        # Config file module
        self.parser = configparser.ConfigParser()
        self.parser.read(self.configPath)

        # Gitlab module
        self.gl = gitlab.Gitlab(self.parser.get('GITLAB', 'GITLAB_ADDRESS'), private_token=self.parser.get('GITLAB', 'GITLAB_TOKEN'))

    # Logging module
    def logConfig(self):
        level = self.parser.get('LOG', 'LOG_LEVEL')
        if level == 'INFO': lvl = logging.INFO
        if level == 'DEBUG': lvl = logging.DEBUG
        logging.basicConfig(filename=self.parser.get('LOG', 'LOG_PATH')+'/'+self.parser.get('LOG', 'LOG_FILENAME'), 
                            level=lvl,
                            format='%(asctime)s | %(levelname)s | %(message)s',
                            datefmt='%d/%m/%Y | %I:%M:%S')