import logging

loggerName = 'consumer'
logger = logging.getLogger(loggerName)

cHandler = logging.StreamHandler()
fHandler = logging.FileHandler('consumerlog.txt')
cHandler.setLevel(logging.INFO)
fHandler.setLevel(logging.CRITICAL)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(message)s')
cHandler.setFormatter(formatter)
fHandler.setFormatter(formatter)

logger.addHandler(cHandler)
logger.addHandler(fHandler)


logger.info("LMAO")