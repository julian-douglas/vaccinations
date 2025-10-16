from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css):
    """Add CSS class to a form field widget."""
    if hasattr(field, 'as_widget'):
        return field.as_widget(attrs={**field.field.widget.attrs, 'class': f"{field.field.widget.attrs.get('class','')} {css}".strip()})
    return field
