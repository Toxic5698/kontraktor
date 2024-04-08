import unittest
from decimal import Decimal

from tests.factories import ProposalFactory
from .models import Proposal, check_payments


class CheckPaymentsTests(unittest.TestCase):

    def setUp(self):
        proposal = ProposalFactory.create()

    def test_no_payments(self):
        proposal = ProposalFactory.create()
        self.assertTrue(check_payments(proposal))
        self.assertEqual(len(proposal.payments.all()), 3)

    def test_invalid_payments(self):
        proposal = Proposal()
        proposal.payments.create(amount=10, part=50)
        self.assertFalse(check_payments(proposal))

    def test_valid_payments(self):
        proposal = Proposal()
        proposal.payments.create(amount=100, part=50)
        proposal.payments.create(amount=100, part=50)
        self.assertTrue(check_payments(proposal))

    def test_update_amounts(self):
        proposal = Proposal(price_brutto=200)
        proposal.payments.create(amount=100, part=50)
        proposal.payments.create(amount=100, part=50)
        check_payments(proposal)
        self.assertEqual(proposal.payments.first().amount, Decimal(100))
