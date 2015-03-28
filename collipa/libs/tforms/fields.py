
import itertools
import datetime
import time
from tornado.escape import to_unicode, utf8
from collipa.libs.tforms import widgets
from collipa.libs.tforms.validators import StopValidation

__all__ = (
    'Field', 'TextField',
)


class _DummyLocale(object):
    def translate(self, message, plural_message=None, count=None):
        if plural_message is not None:
            assert count is not None
            return plural_message
        return message


_unset_value = object()


class Field(object):
    """
    Field base class
    """
    widget = None
    errors = tuple()
    process_errors = tuple()
    required = False
    maxlength = None
    _formfield = True
    _locale = _DummyLocale()

    def __new__(cls, *args, **kwargs):
        if '_form' in kwargs and '_name' in kwargs:
            return super(Field, cls).__new__(cls)
        else:
            return UnboundField(cls, *args, **kwargs)

    def __init__(self, label=None, validators=None, filters=tuple(),
                 description='', id=None, default=None, widget=None,
                 _form=None, _name=None, _prefix='', _locale=None):
        """
        Construct a new field.

        :param label:
            The label of the field.
        :param validators:
            A sequence of validators to call when `validate` is called.
        :param filters:
            A sequence of filters which are run on input data by `process`.
        :param description:
            A description for the field, typically used for help text.
        :param id:
            An id to use for the field. A reasonable default is set by the form,
            and you shouldn't need to set this manually.
        :param default:
            The default value to assign to the field, if no form or object
            input is provided. May be a callable.
        :param widget:
            If provided, overrides the widget used to render the field.
        :param _form:
            The form holding this field. It is passed by the form itself during
            construction. You should never pass this value yourself.
        :param _name:
            The name of this field, passed by the enclosing form during its
            construction. You should never pass this value yourself.
        :param _prefix:
            The prefix to prepend to the form name of this field, passed by
            the enclosing form during construction.

        If `_form` and `_name` isn't provided, an :class:`UnboundField` will be
        returned instead. Call its :func:`bind` method with a form instance and
        a name to construct the field.
        """
        self.name = _name
        if _locale is not None:
            self._locale = _locale
        self.id = id or _prefix + self.name
        if label is None:
            label = _name.replace('_', ' ').title()
        self.label = Label(self.id, self.translate(label))
        if validators is None:
            validators = []
        self.validators = validators
        self.filters = filters
        self.description = self.translate(description)
        self.type = type(self).__name__
        self.default = default
        self.raw_data = None
        if widget:
            self.widget = widget

        for v in validators:
            flag = getattr(v, 'field_flag', None)
            if flag and flag == 'required':
                self.required = True
            elif flag and flag == 'length' and v.max:
                self.maxlength = v.max

    def __unicode__(self):
        """
        Returns a HTML representation of the field. For more powerful rendering,
        see the `__call__` method.
        """
        return self()

    def __str__(self):
        """
        Returns a HTML representation of the field. For more powerful rendering,
        see the `__call__` method.
        """
        return utf8(self())

    def __call__(self, **kwargs):
        """
        Render this field as HTML, using keyword args as additional attributes.

        Any HTML attribute passed to the method will be added to the tag
        and entity-escaped properly.
        """
        return self.widget(self, **kwargs)

    def translate(self, message, plural_message=None, count=None):
        return self._locale.translate(message, plural_message, count)

    def validate(self, form, extra_validators=tuple()):
        """
        Validates the field and returns True or False. `self.errors` will
        contain any errors raised during validation. This is usually only
        called by `Form.validate`.

        Subfields shouldn't override this, but rather override either
        `pre_validate`, `post_validate` or both, depending on needs.

        :param form: The form the field belongs to.
        :param extra_validators: A list of extra validators to run.
        """
        self.errors = list(self.process_errors)
        stop_validation = False

        # Call pre_validate
        try:
            self.pre_validate(form)
        except StopValidation as e:
            if e.args and e.args[0]:
                self.errors.append(e.args[0])
            stop_validation = True
        except ValueError as e:
            self.errors.append(e.args[0])

        # Run validators
        if not stop_validation:
            for validator in itertools.chain(self.validators, extra_validators):
                try:
                    validator(form, self)
                except StopValidation as e:
                    if e.args and e.args[0]:
                        self.errors.append(e.args[0])
                    stop_validation = True
                    break
                except ValueError as e:
                    self.errors.append(e.args[0])

        # Call post_validate
        try:
            self.post_validate(form, stop_validation)
        except ValueError as e:
            self.errors.append(e.args[0])

        return len(self.errors) == 0

    def pre_validate(self, form):
        """
        Override if you need field-level validation. Runs before any other
        validators.

        :param form: The form the field belongs to.
        """
        pass

    def post_validate(self, form, validation_stopped):
        """
        Override if you need to run any field-level validation tasks after
        normal validation. This shouldn't be needed in most cases.

        :param form: The form the field belongs to.
        :param validation_stopped:
            `True` if any validator raised StopValidation.
        """
        pass

    def process(self, formdata, data=_unset_value):
        """
        Process incoming data, calling process_data, process_formdata as needed,
        and run filters.

        If `data` is not provided, process_data will be called on the field's
        default.

        Field subclasses usually won't override this, instead overriding the
        process_formdata and process_data methods. Only override this for
        special advanced processing, such as when a field encapsulates many
        inputs.
        """
        self.process_errors = []
        if data is _unset_value:
            try:
                data = self.default()
            except TypeError:
                data = self.default
        try:
            self.process_data(data)
        except ValueError as e:
            self.process_errors.append(e.args[0])

        # logical fix. obj is the default value
        if formdata and self.name in formdata:
            try:
                self.raw_data = formdata.getlist(self.name)
                self.process_formdata(self.raw_data)
            except ValueError as e:
                self.process_errors.append(e.args[0])

        for _filter in self.filters:
            try:
                self.data = _filter(self.data)
            except ValueError as e:
                self.process_errors.append(e.args[0])

    def process_data(self, value):
        """
        Process the Python data applied to this field and store the result.

        This will be called during form construction by the form's `kwargs` or
        `obj` argument.

        :param value: The python object containing the value to process.
        """
        self.data = value

    def process_formdata(self, valuelist):
        """
        Process data received over the wire from a form.

        This will be called during form construction with data supplied
        through the `formdata` argument.

        :param valuelist: A list of strings to process.
        """
        if valuelist:
            self.data = to_unicode(valuelist[0])
        else:
            self.data = to_unicode(None)

    def populate_obj(self, obj, name):
        """
        Populates `obj.<name>` with the field's data.

        :note: This is a destructive operation. If `obj.<name>` already exists,
               it will be overridden. Use with caution.
        """
        setattr(obj, name, self.data)

    def _value(self):
        return to_unicode(self.data)


