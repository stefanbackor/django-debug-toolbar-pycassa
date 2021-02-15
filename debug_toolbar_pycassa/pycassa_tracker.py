import functools
import time
import inspect
import os

import six

import pycassa

import django
from django.conf import settings

_original_methods = {
    'multiget': pycassa.columnfamily.ColumnFamily.multiget,
    'xget': pycassa.columnfamily.ColumnFamily.xget,
    'get': pycassa.columnfamily.ColumnFamily.get,
    'get_range': pycassa.columnfamily.ColumnFamily.get_range,
    'multiget_count': pycassa.columnfamily.ColumnFamily.multiget_count,
    'get_count': pycassa.columnfamily.ColumnFamily.get_count,
    'insert': pycassa.columnfamily.ColumnFamily.insert,
    'batch_insert': pycassa.columnfamily.ColumnFamily.batch_insert,
    'add': pycassa.columnfamily.ColumnFamily.add,
    'remove': pycassa.columnfamily.ColumnFamily.remove,
    'send': pycassa.batch.Mutator.send,
}

queries = []
batches = []
inserts = []
removes = []

WANT_STACK_TRACE = getattr(settings, 'DEBUG_TOOLBAR_PYCASSA_STACKTRACES', True)
def _get_stacktrace():
    if WANT_STACK_TRACE:
        try:
            stack = inspect.stack()
        except IndexError:
            # this is a work around because python's inspect.stack() sometimes fail
            # when jinja templates are on the stack
            return [(
                "",
                0,
                "Error retrieving stack",
                "Could not retrieve stack. IndexError exception occured in inspect.stack(). "
                "This error might occur when jinja2 templates is on the stack.",
            )]
        return _tidy_stacktrace(reversed(stack))
    else:
        return []

@functools.wraps(_original_methods['multiget'])
def _multiget(_self, *args, **kwargs):
    start_time = time.time()
    result = _original_methods['multiget'](
        _self, *args, **kwargs
    )
    total_time = (time.time() - start_time) * 1000
    key = kwargs.get("key", args[0] if len(args) > 0 else None)
    key = key if isinstance(key, (list, tuple)) else [key]
    queries.append({
        'action': 'multiget',
        'keyspace': _self.pool.keyspace,
        'columnfamily': _self.column_family,
        'key': key,
        'columns': kwargs.get("columns", args[1] if len(args) > 1 else None),
        'column_start': kwargs.get("column_start", ""), 
        'column_finish': kwargs.get("column_finish", ""), 
        'column_reversed': kwargs.get("column_reversed", ""), 
        'column_count': kwargs.get("column_count", ""), 
        'data': result, 
        'time': total_time,
        'stack_trace': _get_stacktrace(),
    })
    #   self, keys, columns=None, column_start="", column_finish="",
    #   column_reversed=False, column_count=100, include_timestamp=False,
    #   super_column=None, read_consistency_level=None, buffer_size=None, include_ttl=False
    return result

@functools.wraps(_original_methods['get'])
def _get(_self, *args, **kwargs):
    start_time = time.time()
    result = _original_methods['get'](
        _self, *args, **kwargs
    )
    total_time = (time.time() - start_time) * 1000
    key = kwargs.get("key", args[0] if len(args) > 0 else None)
    key = key if isinstance(key, (list, tuple)) else [key]
    queries.append({
        'action': 'get',
        'keyspace': _self.pool.keyspace,
        'columnfamily': _self.column_family,
        'key': key,
        'columns': kwargs.get("columns", args[1] if len(args) > 1 else None),
        'column_start': kwargs.get("column_start", ""), 
        'column_finish': kwargs.get("column_finish", ""), 
        'column_reversed': kwargs.get("column_reversed", ""), 
        'column_count': kwargs.get("column_count", ""), 
        'data': result, 
        'count': len(result),
        'time': total_time,
        'stack_trace': _get_stacktrace(),
    })
    # def get(self, key, columns=None, column_start="", column_finish="",
    #         column_reversed=False, column_count=100, include_timestamp=False,
    #         super_column=None, read_consistency_level=None, include_ttl=False):
    return result

