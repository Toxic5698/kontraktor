from django.contrib.auth.models import User
from django.db import transaction
from django.utils import timezone

from contracts.models import Contract, Protocol, ProtocolItem
from tests.factories import ProposalFactory, ItemFactory


def create_demo_client():
    user = User.objects.get(username="Aneta Demová")

    # create client and proposal
    proposal = ProposalFactory.create(created_by=user)

    # create items
    for i in range(5):
        ItemFactory.create(proposal=proposal, created_by=user)

    # edit payments
    first_payment = proposal.payments.get(part=100)
    second_payment = proposal.payments.filter(part=0).last()
    if proposal.contract_type.type == "DILO":
        due = "32"
    else:
        due = "31"

    with transaction.atomic():
        first_payment.part = 60
        second_payment.part = 40
        second_payment.due = due
        first_payment.save()
        second_payment.save()
    proposal.save()

    # create contract
    contract = Contract.objects.create(
        proposal=proposal,
        document_number=proposal.document_number + "C",
        client=proposal.client,
        created_by=user,
        contract_type=proposal.contract_type,
        contract_subject=proposal.contract_subject,
    )

    # create protocols
    protocol = Protocol.objects.create(
        document_number=proposal.document_number + "P",
        contract=contract,
        client=proposal.client,
        note=f"{timezone.now().strftime('%d. %m. %Y %H:%M')} - předáno vše bez výhrad, zákazník spokojen a pochválil práci",
        created_by=user
    )
    for item in proposal.items.all():
        ProtocolItem.objects.create(
            protocol=protocol,
            item=item,
            description="",
            note="bez vad",
            status="yes",
            created_by=user
        )

    return proposal.client.sign_code
