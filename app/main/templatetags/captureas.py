"""
The captureas template tag enables output within a region
to be captured into a context variable.

Example:
    {% captureas title %}
      {% block title %}{% endblock %}
    {% endcaptureas %}

This will capture the "title" block into a context
variable also named "title" to allow the content to be
output multiple times.
"""

from django import template

register = template.Library()


@register.tag(name='captureas')
def do_captureas(parser, token):
    try:
        tag_name, args = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError(
            "'captureas' node requires a variable name.")
    nodelist = parser.parse(('endcaptureas',))
    parser.delete_first_token()
    return CaptureasNode(nodelist, args)


class CaptureasNode(template.Node):
    def __init__(self, nodelist, varname):
        self.nodelist = nodelist
        self.varname = varname

    def render(self, context):
        output = self.nodelist.render(context)
        context[self.varname] = output
        return ''
