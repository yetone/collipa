# coding: utf-8

from collipa.libs.tforms.forms import TornadoForm as Form


class BaseForm(Form):
    def __init__(self, *args, **kargs):
        self._obj = kargs.get('obj')
        super(BaseForm, self).__init__(*args, **kargs)
