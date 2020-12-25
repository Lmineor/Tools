from werkzeug.exceptions import HTTPException, Forbidden


class ToolsBaseError(Exception):
    """Root exception for """
    pass


class ToolsHTTPError(ToolsBaseError, HTTPException):
    description = "An internal error has occured"


ToolsError = ToolsHTTPError


class AuthorizationRequired(ToolsError, Forbidden):
    description = "Authorization is required."


class AuthenticationError(ToolsError):
    description = "Invalid username and password combination."


# Config Error
class ConfigBaseError(Exception):
    def __init(self, msg):
        self.msg = msg
        
    def __str__(self):
        return self.msg


class ConfigFileNotFoundError(ConfigBaseError):
    """Raised if config file  does not exist"""
    def __init__(self, config_dir):
        self.config_dir = config_dir
    
    def __str__(self):
        return ('Failed to read config file directory: %s' % self.config_dir)


class NoSuchGroupError(ConfigBaseError):
    """Raised if config does not has such group"""
    def __init__(self, group_name):
        self.group_name = group_name

    def __str__(self):
        return "no such group [%s]" % self.group_name


class NoSuchOptError(ConfigBaseError, AttributeError):
    """Raised if config does not has such option"""
    def __init__(self, opt_name, group=None):
        self.opt_name = opt_name
        self.group = group

    def __str__(self):
        group_name = "DEFAULT" if self.group is None else self.group.name
        return "no such option %s in group [%s]" % (self.opt_name, group_name)
    
    
class ConfigFileValueError(ConfigBaseError, ValueError):
    """Raised if a config file value does not match its opt type"""
    pass


class InvaildOption(ConfigBaseError):
    pass