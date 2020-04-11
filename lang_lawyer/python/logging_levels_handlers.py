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

logging.basicConfig(
    level=logging.DEBUG,
    # format='%(asctime)s %(message)s', - works, but only here, no effect afterwards...
    # format='{asctime} {message}', - this doesn't work! (3.7)
)

print('\n- basicConfig(level=logging.DEBUG): -\n')
log_messages(' config with level==logging.DEBUG')
print('\n- basicConfig(level=logging.DEBUG), named: -\n')
log_messages(' named with level', logger_name='Aga')

# custom format

print('\n- basicConfig(format={asctime} {message}): -\n')

logging.basicConfig(format='%(asctime)s %(message)s')
log_messages('with format (time)', 'time+message')

# calling directly from the module:

print('\n- from module (logging.debug(...) etc.) -\n')

context = 'logging module'
logging.debug(context + ' debug')
logging.info(context + ' info')
logging.warning(context + ' warning')
logging.error(context + ' error')
logging.critical(context + ' critical')

logging.basicConfig(level=logging.INFO)

context = 'logging module level INFO'
logging.debug(context + ' debug')
logging.info(context + ' info')
logging.warning(context + ' warning')
logging.error(context + ' error')
logging.critical(context + ' critical')

print('This module is dumb, not in a funny way.')
print('It is also very inconvenient, see:')

print("""
import logging
cons = logging.StreamHandler()
cons.setLevel(logging.INFO)
log = logging.FileHandler('debug.log')
log.setLevel(logging.DEBUG)
logging.basicConfig(handlers=[cons, log], format='%(message)s', level=logging.DEBUG)
""")

print('So you better configure everything in one shot, see tee_logging.py')
