from rest_framework.throttling import UserRateThrottle

class QuestionThrottle(UserRateThrottle):
    """
    Custom throttle class for Question API.
    """
    scope = 'question'

    # def allow_request(self, request, view):
    #     new_scope = 'question-' + request.method.lower()

    #     if  new_scope in self.THROTTLE_RATES:
    #         self.scope = new_scope
    #         self.rate = self.get_rate()
    #         self.num_requests, self.duration = self.parse_rate(self.rate)

    #     return super().allow_request(request, view)


class QuestionGetThrottle(UserRateThrottle):
    """
    Alternative to QuestionThrottle class
    Custom throttle class for Question API get requests.
    """
    scope = 'question-get'


class QuestionPostThrottle(UserRateThrottle):
    """
    Alternative to QuestionThrottle class
    Custom throttle class for Question API post requests.
    """
    scope = 'question-post'
