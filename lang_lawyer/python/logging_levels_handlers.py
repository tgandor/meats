import logging


def log_messages(context='default', logger_name=None):
    logger = logging.getLogger(logger_name)
    logger.debug(context + ' debug')
    logger.info(context + ' info')
    logger.warning(context + ' warning')
    logger.error(context + ' error')
    logger.critical(context + ' critical')


# default configuration

print('\n- Without basicConfig(): -\n')
log_messages()
print('\n- Without basicConfig(), named: -\n')
log_messages(logger_name='Ada')

# lowering level

print('\n- basicConfig(level=logging.DEBUG): -\n')
logging.basicConfig(level=logging.DEBUG)
log_messages(' config with level==logging.DEBUG')
print('\n- basicConfig(level=logging.DEBUG), named: -\n')
log_messages(' named with level', logger_name='Aga')
