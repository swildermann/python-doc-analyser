import os, sys, site
site.addsitedir('/export/pydoctypes/python-doc-application/local/lib/python3.2/site-packages')
"""

sys.path.append('/export/pydoctypes/python-doc-application/ITIPD')
sys.path.append('/export/pydoctypes/python-doc-application/ITIPD/extractor')

WSGI config for ITIPD project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ITIPD.settings")

activate_env = os.path.expanduser('/export/pydoctypes/python-doc-application/venv/bin/activate_this.py')

#execfile(activate_env, dict(__file__=activate_env))
# ... Instead of execfile(fn) use exec(open(fn).read()).
exec(open(activate_env).read(), dict(__file__=activate_env))

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
