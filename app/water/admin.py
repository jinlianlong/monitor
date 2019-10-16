# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Water, Alert
# Register your models here.

admin.site.register(Water)
admin.site.register(Alert)