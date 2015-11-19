# Django Debug Toolbar for Pycassa NoSQL driver
This is an extension panel for Django Debug Toolbar that adds Pycassa's NoSQL stack trace debug to your debug toolbar. [Pycassa](https://github.com/pycassa/pycassa) is Apache Cassandra's python driver. 

### Setup
Modify your `settings.py` Add `debug_toolbar_pycassa` to `INSTALLED_APPS` and `DEBUG_TOOLBAR_PANELS`:

```
INSTALLED_APPS = (
    ...
    'debug_toolbar_pycassa',
)
```

```
DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    
    'debug_toolbar_pycassa.pycassa_panel.PycassaDebugPanel',
    
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
]
```

Based on awesome Harry Marr's [MongoDB panel](https://github.com/hmarr/django-debug-toolbar-mongo)