import logging
import os
# import logging.handlers import TimedRotatingFileHandler
from Log.logConfig import LOG_CONFIG


# LOG_PATH = os.environ.get('LOG_PATH', os.path.join(os.getcwd(), 'logdata.log'))

class CustomLogger:
    def __init__(self, logger):
        """
           Currently this CustomLogger will do write logs to stream handler.
           If we need to write to log file we need to create those instances do log level setting.
           
           Log Level default set to 'DEBUG' we can do set at env specific log level dynamically
        """
        self.logger = logger
        self.logger.setLevel(LOG_CONFIG['LEVEL']['DEBUG'])
        
        console_handler = logging.StreamHandler()
        console_handler.setLevel(LOG_CONFIG['LEVEL']['DEBUG'])
        formatter = logging.Formatter(LOG_CONFIG['MESSAGE_FORMAT'], LOG_CONFIG['TIME_FORMAT'])
        console_handler.setFormatter(formatter)
        
        self.logger.addHandler(console_handler)
    
    def get_logger(self):
        return self.logger