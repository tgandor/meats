import datetime

cache = {}


def current_date():
    """Prints formatted date and time into current document."""
    # get the doc from the scripting context which is made available to all scripts
    model = XSCRIPTCONTEXT.getDocument()
    # get the XText interface
    text = model.Text
    # create an XTextRange at the end of the document
    t_range = text.End
    # and set the string
    string = datetime.datetime.now().strftime("\n%Y-%m-%d (%a) %H:%M:%S")
    if 'last_log' in cache:
        time_delta = datetime.datetime.now() - cache['last_log']
        hours, seconds = divmod(time_delta.seconds, 3600)
        minutes, seconds = divmod(seconds, 60)
        string += ' [+ '
        if time_delta.days:
            string += '%dd ' % time_delta.days
        string += '%02d:%02d:%02d]' % (hours, minutes, seconds)
    cache['last_log'] = datetime.datetime.now()
    t_range.String = string + "\n"
    return None
