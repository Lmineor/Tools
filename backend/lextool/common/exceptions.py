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


class ParseError(Exception):
    def __init__(self, message, lineno, line):
        self.msg = message
        self.line = line
        self.lineno = lineno

    def __str__(self):
        return 'at line %d, %s: %r' % (self.lineno, self.msg, self.line)


class ConfigFileNotFoundError(Exception):
    def __init__(self, config_dir):
        self.config_dir = config_dir
    
    def __str__(self):
        return ('Failed to read config file directory: %s' % self.config_dir)
    
    
class ConfigOptionCanNotBeAssigned(Exception):
    def __init__(self, config_op):
        self.config_op = config_op
        
    def __str__(self):
        return ("Failed to assign config options: %s " % self.config_op)
    
class InvaildOption(ValueError):
    def __init__(self, section, option):
        self.option = option
        self.section = section
        
    def __str__(self):
        return ("Invalid config options <%s: %s>, check it" % (self.section, self.option))