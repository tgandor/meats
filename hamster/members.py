import androidhelper as module
import inspect
import sys

dont_call_these = {
    # TMI
    'getLaunchableApplications',
    'getRunningPackages',
    # NullPointerException when called
    'getDeviceId',
    'getDeviceSoftwareVersion',
    'getSubscriberId',
    'getVoiceMailAlphaTag',
    'getVoiceMailNumber',
    'getSimSerialNumber',
    'getLine1Number',
}

call_these_anyway = {
    'wifiGetConnectionInfo',
    'checkWifiState',
    # 'contactsGetCount', # NPE
}

def describe(module, out=sys.stdout):
    for field in dir(module):
        if field.startswith('_'):
            continue
        value = getattr(module, field)
        if inspect.isfunction(value) or inspect.ismethod(value):
            spec = inspect.getargspec(value)
            if len(spec.args) and spec.args[0] == 'self': # omit self argument
                spec_str = inspect.formatargspec(spec.args[1:], spec.varargs, spec.keywords, spec.defaults)
            else:
                spec_str = inspect.formatargspec(*spec)
            out.write('{}{}\n'.format(field, spec_str))
            if (len(spec.args) == 1 and field.startswith('get') and (field not in dont_call_these)) or field in call_these_anyway:
                out.write('  = {}\n'.format(value()))
            out.write('-' * 40 + '\n')
            continue
        out.write("{} : {} = {}\n".format(field, type(value).__name__, repr(value)))
        out.write('-' * 40 + '\n')

describe(module.Android())
with open('/mnt/sdcard/Download/AH.txt', 'w') as f:
    describe(module.Android(), f)

module.Android().makeToast('The results were saved to Download/AH.txt')
