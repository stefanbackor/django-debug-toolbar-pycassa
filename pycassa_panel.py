from django.template import Template, Context
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from debug_toolbar.panels import Panel

import pycassa_tracker as tracker

SUBTITLE_TEMPLATE = u"""
{% for o, n, t in operations %}
    {{ n }} {{ o }}{{ n|pluralize }} in {{ t }}ms<br/>
    {% if forloop.last and forloop.counter0 %}
        {{ count }} operation{{ count|pluralize }} in {{ time }}ms
    {% endif %}
{% endfor %}
"""

class PycassaDebugPanel(Panel):
    name = 'Pycassa'
    has_content = True
    template = 'pycassa-panel.html'

    def __init__(self, *args, **kwargs):
        super(PycassaDebugPanel, self).__init__(*args, **kwargs)
        tracker.install_tracker()

    def nav_title(self):
        return _('Pycassa')

    def nav_subtitle(self):
        fun = lambda x, y: (x, len(y), '%.2f' % sum(z['time'] for z in y))
        ctx = {'operations': [], 'count': 0, 'time': 0}
        
        if tracker.queries:
            ctx['operations'].append(fun('read', tracker.queries))
            ctx['count'] += len(tracker.queries)
            ctx['time'] += sum(x['time'] for x in tracker.queries)
        
        if tracker.inserts:
            ctx['operations'].append(fun('insert', tracker.inserts))
            ctx['count'] += len(tracker.inserts)
            ctx['time'] += sum(x['time'] for x in tracker.inserts)
        
        if tracker.removes:
            ctx['operations'].append(fun('remove', tracker.removes))
            ctx['count'] += len(tracker.removes)
            ctx['time'] += sum(x['time'] for x in tracker.removes)
        
        ctx['time'] = '%.2f' % ctx['time']
        
        return mark_safe(Template(SUBTITLE_TEMPLATE).render(Context(ctx)))

    def title(self):
        return _('Pycassa NoSQL Operations')

    def url(self):
        return ''

    def process_request(self, request):
        tracker.reset()

    def process_response(self, request, response):
        self.record_stats({
            'queries': tracker.queries,
            'batches': tracker.batches,
            'inserts': tracker.inserts,
            'removes': tracker.removes
        })