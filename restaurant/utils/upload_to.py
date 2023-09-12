import os


def pdf_path(instance, filename):
    _, extension = os.path.splitext(filename)
    return os.path.join(
        "pdf//",
        f"{instance.id}_{instance.type}"
    )
