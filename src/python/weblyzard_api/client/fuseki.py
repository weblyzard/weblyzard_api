from deprecated import deprecated
from weblyzard_api.client.triplestore.fuseki import FusekiWrapper as NewFusekiWrapper


@deprecated(reason="Class was moved, use triplestore.fuseki")
class DeprecationHelperFusekiWrapper(object):

    def __init__(self, new_target):
        self.new_target = new_target

    def __call__(self, *args, **kwargs):
        return self.new_target(*args, **kwargs)

    def __getattr__(self, attr):
        return getattr(self.new_target, attr)


FusekiWrapper = DeprecationHelperFusekiWrapper(NewFusekiWrapper)