@functools.wraps(_original_methods['xget'])
def _xget(_self, *args, **kwargs):
    start_time = time.time()
    result = _original_methods['xget'](
        _self, *args, **kwargs
    )
    total_time = (time.time() - start_time) * 1000
    key = kwargs.get("key", args[0] if len(args) > 0 else None)
    key = key if isinstance(key, (list, tuple)) else [key]
    queries.append({
        'action': 'get',
        'keyspace': _self.pool.keyspace,
        'columnfamily': _self.column_family,
        'key': key,
        'column_start': kwargs.get("column_start", ""), 
        'column_finish': kwargs.get("column_finish", ""), 
        'column_reversed': kwargs.get("column_reversed", ""), 
        'column_count': kwargs.get("column_count", ""), 
        'data': result, 
        'count': len(result),
        'time': total_time,
        'stack_trace': _get_stacktrace(),
    })
    # def xget(self, key, column_start="", column_finish="", column_reversed=False,
    #          column_count=None, include_timestamp=False, read_consistency_level=None,
    #          buffer_size=None, include_ttl=False):
    return result

@functools.wraps(_original_methods['get_count'])
def _get_count(_self, *args, **kwargs):
    start_time = time.time()
    result = _original_methods['get_count'](
        _self, *args, **kwargs
    )
    total_time = (time.time() - start_time) * 1000
    key = kwargs.get("key", args[0] if len(args) > 0 else None)
    key = key if isinstance(key, (list, tuple)) else [key]
    queries.append({
        'action': 'get',
        'keyspace': _self.pool.keyspace,
        'columnfamily': _self.column_family,
        'key': key,
        'columns': kwargs.get("columns", args[3] if len(args) > 3 else None),
        'column_start': kwargs.get("column_start", ""), 
        'column_finish': kwargs.get("column_finish", ""), 
        'column_reversed': kwargs.get("column_reversed", ""), 
        'column_count': kwargs.get("column_count", ""), 
        'data': result, 
        'count': result,
        'time': total_time,
        'stack_trace': _get_stacktrace(),
    })
    # def get_count(self, key, super_column=None, read_consistency_level=None,
    #               columns=None, column_start="", column_finish="",
    #               column_reversed=False, max_count=None):
    return result

@functools.wraps(_original_methods['multiget_count'])
def _multiget_count(_self, *args, **kwargs):
    start_time = time.time()
    result = _original_methods['multiget_count'](
        _self, *args, **kwargs
    )
    total_time = (time.time() - start_time) * 1000
    key = kwargs.get("keys", args[0] if len(args) > 0 else None)
    key = key if isinstance(key, (list, tuple)) else [key]
    queries.append({
        'action': 'get',
        'keyspace': _self.pool.keyspace,
        'columnfamily': _self.column_family,
        'key': key,
        'columns': kwargs.get("columns", args[3] if len(args) > 3 else None),
        'column_start': kwargs.get("column_start", ""), 
        'column_finish': kwargs.get("column_finish", ""), 
        'column_reversed': kwargs.get("column_reversed", ""), 
        'column_count': kwargs.get("column_count", ""), 
        'data': result, 
        'count': sum(result.values()),
        'time': total_time,
        'stack_trace': _get_stacktrace(),
    })
    # def multiget_count(self, keys, super_column=None,
    #                    read_consistency_level=None,
    #                    columns=None, column_start="",
    #                    column_finish="", buffer_size=None,
    #                    column_reversed=False, max_count=None):
    return result

