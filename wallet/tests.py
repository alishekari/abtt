from wallet.models import CheckoutRequest
from wallet.services.checkout_request_services import CheckoutRequestServices

c = CheckoutRequest.objects.get(id=12)

CheckoutRequestServices(checkout_request=c).pay_checkout_request_by_toman(admin_id=1)