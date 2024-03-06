from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Avg, OuterRef, Subquery, Sum, Count, F, DurationField, ExpressionWrapper
from django.db.models.functions import TruncDate
from django.template.response import TemplateResponse
from django.views.generic import View

from clients.models import Client
from contracts.models import Contract
from proposals.models import Proposal


class ReportsView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        cs = Contract.objects.filter(signed_at__isnull=False)
        context = {
            "clients": Client.objects.all().count(),
            "closed_proposals": Proposal.objects.filter(signed_at__isnull=False).count(),
            "closed_contracts": cs.count(),
            "total_closed_contracts": Proposal.objects.filter(contract__signed_at__isnull=False).aggregate(
                total_closed_contracts=Sum("price_netto"))["total_closed_contracts"],
            "average_protocols_on_contract": get_average_protocols_on_contract(),
            "average_closing_time": get_average_closing_time(),
            "average_proposals_per_day": get_average_proposals_per_day(),
            "top_users_proposals": User.objects.annotate(total_proposals=Count("proposal_created_by")).values('username', 'total_proposals'),
            "top_users_closed_contracts": User.objects.filter(contract_created_by__in=cs).annotate(num_contracts=Count('contract_created_by')).values('username', 'num_contracts'),
            "top_users_protocols": User.objects.annotate(total_protocols=Count("protocol_created_by")).values('username', 'total_protocols'),
        }

        return TemplateResponse(template="reports/reports.html", context=context, request=request)


def get_average_proposals_per_day():
    daily_proposals = Proposal.objects.annotate(date=TruncDate('created_at')).values('date').annotate(count=Count('id')).order_by('date')
    total_days = len(daily_proposals)
    total_proposals = sum(p['count'] for p in daily_proposals)
    avg_per_day = total_proposals / total_days
    return avg_per_day


def get_average_closing_time():
    contracts = Contract.objects.filter(proposal_id=OuterRef('id'))
    proposals = Proposal.objects.annotate(
        c_signed_at=Subquery(contracts.values('signed_at')[:1])
    )
    proposals = proposals.annotate(
        days_until_signed=ExpressionWrapper(
            F('c_signed_at') - F('created_at'), output_field=DurationField()
        )
    )
    avg_days = proposals.aggregate(avg_days=Avg('days_until_signed'))['avg_days']
    return avg_days


def get_average_protocols_on_contract():
    contracts = Contract.objects.annotate(num_protocols=Count('protocols'))
    avg_protocols = contracts.aggregate(avg_num=Avg('num_protocols'))['avg_num']
    return avg_protocols
