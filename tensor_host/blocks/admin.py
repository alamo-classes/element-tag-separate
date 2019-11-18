""" Add the Block's model to the admin section """
from django.contrib import admin
from blocks.models import BlockCatalog

admin.site.register(BlockCatalog)
