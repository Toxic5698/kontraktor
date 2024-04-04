from django.apps.registry import apps

from clients.models import Client


def get_data_in_dict(request):
    data = request.POST.dict()
    data.pop('csrfmiddlewaretoken')
    return data


def get_model(model_name):
    if model_name.lower() == "proposal":
        app_label = "proposals"
    else:
        app_label = "contracts"
    model = apps.get_model(model_name=model_name, app_label=app_label)
    return model


def get_documents_for_client(client_id=None, sign_code=None):
    if client_id:
        client = Client.objects.prefetch_related("proposals", "contracts", "protocols").get(id=client_id)
    elif sign_code:
        client = Client.objects.prefetch_related("proposals", "contracts", "protocols").get(sign_code=sign_code)
    documents = []
    for proposal in client.proposals.all():
        documents.append(proposal)
    for contract in client.contracts.all():
        documents.append(contract)
    for protocol in client.protocols.all():
        documents.append(protocol)
    return client, documents