@functools.wraps(_original_methods['send'])
def _send(_self, *args, **kwargs):
    start_time = time.time()
    data = _self._buffer
    result = _original_methods['send'](
        _self, *args, **kwargs
    )
    total_time = (time.time() - start_time) * 1000
    batches.append({
        'action': 'batch.send',
        'keyspace': _self.pool.keyspace,
        'columnfamily': list(set([m[1] for m in data])), 
        'data': data, 
        'count': sum([len(m[2]) if isinstance(m[2], (list, tuple,)) else 1 for m in data]),
        'time': total_time,
        'stack_trace': _get_stacktrace(),
    })
    #   self, key, columns=None, column_start="", column_finish="",
    #   column_reversed=False, column_count=100, include_timestamp=False,
    #   super_column=None, read_consistency_level=None, include_ttl=False
    return result

def install_tracker():
    if pycassa.columnfamily.ColumnFamily.multiget != _multiget:
         pycassa.columnfamily.ColumnFamily.multiget = _multiget
    if pycassa.columnfamily.ColumnFamily.get != _get:
         pycassa.columnfamily.ColumnFamily.get = _get
    if pycassa.columnfamily.ColumnFamily.xget != _xget:
         pycassa.columnfamily.ColumnFamily.xget = _xget
    if pycassa.columnfamily.ColumnFamily.get_count != _get_count:
         pycassa.columnfamily.ColumnFamily.get_count = _get_count
    if pycassa.columnfamily.ColumnFamily.multiget_count != _multiget_count:
         pycassa.columnfamily.ColumnFamily.multiget_count = _multiget_count
    if pycassa.batch.Mutator.send != _send:
         pycassa.batch.Mutator.send = _send
    pass

def uninstall_tracker():
    if pycassa.columnfamily.ColumnFamily.multiget == _multiget:
        pycassa.columnfamily.ColumnFamily.multiget = _original_methods['multiget']
    if pycassa.columnfamily.ColumnFamily.get == _get:
        pycassa.columnfamily.ColumnFamily.get = _original_methods['get']
    if pycassa.columnfamily.ColumnFamily.xget == _xget:
        pycassa.columnfamily.ColumnFamily.xget = _original_methods['xget']
    if pycassa.columnfamily.ColumnFamily.get_count == _get_count:
        pycassa.columnfamily.ColumnFamily.get_count = _original_methods['get_count']
    if pycassa.columnfamily.ColumnFamily.multiget_count == _multiget_count:
        pycassa.columnfamily.ColumnFamily.multiget_count = _original_methods['multiget_count']
    if pycassa.batch.Mutator.send == _send:
        pycassa.batch.Mutator.send = _original_methods['send']
    pass

def reset():
    global queries, batches, inserts, removes
    queries = []
    batches = []
    inserts = []
    removes = []


# Taken from Django Debug Toolbar 0.8.6
def _tidy_stacktrace(stack):
    """
    Clean up stacktrace and remove all entries that:
    1. Are part of Django (except contrib apps)
    2. Are part of SocketServer (used by Django's dev server)
    3. Are the last entry (which is part of our stacktracing code)
    ``stack`` should be a list of frame tuples from ``inspect.stack()``
    """
    django_path = os.path.realpath(os.path.dirname(django.__file__))
    django_path = os.path.normpath(os.path.join(django_path, '..'))
    socketserver_path = os.path.realpath(os.path.dirname(six.moves.socketserver.__file__))
    pycassa_path = os.path.realpath(os.path.dirname(pycassa.__file__))

    trace = []
    for frame, path, line_no, func_name, text in (f[:5] for f in stack):
        s_path = os.path.realpath(path)
        # Support hiding of frames -- used in various utilities that provide
        # inspection.
        if '__traceback_hide__' in frame.f_locals:
            continue
        if getattr(settings, 'DEBUG_TOOLBAR_CONFIG', {}).get('HIDE_DJANGO_SQL', True) \
            and django_path in s_path and not 'django/contrib' in s_path:
            continue
        if socketserver_path in s_path:
            continue
        if pycassa_path in s_path:
            continue
        if not text:
            text = ''
        else:
            text = (''.join(text)).strip()
        trace.append((path, line_no, func_name, text))
    return trace
