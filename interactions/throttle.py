from rest_framework.throttling import UserRateThrottle


class CommentRateThrottle(UserRateThrottle):
    rate = '5/min'