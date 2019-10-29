import sys
import os

from django.conf import settings

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

settings.configure(
    DEBUG=True,
    SECRET_KEY='ac!5bu68^vf3_12)m1e&2ls#1uidd_33f)c!j=&&^b_91m7g#+',
    ROOT_URLCONF=__name__,
    MIDDLEWARE_CLASSES=(
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ),
    ALLOWED_HOSTS = [ 'thawing-lowlands-10894.herokuapp.com',
                      'localhost'],
    BASE_DIR = BASE_DIR,
    STATIC_URL = '/static/',
    STATIC_ROOT = os.path.join(BASE_DIR, 'static'),
    TEMPLATES = [{
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [ os.path.join(BASE_DIR, 'templates'), ],
        }],
    INSTALLED_APPS = [ 'django.contrib.staticfiles', ],
)

from django.conf.urls import url
from django.http import HttpResponse
from django.shortcuts import render
from django.template import Context, loader

import subprocess

def batch_r(str_source):
    # call_string = "fakechroot fakeroot chroot /app/.root /usr/bin/"     + R CMD BATCH
    call_string = os.getenv('R_EXEC_STRING', '') + 'R CMD BATCH'
    file_target = os.getenv('R_SCRIPT_FOLDER_PREFIX', '') + str_source
    subprocess.call(call_string + ' ' + file_target, shell=True)

    return None

def index(request):
    batch_r('processMining.R')

    return render(request, 'index.html')

urlpatterns = (
    url(r'^$', index),
)

if __name__ == "__main__":
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)

from django.core.wsgi import get_wsgi_application
from whitenoise.django import DjangoWhiteNoise

application = get_wsgi_application()
application = DjangoWhiteNoise(application)
