from proposals.models import Item
import pypdfium2 as pdfium


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
    for part in first_split:
        # sanitizing text in part from splitters and redundant characters
        part = part.replace("\n", " ")
        part = part.replace("\t", " ")
        part = part.replace("\r", " ")
        part = part.replace("  ", " ")
        part = part.replace("  ", " ")
        part = part.strip(" ")
        # print(part)

        # TODO: split with regex
        priority, code, quantity, price, data = part.split(" ", maxsplit=4)

        item, created = Item.objects.update_or_create(
            priority=priority,
            proposal=proposal,
            defaults={
                "title": code,
                "production_price": price,
                "quantity": int(quantity.split(".")[0]),
                "from_upload": True,
            }
        )

    return "success"
