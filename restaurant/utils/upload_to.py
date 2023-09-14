import os


def pdf_path(instance, filename: str) -> str:
    """
    Generate the file path for a PDF associated with a Check instance.

    This function is used to generate the file path for a PDF
    file that is associated with a Check instance.
    The file path is constructed based on the Check's ID and type.

    :param instance: The Check instance for which the PDF file path is generated. # noqa: 501
    :type instance: Check
    :param filename: The original filename of the PDF file.
    :type filename: str
    :return: The generated file path for the PDF.
    :rtype: str
    """
    _, extension = os.path.splitext(filename)
    return os.path.join(
        "pdf/",
        f"{instance.id}_{instance.type}"
    )
