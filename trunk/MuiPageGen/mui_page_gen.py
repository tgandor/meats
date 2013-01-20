#!/usr/bin/env python

class Item(object):
    LABEL = 0
    CHECKBOX = 1
    SPACER = 2
    def __init__(self, kind, left=2, right=330, name=None):
        self.kind = kind
        self.left = left
        self.right = right
        self.field_id = 0
        self.formname = ''
	self.name = name
    def generate_getters(self, out):
        pass

class I18nItem(Item):
    langs = [
        ('en', 1033),
        ('de', 1031),
        ('pl', 1045),
    ]

    def __init__(self, kind, texts=[], **kwargs):
        super(I18nItem, self).__init__(kind, **kwargs)
        self.texts = texts
    def default_text(self):
        if len(self.texts) == 0:
            return "empty text"
        return self.texts[0][0]
    def render(self, out, top, bottom):
        out.write("[Field %d]\r\n" % self.field_id)
        out.write("Type=%s\r\n" % self.item_type())
        out.write("Text=%s\r\n" % self.default_text())
        out.write("Left=%d\r\nRight=%d\r\nTop=%d\r\nBottom=%d\r\n\r\n" % (
            self.left, self.right, top, bottom
        ))
    def _i18nSymbol(self):
        return "%s_FIELD_%d_TEXT" % (self.formname.upper(), self.field_id)

    def write_translations(self, out):
        for message in self.texts:
            for lang in self.langs:
                if message[1] in lang:
                    out.write("LangString %s %d \"%s\"\n" % (
                        self._i18nSymbol(), lang[1], message[0] ))

    def write_translate(self, out):
        if len(self.texts) < 2:
            return # no need to set text (none available)
        out.write(
"  !insertmacro MUI_INSTALLOPTIONS_WRITE \"%s.ini\" \"Field %d\" \"Text\" $(%s)\n"
% (self.formname, self.field_id, self._i18nSymbol()))


class Label(I18nItem):
    def __init__(self, **kwargs):
        super(Label, self).__init__(Item.LABEL, **kwargs)
    def item_type(self):
        return 'label'

class Checkbox(I18nItem):
    def __init__(self, name, **kwargs):
        super(Checkbox, self).__init__(Item.CHECKBOX, name=name, **kwargs)
        self.name = name
    def item_type(self):
        return 'checkbox'
    def generate_getters(self, out):
        out.write("""
!macro _%s.%s _a _b _t _f
  !insertmacro MUI_INSTALLOPTIONS_READ $_%s_temp "%s.ini" "Field %d" "State"
  StrCmp "1" $_%s_temp `${_t}` `${_f}`
!macroend 
!define %s.%s `"" %s.%s ""`
""" % (
    self.formname, self.name, self.formname, self.formname, self.field_id,
    self.formname, self.formname, self.name, self.formname, self.name
    ))


class Spacer(Item):
    def __init__(self, height=10, **kwargs):
        super(Spacer, self).__init__(Item.SPACER, **kwargs)
        self.height = height

class Form(object):
    topmost = 3
    item_height = 11
    item_below = 6

    def __init__(self, name):
        self.items = []
        self.fields = []
        self.name = name
        self.fieldnum = 0

    def generate(self):
        self.write_ini_file()

    def append(self, item):
        if isinstance(item, I18nItem):
            self.fieldnum += 1
            item.field_id = self.fieldnum
            item.formname = self.name
            self.fields.append(item)
        self.items.append(item)

    def write_ini_file(self):
        f = open(self.name+'.ini', 'wb')
        f.write("[Settings]\r\n")
        f.write("NumFields=%d\r\n\r\n" % self.fieldnum)
        top = Form.topmost
        for item in self.items:
            if item.kind == Item.SPACER:
                top += item.height
            elif isinstance(item, I18nItem):
                item.render(f, top, top + self.item_height)
                top += self.item_height + self.item_below
        f.close()

    def write_nsh_file(self):
        f = open(self.name+'.nsh', 'w')
        f.write("; This file was generated with mui_page_gen.py\n\n")
        f.write("!include LogicLib.nsh\n\n")
        f.write("Var /GLOBAL _%s_temp\n\n" % self.name)
        f.write("; Language strings\n\n")
        for field in self.fields:
            field.write_translations(f)
        f.write("\n; Initialization\n\n")

        # Page function to translate etc.
        f.write("Function %sStandardInit\n" % self.name.capitalize())
        f.write('  ReserveFile "%s.ini"\n' % self.name)
        f.write('  !insertmacro MUI_INSTALLOPTIONS_EXTRACT "%s.ini"\n' % self.name)
        for field in self.fields:
            field.write_translate(f)
        f.write("FunctionEnd\n\n")
        # Default page function
        f.write("Function %sCustomPage\n" % self.name.capitalize())
        f.write("  Call %sStandardInit\n" % self.name.capitalize())
        f.write('  !insertmacro MUI_INSTALLOPTIONS_DISPLAY "%s.ini"\n' %
                self.name)
        f.write("FunctionEnd\n\n")
        for field in self.fields:
            field.generate_getters(f)
        f.close()

def test():
    form = Form('components')
    form.append(Label())
    form.append(Checkbox('shortcut', texts=[('mark me', 'en')]))
    form.append(Spacer())
    form.append(Label(texts=[('fiu', 'pl'), ('phew', 'en')]))
    form.write_ini_file()
    form.write_nsh_file()

if __name__ == '__main__':
    test()
