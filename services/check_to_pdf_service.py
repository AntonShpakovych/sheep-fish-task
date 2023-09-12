class CheckToPDFService:
    @classmethod
    def generate_pdf(cls, check):
        pass

    @classmethod
    def is_already_exist(cls, check):
        return check.status != "new"
