from django.forms import EmailInput, NumberInput, PasswordInput, Textarea, TextInput, URLInput
from django.utils.safestring import mark_safe

from .core import get_bootstrap_setting, get_field_renderer, get_form_renderer, get_formset_renderer
from .css import merge_css_classes
from .exceptions import BootstrapError
from .html import render_tag
from .size import DEFAULT_SIZE, SIZE_MD, get_size_class

WRAPPER_CLASS = ""
WRAPPER_TAG = "div"


def render_formset(formset, **kwargs):
    """Render a formset to a Bootstrap layout."""
    renderer_cls = get_formset_renderer(**kwargs)
    return renderer_cls(formset, **kwargs).render()


def render_formset_errors(formset, **kwargs):
    """Render formset errors to a Bootstrap layout."""
    renderer_cls = get_formset_renderer(**kwargs)
    return renderer_cls(formset, **kwargs).render_errors()


def render_form(form, **kwargs):
    """Render a form to a Bootstrap layout."""
    renderer_cls = get_form_renderer(**kwargs)
    return renderer_cls(form, **kwargs).render()


def render_form_errors(form, type="all", **kwargs):
    """Render form errors to a Bootstrap layout."""
    renderer_cls = get_form_renderer(**kwargs)
    return renderer_cls(form, **kwargs).render_errors(type)


def render_field(field, **kwargs):
    """Render a field to a Bootstrap layout."""
    renderer_cls = get_field_renderer(**kwargs)
    return renderer_cls(field, **kwargs).render()


def render_label(content, label_for=None, label_class=None, label_title=""):
    """Render a label with content."""
    attrs = {}
    if label_for:
        attrs["for"] = label_for
    if label_class:
        attrs["class"] = label_class
    if label_title:
        attrs["title"] = label_title
    return render_tag("label", attrs=attrs, content=content)


def render_button(
    content,
    button_type=None,
    button_class="btn-primary",
    button_outline=False,
    size="",
    href="",
    name=None,
    value=None,
    title=None,
    extra_classes="",
    id="",
):
    """Render a button with content."""
    attrs = {}
    size_class = get_size_class(size, prefix="btn", skip=SIZE_MD, default=DEFAULT_SIZE)
    classes = merge_css_classes("btn", button_class, size_class)

    if button_type:
        if button_type not in ("submit", "reset", "button", "link"):
            raise BootstrapError(
                (
                    'Parameter "button_type" should be "submit", "reset", "button", "link" or empty '
                    '("{button_type}" given).'
                ).format(button_type=button_type)
            )
        if button_type != "link":
            attrs["type"] = button_type

    classes = merge_css_classes(classes, extra_classes)
    attrs["class"] = classes

    if href:
        tag = "a"
        if button_type and button_type != "link":
            raise BootstrapError(
                'Button of type "{button_type}" is not allowed a "href" parameter.'.format(button_type=button_type)
            )
        attrs["href"] = href
        # Specify role for link with button appearance
        attrs.setdefault("role", "button")
    else:
        tag = "button"

    if id:
        attrs["id"] = id
    if name:
        attrs["name"] = name
    if value:
        attrs["value"] = value
    if title:
        attrs["title"] = title
    return render_tag(tag, attrs=attrs, content=mark_safe(content))


def render_field_and_label(field, label, field_class="", label_for=None, label_class="", layout="", **kwargs):
    """Render a field with its label."""
    if layout == "horizontal":
        if not label_class:
            label_class = get_bootstrap_setting("horizontal_label_class")
        if not field_class:
            field_class = get_bootstrap_setting("horizontal_field_class")
        if not label:
            label = mark_safe("&#160;")
        label_class = merge_css_classes(label_class, "control-label")
    html = field
    if field_class:
        html = '<div class="{field_class}">{html}</div>'.format(field_class=field_class, html=html)
    if label:
        html = render_label(label, label_for=label_for, label_class=label_class) + html
    return html


def render_form_group(content, css_class=WRAPPER_CLASS):
    """Render a Bootstrap form group."""
    return '<div class="{css_class}">{content}</div>'.format(css_class=css_class, content=content)


def is_widget_with_placeholder(widget):
    """
    Return whether this widget should have a placeholder.

    Only text, text area, number, e-mail, url, password, number and derived inputs have placeholders.
    """
    return isinstance(widget, (TextInput, Textarea, NumberInput, EmailInput, URLInput, PasswordInput))
