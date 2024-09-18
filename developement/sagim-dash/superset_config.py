from superset.security import SupersetSecurityManager

class NoAuthSecurityManager(SupersetSecurityManager):
    def is_authentication_enabled(self):
        return False

CUSTOM_SECURITY_MANAGER = NoAuthSecurityManager
DEFAULT_HOME_PAGE = '/superset/dashboard/1/'
