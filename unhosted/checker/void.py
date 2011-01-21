from zope import interface
import unhosted.interfaces

class VoidChecker(object):
    """Registration checker that always succeeds."""

    interface.implements(unhosted.interfaces.IRegistrationChecker)

    def check(self, account):
        """Mark account as checked."""
        if not unhosted.interfaces.IAccount.providedBy(account):
            raise TypeError("1st parameter should provide IAccount")
        pass # TODO
