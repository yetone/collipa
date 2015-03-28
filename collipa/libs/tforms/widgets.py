
from tornado.escape import to_unicode, xhtml_escape


def html_params(**kwargs):
    """
    Generate HTML parameters from inputted keyword arguments.

    The output value is sorted by the passed keys, to provide consistent output
    each time this function is called with the same parameters.  Because of the
    frequent use of the normally reserved keywords `class` and `for`, suffixing
    these with an underscore will allow them to be used.

    >>> html_params(name='text1', id='f', class_='text')
    'class="text" id="f" name="text1"'
    """
    params = []
    for k, v in sorted(kwargs.iteritems()):
        if k in ('class_', 'for_'):
            k = k[:-1]
        if k.startswith('data_'):
            k = 'data-' + k[5:]
        if v is True:
            params.append(k)
        else:
            params.append('%s="%s"' % (to_unicode(k), xhtml_escape(to_unicode(v))))
    return ' '.join(params)


class Input(object):
    """
    Render a basic ``<input>`` field.

    This is used as the basis for most of the other input fields.

    By default, the `_value()` method will be called upon the associated field
    to provide the ``value=`` HTML attribute.
    """

    def __init__(self, input_type=None):
        if input_type is not None:
            self.input_type = input_type

    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        kwargs.setdefault('type', self.input_type)
        if 'value' not in kwargs:
            kwargs['value'] = field._value()
        return '<input %s>' % html_params(name=field.name, **kwargs)

class TextArea(object):
    """
    Render a ``<textarea>`` field.
    """

    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        return '<textarea %s>%s</textarea>' % (html_params(name=field.name, **kwargs), xhtml_escape(to_unicode(field._value())))

class TextInput(Input):
    input_type = 'text'

class HiddenInput(Input):
    input_type = 'hidden'

class EmailInput(Input):
    input_type = 'email'

class URLInput(Input):
    input_type = 'url'

class NumberInput(Input):
    input_type = 'number'

class PasswordInput(Input):
    """
    Render a password input.

    For security purposes, this field will not reproduce the value on a form
    submit by default. To have the value filled in, set `hide_value` to
    `False`.
    """
    input_type = 'password'

    def __init__(self, hide_value=True):
        self.hide_value = hide_value

    def __call__(self, field, **kwargs): 
        if self.hide_value:
            kwargs['value'] = ''
        return super(PasswordInput, self).__call__(field, **kwargs)

class Select(object):
    """
    Renders a select field.

    If `multiple` is True, then the `size` property should be specified on
    rendering to make the field useful.

    The field must provide an `iter_choices()` method which the widget will
    call on rendering; this method must yield tuples of 
    `(value, label, selected)`.
    """
    def __init__(self, multiple=False):
        self.multiple = multiple

    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        if self.multiple:
            kwargs['multiple'] = True 
        html = ['<select %s>' % html_params(name=field.name, **kwargs)]
        for val, label, selected in field.iter_choices():
            html.append(self.render_option(val, label, selected))
        html.append('</select>')
        return ''.join(html)

    @classmethod
    def render_option(cls, value, label, selected):
        options = {'value': value}
        if selected:
            options['selected'] = True 
        return '<option %s>%s</option>' % (html_params(**options), xhtml_escape(to_unicode(label)))

class Option(object):
    """
    Renders the individual option from a select field. 
    
    This is just a convenience for various custom rendering situations, and an
    option by itself does not constitute an entire field.
    """
    def __call__(self, field, **kwargs):
        return Select.render_option(field._value(), field.label.text, field.checked)

class CheckboxInput(Input):
    """
    Render a checkbox.

    The ``checked`` HTML attribute is set if the field's data is a non-false value.
    """
    input_type = 'checkbox'

    def __call__(self, field, **kwargs):
        if getattr(field, 'checked', field.data):
            kwargs['checked'] = True
        return super(CheckboxInput, self).__call__(field, **kwargs)
