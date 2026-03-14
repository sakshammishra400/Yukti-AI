import fitz

def fill_passport_form(data):

    template = "forms/passport_template.pdf"

    doc = fitz.open(template)

    page = doc[0]

    page.insert_text((100,200), data["name"])
    page.insert_text((100,250), data["address"])

    output = "forms/filled_passport.pdf"

    doc.save(output)

    return output