import logging
import sys

cons = logging.StreamHandler(stream=sys.stdout)  # works, and 3.7 has even setStream() for switching
cons.setLevel(logging.INFO)
cons.setFormatter(logging.Formatter('%(levelname)s %(message)s'))
# cons.addFilter(print) - nice, prints log records

# but use this, if you want to go deeper into LogRecords
def filter(lr):
    import code; code.interact(local=locals())
    return True
# cons.addFilter(filter)

cons.addFilter(lambda log_record: log_record.levelno < logging.WARNING)

err = logging.StreamHandler()
err.setLevel(logging.WARNING)
# err.setFormatter('STDERR: %(message)s')
err.setFormatter(logging.Formatter('STDERR: %(message)s'))

log = logging.FileHandler('debug.log')
log.setLevel(logging.DEBUG)
log.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))

logging.basicConfig(handlers=[err, cons, log], format='%(message)s', level=logging.DEBUG)

logging.info('info goes to both')
logging.debug('debug goes to file')
logging.warning('warning and above would go to all three, but is filtered from cons')
