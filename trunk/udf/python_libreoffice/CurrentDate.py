import datetime


def current_date():
    """Prints formated date and time into current document."""
    # get the doc from the scripting context which is made available to all scripts
    model = XSCRIPTCONTEXT.getDocument()
    # get the XText interface
    text = model.Text
    # create an XTextRange at the end of the document
    tRange = text.End
    # and set the string
    tRange.String = datetime.datetime.now().strftime("%Y-%m-%d (%a) %H:%M:%S\n")
    return None
