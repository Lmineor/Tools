from werkzeug.exceptions import HTTPException, Forbidden


class ToolsBaseError(Exception):
    """Root exception for tools"""
    description = "An internal error has occured"
    
    def __init__(self, msg=None):
        self.msg = msg
        
    def __str__(self):
        if self.msg is None:
            return self.description
        return self.msg


class AuthorizationRequired(ToolsBaseError, Forbidden):
    description = "Authorization is required."


class ConfigFileNotFoundError(ToolsBaseError):
    """Raised if config file  does not exist"""
    def __init__(self, config_dir):
        self.config_dir = config_dir
    
    def __str__(self):
        return ('Failed to load config file in the directory: %s' % self.config_dir)


class NoSuchGroupError(ToolsBaseError, AttributeError):
    """Raised if config does not has such group"""
    def __init__(self, group_name):
        self.group_name = group_name

    def __str__(self):
        return "no such group [%s]" % self.group_name


class NoSuchOptError(ToolsBaseError, AttributeError):
    """Raised if config does not has such option"""
    def __init__(self, opt_name, group):
        self.opt_name = opt_name
        self.group = group

    def __str__(self):
        return "no such option %s in group [%s]" % (self.opt_name, self.group)

class InvaildOption(ToolsBaseError):
    def __init__(self, k, v):
        self.k = k
        self.v = v
    
    def __str__(self):
        return "The group name [%s] or option %s is invalid" % (self.k, self.v)

class PoemNotFound(ToolsBaseError, HTTPException):
    description = "The poem you refer does not exist, check your input"
    code = 404
    response = 404
    
    
class FilterInvaild(ToolsBaseError):
    def __init__(self, filters):
        self.filters = filters
        
    def __str__(self):
        return "The filter %s you refer is invalid!" % ','.join(self.filters)

class FiltersTypeError(ToolsBaseError):
    description = "Filters must be the type of `list`"