class UnboundField(object):
    _formfield = True
    creation_counter = 0

    def __init__(self, field_class, *args, **kwargs):
        UnboundField.creation_counter += 1
        self.field_class = field_class
        self.args = args
        self.kwargs = kwargs
        self.creation_counter = UnboundField.creation_counter

    def bind(self, form, name, prefix='', locale=None, **kwargs):
        return self.field_class(_form=form, _prefix=prefix, _name=name, _locale=locale, *self.args, **dict(self.kwargs, **kwargs))

    def __repr__(self):
        return '<UnboundField(%s, %r, %r)>' % (self.field_class.__name__, self.args, self.kwargs)


class Label(object):
    """
    An HTML form label.
    """
    def __init__(self, field_id, text):
        self.field_id = field_id
        self.text = text

    def __str__(self):
        return utf8(self())

    def __unicode__(self):
        return self()

    def __call__(self, text=None, **kwargs):
        kwargs['for'] = self.field_id
        if 'class' not in kwargs or 'class_' not in kwargs:
            kwargs['class'] = 'fm-label'
        attributes = widgets.html_params(**kwargs)
        return '<label %s>%s</label>' % (attributes, to_unicode(text) or to_unicode(self.text))

    def __repr__(self):
        return 'Label(%r, %r)' % (self.field_id, self.text)


class TextField(Field):
    """
    This field is the base for most of the more complicated fields, and
    represents an ``<input type="text">``.
    """

    widget = widgets.TextInput()

    def __call__(self, **kwargs):
        if self.maxlength:
            kwargs['maxlength'] = str(self.maxlength)
        return self.widget(self, **kwargs)

    def _value(self):
        if self.data:
            return to_unicode(self.data)
        return to_unicode('')


class HiddenField(TextField):
    """
    Represents an ``<input type="hidden">``.
    """
    widget = widgets.HiddenInput()


class TextAreaField(TextField):
    """
    This field represents an HTML ``<textarea>`` and can be used to take
    multi-line input.
    """
    widget = widgets.TextArea()


class PasswordField(TextField):
    """
    Represents an ``<input type="password">``.
    """
    widget = widgets.PasswordInput()


class IntegerField(TextField):
    """
    A text field, except all input is coerced to an integer.  Erroneous input
    is ignored and will not be accepted as a value.
    """
    def _value(self):
        if self.raw_data:
            return self.raw_data[0]
        elif self.data is not None:
            return to_unicode(str(self.data))
        return ''

    def process_formdata(self, valuelist):
        if valuelist:
            try:
                self.data = int(valuelist[0])
            except ValueError:
                raise ValueError(self.translate('Not a valid integer value'))


class FloatField(TextField):
    """
    A text field, except all input is coerced to an float.  Erroneous input
    is ignored and will not be accepted as a value.
    """
    def _value(self):
        if self.raw_data:
            return self.raw_data[0]
        elif self.data is not None:
            return to_unicode(self.data)
        return ''

    def process_formdata(self, valuelist):
        if valuelist:
            try:
                self.data = float(valuelist[0])
            except ValueError:
                raise ValueError(self.translate('Not a valid float value'))


