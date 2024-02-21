from django.urls import path
from emailing.views import *

urlpatterns = [
    path("<int:pk>/", ClientMailManageView.as_view(), name="client-mail-list"),
    path("create-mail/<int:client_id>/", MailCreateView.as_view(), name="create-mail"),
    path("delete-mail/<int:pk>/", MailDeleteView.as_view(), name="delete-mail"),
    path("edit-mail/<int:mail_id>/", MailCreateView.as_view(), name="edit-mail"),
    path("add-document/<int:mail_id>/", MailCreateView.as_view(), name="add-mail-document"),
    path("add-note/<int:mail_id>/", MailCreateView.as_view(), name="add-mail-note"),
    path("change-receiver/<int:mail_id>/", MailCreateView.as_view(), name="change-receiver"),
    path("change-subject/<int:mail_id>/", MailCreateView.as_view(), name="change-subject"),
    path("preview/<int:mail_id>/", MailPreviewView.as_view(), name="preview-mail"),
    path("send-mail/<int:mail_id>/", MailPreviewView.as_view(), name="send-mail"),
]
