class ParseError(Exception):
    def __init__(self, message=None, value=None, line=None, column=None):
        self.value = value
        self.line = line
        self.column = column
        super(ParseError, self).__init__(message)

    def __str__(self):
        if self.line:
            position_info = 'Line %s' % self.line
            if self.column:
                position_info += ', col %s' % self.column
            return '%s: %s' % (position_info, self.message)
        else:
            return self.message


class LexerError(ParseError):
    pass


class SyntaxError(ParseError):
    pass
