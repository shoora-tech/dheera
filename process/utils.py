from django.utils import timezone

def get_quotation_number():
    now = timezone.now()
    formatted = now.strftime("%Y-%m-%dT%HH-%MM-%SS")
    return "QT-"+formatted

def get_po_number():
    now = timezone.now()
    formatted = now.strftime("%Y-%m-%dT%HH-%MM-%SS")
    return "PO-"+formatted

def get_co_number():
    now = timezone.now()
    formatted = now.strftime("%Y-%m-%dT%HH-%MM-%SS")
    return "CS-"+formatted

def get_spi_number():
    now = timezone.now()
    formatted = now.strftime("%Y-%m-%dT%HH-%MM-%SS")
    return "CS-"+formatted