import re
from datetime import datetime
from decimal import Decimal

import pypdfium2 as pdfium
import sentry_sdk

from proposals.models import Item


def parse_items(file, proposal):
    uploaded_proposal_text = ""
    pdf = pdfium.PdfDocument(file)
    for page in pdf:
        text = page.get_textpage().get_text_range()
        uploaded_proposal_text += text

    first_split = uploaded_proposal_text.split(
        "-------------------------------------------------------------------------------------------"
    )
    header = first_split.pop(0)
    footer = first_split.pop(-1)

    # change priority of existing items
    imported_items_count = len(first_split)
    if proposal.items.all().count() > 0 and proposal.items.all().count() != imported_items_count:
        for item in proposal.items.all():
            item.priority += imported_items_count
            item.save()

    # creating imported items
    for part in first_split:
        # sanitizing text in part from splitters and redundant characters
        part = re.sub("\*{3}.+|=+|Řádek Výrobek Množství Mj Cena/sleva DPH Cena celkem Rok/týden/ datum", " ", part)
        part = re.sub("\s+", " ", part)

        pattern = r"(\d+)\s([A-Z0-9-]+)\s(\d+\.\d+ks)\s(\d+(?:\s\d+)?\.\d+)\s%\s(\d+(?:\s\d+)?\.\d+)\s(\d{4}/\d{2}/(?:\s?\d{1,2}\.\d{2}\.\d{4}|\d{1,2}))\s(.+)\s(\d+\.\d+-%)\s(\d+)\s(.+)"
        matches = re.findall(pattern, part)

        if matches:
            (
                priority,
                description,
                quantity,
                price_without_sale,
                price_with_sale,
                production_date,
                title,
                sale,
                number,
                production_data,
            ) = matches[0]
            item, created = Item.objects.update_or_create(
                priority=int(priority),
                proposal=proposal,
                defaults={
                    "title": title,
                    "description": description,
                    "production_price": 0,
                    "price_per_unit": Decimal(float(price_without_sale)),
                    "sale_discount": int(sale.split(".")[0]),
                    "quantity": int(quantity.split(".")[0]),
                    "from_upload": True,
                    "production_data": production_data,
                    "production_date": datetime.strptime(production_date.split("/")[2], "%d.%m.%Y").date(),
                },
            )

        else:
            sentry_sdk.capture_message(f"Matching error during import items from file {file}, data: {part}")

    return "success"
