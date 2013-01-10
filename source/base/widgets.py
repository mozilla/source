'''
Original AdminImageWidget and AdminImageMixin found in
sorl-thumbnail/sorl/thumbnail/admin/current.py

Customizing here, however, to make them align a little
more nicely in the admin forms.
'''
from django import forms
from django.utils.safestring import mark_safe
from sorl.thumbnail.fields import ImageField
from sorl.thumbnail.shortcuts import get_thumbnail


class AdminImageWidget(forms.ClearableFileInput):
    """
    An ImageField Widget for django.contrib.admin that shows
    a thumbnailed image and link to the current file.
    """

    template_with_initial = u'%(clear_template)s<div style="display: block; clear: both; margin-top: 10px;">%(input_text)s:<br/>%(input)s</div>'
    template_with_clear = u'%(clear)s <label style="width:auto" for="%(clear_checkbox_id)s">%(clear_checkbox_label)s</label>'

    def render(self, name, value, attrs=None):
        output = super(AdminImageWidget, self).render(name, value, attrs)
        if value and hasattr(value, 'url'):
            try:
                mini = get_thumbnail(value, 'x80', upscale=False)
            except Exception:
                pass
            else:
                output = (
                    u'<div style="float:left">'
                    u'<a style="width:%spx;display:block;margin:0 0 10px" class="thumbnail" target="_blank" href="%s">'
                    u'<img src="%s"></a>%s</div>'
                    ) % (mini.width, value.url, mini.url, output)
        return mark_safe(output)


class AdminImageMixin(object):
    """
    This is a mix-in for InlineModelAdmin subclasses to make ``ImageField``
    show nicer form widget
    """
    def formfield_for_dbfield(self, db_field, **kwargs):
        if isinstance(db_field, ImageField):
            return db_field.formfield(widget=AdminImageWidget)
        sup = super(AdminImageMixin, self)
        return sup.formfield_for_dbfield(db_field, **kwargs)

