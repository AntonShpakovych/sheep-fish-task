from restaurant.utils.choices import CheckStatusChoices


class PrintCheckPDFService:
    def __init__(self, printer, path_to_check):
        self.printer = printer
        self.path_to_check = path_to_check

    def print_pdf(self):
        self.download_check_pdf()
        self.printing()

    def download_check_pdf(self):
        """plug for downloading:
        printer(self.printer) download file.pdf(check)
        """
        pass

    def printing(self):
        """plug for printing: printer(self.printer) print"""
        pass

    @classmethod
    def get_rendered_checks(cls, printer):
        return [
            check.id for check
            in printer.checks.filter(status=CheckStatusChoices.RENDERED)
        ]
