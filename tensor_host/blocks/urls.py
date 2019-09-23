from django.urls import path

from blocks.views import BlockProfileEdit
from tensor_host.blocks.views import Blocks, BlockProfile

urlpatterns = [
    path('', Blocks.as_view()),
    path('form/', BlockProfile.as_view(), name="block_form"),
    path('form/<int:part_number>', BlockProfileEdit.as_view(), name="block_form_edit")
]
