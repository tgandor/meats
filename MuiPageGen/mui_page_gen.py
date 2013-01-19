#!/usr/bin/env python

class Item(object):
    LABEL = 0
    CHECKBOX = 1
    SPACER = 2
    langs = [
        ('en', 1033),
        ('de', 1031),
        ('pl', 1045),
    ]
    def __init__(self, kind, left=2, right=330):
        self.kind = kind
        self.left = left
        self.right = right
        self.field_id = 0

class I18nItem(Item):
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

class Label(I18nItem):
    def __init__(self, **kwargs):
        super(Label, self).__init__(Item.LABEL, **kwargs)
    def item_type(self):
        return 'label'

class Checkbox(I18nItem):
    def __init__(self, name, **kwargs):
        super(Checkbox, self).__init__(Item.CHECKBOX, **kwargs)
        self.name = name
    def item_type(self):
        return 'checkbox'

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
        self.name = name
        self.fieldnum = 0

    def generate(self):
        self.write_ini_file()

    def append(self, item):
        if isinstance(item, I18nItem):
            self.fieldnum += 1
            item.field_id = self.fieldnum
        self.items.append(item)

    def write_ini_file(self):
        f = open(self.name+'.ini', 'wb')
        f.write("[Settings]\r\n")
        f.write("NumFields=%d\r\n\r\n" % len(self.items))
        top = Form.topmost
        for item in self.items:
            if item.kind == Item.SPACER:
                top += item.height
            elif isinstance(item, I18nItem):
                self.fieldnum += 1
                item.render(f, top, top + self.item_height)
                top += self.item_height + self.item_below
        f.close()

def test():
    form = Form('components')
    form.append(Label())
    form.append(Checkbox('shortcut'))
    form.append(Spacer())
    form.append(Label(texts=[('fiu', 'pl')]))
    form.write_ini_file()

if __name__ == '__main__':
    test()
