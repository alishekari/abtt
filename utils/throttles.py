from rest_framework.throttling import AnonRateThrottle


class PublicAPIThrottle(AnonRateThrottle):
    rate = '2/min'
