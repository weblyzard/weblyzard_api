from deprecated import deprecated
from weblyzard_api.client.triplestore.blazegraph import BlazegraphWrapper as NewBlazegraphWrapper

@deprecated(reason="Class was moved, use triplestore.blazegraph")
class DeprecationHelperBlazegraphWrapper(object):

    def __init__(self, new_target):
        self.new_target = new_target

    def __call__(self, *args, **kwargs):
        return self.new_target(*args, **kwargs)

    def __getattr__(self, attr):
        return getattr(self.new_target, attr)


BlazegraphWrapper = DeprecationHelperBlazegraphWrapper(NewBlazegraphWrapper)
