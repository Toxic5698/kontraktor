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
        "-------------------------------------------------------------------------------------------")
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
            priority, description, quantity, price_without_sale, price_with_sale, production_date, title, sale, number, production_data = matches[0]
            item, created = Item.objects.update_or_create(
                priority=int(priority),
                proposal=proposal,
                defaults={
                    "title": title,
                    "description": description,
                    "production_price": Decimal(float(price_without_sale)),
                    "price_per_unit": Decimal(float(price_without_sale)),
                    "sale_discount": int(sale.split(".")[0]),
                    "quantity": int(quantity.split(".")[0]),
                    "from_upload": True,
                    "production_data": production_data,
                    "production_date": datetime.strptime(production_date.split("/")[2], '%d.%m.%Y').date()
                }
            )

        else:
            sentry_sdk.capture_message(f"Matching error during import items from file {file}, data: {part}")

    return "success"

# 7 DOPRAVA 1.00ks 1000.00 % 980.00 2022/40/ 7.10.2022 DOPRAVA 2.00-% 000 000 Dodání a manipulace - prahy
# 1 VD100-0000113 1.00ks 30529.00 % 28 391.97 2022/51/20.12.2022 D+Z+K Elegant K 10 OKZ-No-ost TORRES hra 7.00-% 916 D+Z+K Elegant K 10 OKZ-No-ost TORRES hra 916 1245x1960 ss.110 mm P Česká 1245x1960 Vstup kino Druh V100-VD V100-VD Komplet Dveře+zárubeň V100-VD Dveře+zárubeň Stupeň zatížení+polo Byt.s polodr.dř.zár. Byt.s polodr.dř.zár. Odolnost Rw 32 dB Byt.s polodr.dř.zár. Rw 32 dB Typ obložky / zárubn OKZ-Normal-ostrá OKZ-Normal-ostrá Počet křídel Dvoukřídlové OKZ-Normal-ostrá Dvoukřídlové Modelová řada 1 Elegant Komfort Elegant Komfort Model 1 10 Elegant Komfort Povrch 1 HPL Bílá perla HPL Bílá perla Z Povrch A (1) HPL Bílá perla HPL Bílá perla HPL Bílá perla Objednací šířka 1245 Šířka hlavního křídl 875 1245 875 Z Síla stěny 110 mm Orientace dveří Pravé 110 mm Pravé Norma Česká Objednací výška 1960 Česká 1960 Typ závěsu TUKAN SATÉN TUKAN SATÉN Typ zámku KOMFORT Vložkový TUKAN SATÉN KOMFORT Vložkový Z Typ protiplechu Stand. SATÉN Stand. SATÉN Provedení hrany O3 Stand. SATÉN Povrch hrany ABS 05 Bílá perla ABS 05 Bílá perla PÚ+barva povrchu 1 Upraveno ABS 05 Bílá perla Upraveno Z PÚ+barva povrchu A Upraveno Upraveno Z Šířka obložky A 50 mm Upraveno 50 mm Z Šířka obložky B 75 mm Z Barva těsnění bílá 75 mm bílá Typ mechanického pra Zvukově izolační Zvukově izolační MK Dodavatel kování SAPELI Zvukově izolační SAPELI MK Název kování TORRES hranatá TORRES hranatá MK Povrch kování NEREZ BROUŠENÝ TORRES hranatá NEREZ BROUŠENÝ MK Provedení KLIKA/KLIKA PZ KLIKA/KLIKA PZ MK Tloušťka dveří 42 mm KLIKA/KLIKA PZ 42 mm Vložka FAB3 30+35 NI FAB3 30+35 NI
# ===========================================================================================
