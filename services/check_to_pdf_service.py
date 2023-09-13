from restaurant.tasks import produce_check_pdf
from restaurant.utils.choices import CheckStatusChoices


class CheckToPDFService:
    @classmethod
    def generate_pdf(cls, check_id):
        produce_check_pdf.delay(check_id)

    @classmethod
    def is_file_already_exist(cls, check):
        return check.status != CheckStatusChoices.NEW
