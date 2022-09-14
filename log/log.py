import logging


class Logger:
    __register = False

    def __init__(self):
        if not self.__register: #this will run only on first call
            self._init_default_register()

    def _init_default_register(self):
        logger = logging.getLogger() # first time init as root loger
        logger.setLevel(logging.INFO) # refer https://docs.python.org/3/library/logging.html#levels
        Logger.__register = True
        logging.info("Logger initialized")

    def get_logger(self, filename):
        return logging.getLogger(filename)


def log(cls):
    cls.log = Logger().get_logger(cls.__name__) # calling Logger class and it's method get_logger
    return cls



#better to use this things as decorators
''' 
@log 
class xyz:
    def b(self):
        self.log.info("Proxy record" )

a = xyz()
a.b()
'''



