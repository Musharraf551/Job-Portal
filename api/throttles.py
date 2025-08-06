from rest_framework.throttling import UserRateThrottle

class JobApplyRateThrottle(UserRateThrottle):
    scope = 'apply_job'