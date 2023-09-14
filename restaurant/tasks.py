import logging
from typing import List
import base64
import json
import requests

from django.conf import settings
from django.template.loader import render_to_string

from config.celery import app

from restaurant.models import Check
from restaurant.utils.choices import CheckStatusChoices

from services.print_check_pdf_service import PrintCheckPDFService


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)


@app.task()
def produce_check_pdf(pk: int) -> None:
    """
    Generate a PDF file for a Check instance and save it.

    This Celery task generates a PDF file for the
    specified Check instance, renders its content
    from an HTML template, sends it to an external
    service (e.g., Wkhtmltopdf), and saves the resulting PDF file.

    :param pk: The primary key of the Check instance for which to generate a PDF. # noqa: 501
    :type pk: int
    :raises Check.DoesNotExist: If the Check instance with the specified primary key does not exist. # noqa: 501
    """
    check = Check.objects.get(pk=pk)

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


@app.task(bind=True, max_retries=3, soft_time_limit=300)
def produce_print(self, check_ids: List[int]) -> None:
    """
    Print PDFs for a list of Check instances.

    This Celery task is responsible for printing PDFs
    for a list of Check instances specified by their IDs.
    It retrieves each Check, prepares it for printing
    using PrintCheckPDFService, updates its status,
    and saves the Check.

    :param self: The Celery task instance.
    :type self: Task
    :param check_ids: A list of Check IDs to print.
    :type check_ids: List[int]
    :raises self.retry: If an exception occurs during printing, the task is retried up to the maximum retries. # noqa: 501
    """
    try:
        for check_id in check_ids:
            check = Check.objects.select_related(
                "printer"
            ).get(id=check_id)

            printer = PrintCheckPDFService(
                printer=check.printer,
                path_to_check=check.pdf_file.path
            )
            printer.print_pdf()

            check.status = CheckStatusChoices.PRINTED
            check.save()
    except Exception as e:
        raise self.retry(exc=e)
