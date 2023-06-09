from rply import LexerGenerator


class Lexer():
    def __init__(self):
        self.lexer = LexerGenerator()

    def _add_tokens(self):
        # Keywords
        self.lexer.add('LET', r'LET')
        self.lexer.add('IF', r'IF')
        self.lexer.add('THEN', r'THEN')
        self.lexer.add('ELSE', r'ELSE')
        self.lexer.add('END', r'END')
        self.lexer.add('FOR', r'FOR')
        self.lexer.add('TO', r'TO')
        self.lexer.add('DO', r'DO')
        self.lexer.add('FUNCTION', r'FUNCTION')
        self.lexer.add('PRINTLN', r'PRINTLN')
        self.lexer.add('TAKEOFF', r'TAKEOFF')
        self.lexer.add('LAND', r'LAND')
        self.lexer.add('WAYPOINT', r'WAYPOINT')
        self.lexer.add('AIRCRAFT', r'AIRCRAFT')
        self.lexer.add('RUNWAY', r'RUNWAY')
        self.lexer.add('FLAPS', r'FLAPS')
        self.lexer.add('SPEED', r'SPEED')
        self.lexer.add('ALTITUDE', r'ALTITUDE')
        self.lexer.add('WP_NAME', r'WP_NAME')

        # Math functions
        self.lexer.add('SIN', r'SIN')
        self.lexer.add('COS', r'COS')
        self.lexer.add('TAN', r'TAN')
        self.lexer.add('ASIN', r'ASIN')
        self.lexer.add('ACOS', r'ACOS')
        self.lexer.add('ATAN', r'ATAN')
        self.lexer.add('SINH', r'SINH')
        self.lexer.add('COSH', r'COSH')
        self.lexer.add('TANH', r'TANH')
        self.lexer.add('ASINH', r'ASINH')
        self.lexer.add('ACOSH', r'ACOSH')
        self.lexer.add('ATANH', r'ATANH')
        self.lexer.add('EXP', r'EXP')
        self.lexer.add('LOG10', r'LOG10')
        self.lexer.add('LOG', r'LOG')
        self.lexer.add('SQRT', r'SQRT')
        self.lexer.add('CBRT', r'CBRT')
        self.lexer.add('CEIL', r'CEIL')
        self.lexer.add('FLOOR', r'FLOOR')
        self.lexer.add('ABS', r'ABS')
        self.lexer.add('ROUND', r'ROUND')
        self.lexer.add('TRUNC', r'TRUNC')
        self.lexer.add('SIGNUM', r'SIGNUM')
        self.lexer.add('RINT', r'RINT')
        self.lexer.add('MIN', r'MIN')
        self.lexer.add('MAX', r'MAX')
        self.lexer.add('RANDOM', r'RANDOM')

        # Other tokens
        self.lexer.add('STRING', r'"[^"]*"')
        self.lexer.add('NUMBER', r'-?\d+(\.\d+)?')
        self.lexer.add('BOOLEAN', r'TRUE|FALSE')
        self.lexer.add('IDENTIFIER', r'[a-zA-Z_][a-zA-Z0-9_]*')
        self.lexer.add('COMMA', r',')
        self.lexer.add('OPEN_PAREN', r'\(')
        self.lexer.add('CLOSE_PAREN', r'\)')
        self.lexer.add('OPEN_BRACKET', r'\[')
        self.lexer.add('CLOSE_BRACKET', r'\]')
        self.lexer.add('OPEN_BRACE', r'\{')
        self.lexer.add('CLOSE_BRACE', r'\}')
        self.lexer.add('SEMI_COLON', r';')
        self.lexer.add('COLON', r':')
        self.lexer.add('PLUS', r'\+')
        self.lexer.add('MINUS', r'-')
        self.lexer.add('TIMES', r'\*')
        self.lexer.add('DIVIDE', r'/')
        self.lexer.add('POWER', r'\^')
        self.lexer.add('MODULO', r'%')
        self.lexer.add('GREATER_THAN', r'>')
        self.lexer.add('LESS_THAN', r'<')
        self.lexer.add('GREATER_THAN_EQUAL', r'>=')
        self.lexer.add('LESS_THAN_EQUAL', r'<=')
        self.lexer.add('NOT_EQUAL', r'!=')
        self.lexer.add('EQUAL_EQUAL', r'==')
        self.lexer.add('AND', r'&&')
        self.lexer.add('OR', r'\|\|')
        self.lexer.add('NOT', r'!')
        self.lexer.add('EQUALS', r'=')
        # self.lexer.add('NEWLINE', r'\n+')
        self.lexer.add('SKIP', r'[ \t]+')
        self.lexer.add('MISMATCH', r'.')
        self.lexer.ignore(r'[ \t]+|\n|\r+')

    def get_lexer(self):
        self._add_tokens()
        return self.lexer.build()
