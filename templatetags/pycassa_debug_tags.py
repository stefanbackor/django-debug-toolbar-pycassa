from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _

import json
import pprint
import os

register = template.Library()

@register.inclusion_tag('pycassa-panel-stack-trace.html')
def stack_trace_table(stack_trace, forloop_counter):
    return {"stack_trace": stack_trace, "forloop_counter": forloop_counter}

@register.filter
def format_stack_trace(value):
    stack_trace = []
    fmt = (
        '<span class="path">{0}/</span>'
        '<span class="file">{1}</span> in <span class="func">{3}</span>'
        '(<span class="lineno">{2}</span>) <span class="code">{4}</span>'
    )
    for frame in value:
        params = map(escape, frame[0].rsplit('/', 1) + list(frame[1:]))
        stack_trace.append(fmt.format(*params))
    return mark_safe('\n'.join(stack_trace))

@register.filter
def embolden_file(path):
    head, tail = os.path.split(escape(path))
    return mark_safe(os.sep.join([head, '<strong>{0}</strong>'.format(tail)]))

@register.filter
def format_dict(value, width=60):
    return pprint.pformat(value, width=int(width))

@register.filter
def format_value(value):
    try:
        # Try extract json value
        value = json.loads(value)
    except (TypeError, ValueError), e:
        pass
        
    if isinstance(value, (basestring, int, float)):
        # Return one dimensional values
        return value
    
    # Try building dict out of other values
    try:
        value = dict(value.items())
        for k, v in value.items():
            try:
                value[k] = unicode(v, encoding="utf8", errors="replace").encode("utf-8")
            except TypeError, e:
                value[k] = v.encode("utf-8")
    except Exception, e:
        pass
    
    # For pretty print purposes lets convert to json
    try:
        output = json.dumps(value, sort_keys=True, indent=4)
    except (TypeError, ValueError), e:
        output = _("Unable to load value")
    return output

@register.filter
def highlight(value, language):
    try:
        from pygments import highlight
        from pygments.lexers import get_lexer_by_name
        from pygments.formatters import HtmlFormatter
    except ImportError:
        return value
    # Can't use class-based colouring because the debug toolbar's css rules
    # are more specific so take precedence
    formatter = HtmlFormatter(style='friendly', nowrap=True, noclasses=True)
    return highlight(value, get_lexer_by_name(language), formatter)