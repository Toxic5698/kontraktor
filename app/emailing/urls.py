from django.urls import path
from emailing.views import *

urlpatterns = [
    path("<str:pk>/", ClientMailManageView.as_view(), name="client-mail-list"),
    path("create-mail/<str:client_id>/", MailCreateView.as_view(), name="create-mail"),
    path("delete-mail/<str:pk>/", MailDeleteView.as_view(), name="delete-mail"),
    path("edit-mail/<str:mail_id>/", MailCreateView.as_view(), name="edit-mail"),
    path("add-document/<str:mail_id>/", MailCreateView.as_view(), name="add-mail-document"),
    path("add-note/<str:mail_id>/", MailCreateView.as_view(), name="add-mail-note"),
    path("change-receiver/<str:mail_id>/", MailCreateView.as_view(), name="change-receiver"),
    path("change-subject/<str:mail_id>/", MailCreateView.as_view(), name="change-subject"),
    path("preview/<str:mail_id>/", MailPreviewView.as_view(), name="preview-mail"),
    path("send-mail/<str:mail_id>/", MailPreviewView.as_view(), name="send-mail"),
]
