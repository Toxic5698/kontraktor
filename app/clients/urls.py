from django.urls import path

urlpatterns = [
    path("", ClientsTableView.as_view(), name="clients"),
    path("edit/<int:pk>/", ClientEditView.as_view(), name="edit-client"),
    path("create/", ClientCreateView.as_view(), name="create-client"),
    path("delete/<int:pk>/", ClientDeleteView.as_view(), name="delete-client"),
    path("signing/<str:sign_code>/<int:pk>/<str:type>", SigningDocument.as_view(), name="signing-document"),

]
