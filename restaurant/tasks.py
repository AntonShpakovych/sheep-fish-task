import base64
import json
import requests

from django.conf import settings
from django.template.loader import render_to_string

from config.celery import app

from restaurant.models import Check
from restaurant.utils.choices import CheckStatusChoices


@app.task()
def produce_check_pdf(check_id):
    check = Check.objects.get(id=check_id)
    html_string = render_to_string(
        "check.html",
        {"check": check}
    )
    html_binary = base64.b64encode(bytes(html_string, "utf-8"))
    data = {
        "contents": html_binary.decode("utf-8"),
    }
    headers = {
        "Content-Type": "application/json",
    }
    response = requests.post(
        settings.URL_TO_WKHTMLTOPDF,
        data=json.dumps(data),
        headers=headers
    )
    path_to_dir = f"{settings.MEDIA_ROOT}/pdf"
    file_name = f"{check.id}_{check.type}.pdf"
    full_path = f"{path_to_dir}/{file_name}"

    with open(full_path, "wb") as pdf_file:
        pdf_file.write(response.content)

    check.pdf_file = full_path
    check.status = CheckStatusChoices.RENDERED
    check.save()