class BooleanField(Field):
    """
    Represents an ``<input type="checkbox">``.
    """
    widget = widgets.CheckboxInput()

    def process_data(self, value):
        self.data = bool(value)

    def process_formdata(self, valuelist):
        # Checkboxes and submit buttons simply do not send a value when
        # unchecked/not pressed. So the actual value="" doesn't matter for
        # purpose of determining .data, only whether one exists or not.
        self.data = bool(valuelist)

    def _value(self):
        if self.raw_data:
            return to_unicode(self.raw_data[0])
        return 'y'


class DateTimeField(Field):
    """
    A text field which stores a `datetime.datetime` matching a format.
    """
    widget = widgets.TextInput()

    def __init__(self, label=None, validators=None, format='%Y-%m-%d %H:%M:%S', **kwargs):
        super(DateTimeField, self).__init__(label, validators, **kwargs)
        self.format = format

    def _value(self):
        if self.raw_data:
            return to_unicode(' '.join(self.raw_data))
        return self.data and self.data.strftime(self.format) or ''

    def process_formdata(self, valuelist):
        if valuelist:
            date_str = to_unicode(' '.join(valuelist))
            try:
                timetuple = time.strptime(date_str, self.format)
                self.data = datetime.datetime(*timetuple[:6])
            except ValueError:
                self.data = None
                raise ValueError(self.translate('Not a valid datetime value'))


class DateField(DateTimeField):
    """
    Same as DateTimeField, except stores a `datetime.date`.
    """
    def __init__(self, label=None, validators=None, format='%Y-%m-%d', **kwargs):
        super(DateField, self).__init__(label, validators, format, **kwargs)

    def process_formdata(self, valuelist):
        if valuelist:
            date_str = to_unicode(' '.join(valuelist))
            try:
                timetuple = time.strptime(date_str, self.format)
                self.data = datetime.date(*timetuple[:3])
            except ValueError:
                self.data = None
                raise ValueError(self.translate('Not a valid date value'))


class SelectFieldBase(Field):
    option_widget = widgets.Option()

    """
    Base class for fields which can be iterated to produce options.

    This isn't a field, but an abstract base class for fields which want to
    provide this functionality.
    """
    def __init__(self, label=None, validators=None, option_widget=None, **kwargs):
        super(SelectFieldBase, self).__init__(label, validators, **kwargs)

        if option_widget is not None:
            self.option_widget = option_widget

    def iter_choices(self):
        """
        Provides data for choice widget rendering. Must return a sequence or
        iterable of (value, label, selected) tuples.
        """
        raise NotImplementedError()

    def __iter__(self):
        opts = dict(widget=self.option_widget, _name=self.name, _form=None)
        for i, (value, label, checked) in enumerate(self.iter_choices()):
            opt = self._Option(label=label, id='%s-%d' % (self.id, i), **opts)
            opt.process(None, value)
            opt.checked = checked
            yield opt

    class _Option(Field):
        checked = False

        def _value(self):
            return self.data


class SelectField(SelectFieldBase):
    widget = widgets.Select()

    def __init__(self, label=None, validators=None, coerce=to_unicode, choices=None, **kwargs):
        super(SelectField, self).__init__(label, validators, **kwargs)
        self.coerce = coerce
        self.choices = choices

    def iter_choices(self):
        for value, label in self.choices:
            label = self.translate(label)
            yield (value, label, self.coerce(value) == self.data)

    def process_data(self, value):
        try:
            self.data = self.coerce(value)
        except (ValueError, TypeError):
            self.data = None

    def process_formdata(self, valuelist):
        if valuelist:
            try:
                self.data = self.coerce(valuelist[0])
            except ValueError:
                raise ValueError(self.translate('Invalid Choice: could not coerce'))

    def pre_validate(self, form):
        for v, _ in self.choices:
            if self.data == v:
                break
        else:
            raise ValueError(self.translate('Not a valid choice'))


class SelectMultipleField(SelectField):
    """
    No different from a normal select field, except this one can take (and
    validate) multiple choices.  You'll need to specify the HTML `rows`
    attribute to the select field when rendering.
    """
    widget = widgets.Select(multiple=True)

    def iter_choices(self):
        for value, label in self.choices:
            selected = self.data is not None and self.coerce(value) in self.data
            yield (value, label, selected)

    def process_data(self, value):
        try:
            self.data = list(self.coerce(v) for v in value)
        except (ValueError, TypeError):
            self.data = None

    def process_formdata(self, valuelist):
        try:
            self.data = list(self.coerce(x) for x in valuelist)
        except ValueError:
            raise ValueError(self.translate('Invalid choice(s): one or more data inputs could not be coerced'))

    def pre_validate(self, form):
        if self.data:
            values = list(c[0] for c in self.choices)
            for d in self.data:
                if d not in values:
                    raise ValueError(self.translate("'%(value)s' is not a valid choice for this field") % dict(value=d))
