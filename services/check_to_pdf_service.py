from restaurant.models import Check
from restaurant.tasks import produce_check_pdf
from restaurant.utils.choices import CheckStatusChoices


class CheckToPDFService:
    """
    Service for generating  PDF files for checks
    """
    @classmethod
    def generate_pdf(cls, pk: int):
        """
        Generate a PDF for the given Check asynchronously through Celery.

        This method initiates the generation of a PDF
        for the specified Check by scheduling a background task.

        :param pk: The primary key of the Check for which to generate a PDF.
        :type pk: int
        """
        produce_check_pdf.delay(pk=pk)

    @classmethod
    def is_file_already_exist(cls, check: Check) -> bool:
        """
        Check if a PDF file already exists for the given Check.

        This method checks the status of the Check
        to determine if a PDF file has already been generated.

        :param check: The Check instance to check for the existence of a PDF file. # noqa: 501
        :type check: Check
        :return: True if a PDF file exists, False otherwise.
        :rtype: bool
        """
        return check.status != CheckStatusChoices.NEW
