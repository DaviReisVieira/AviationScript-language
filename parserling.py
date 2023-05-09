from rply import ParserGenerator
from tree import *


class Parser():
    def __init__(self):
        self.pg = ParserGenerator(
            [
                "LET", "EQUALS", "IDENTIFIER", "COLON", "COMMA",
                "NUMBER", "STRING", "BOOLEAN",
                "PLUS", "MINUS", "TIMES", "DIVIDE",
                "IF", "THEN", "ELSE", "END", "FOR", "TO", "DO",
                "EQUAL_EQUAL", "NOT_EQUAL", "GREATER_THAN", "LESS_THAN", "GREATER_THAN_EQUAL", "LESS_THAN_EQUAL",
                "OPEN_PAREN", "CLOSE_PAREN", "PRINTLN", "OPEN_BRACE", "CLOSE_BRACE", "OPEN_BRACKET", "CLOSE_BRACKET",
                "SIN", "COS", "TAN", "ASIN", "ACOS", "ATAN", "SINH", "COSH", "TANH", "ASINH", "ACOSH", "ATANH", "EXP", "LOG", "LOG10", "SQRT", "CBRT", "CEIL", "FLOOR", "ABS", "ROUND", "TRUNC", "SIGNUM", "RINT", "MIN", "MAX", "RANDOM"
            ],
            precedence=[
                ("left", ["PLUS", "MINUS"]),
                ("left", ["TIMES", "DIVIDE"]),
            ]
        )

    def parse(self):
        @self.pg.production("program : statements")
        def program(p):
            return p[0]

        @self.pg.production("statements : statements statement")
        @self.pg.production("statements : statement")
        def statements(p):
            if len(p) == 1:
                return Statements(p[0])
            else:
                p[0].add_statement(p[1])
                return p[0]

        @self.pg.production("statement : assignment")
        @self.pg.production("statement : conditional")
        @self.pg.production("statement : loop")
        @self.pg.production("statement : println")
        def statement(p):
            return p[0]

        @self.pg.production("conditional : IF condition THEN statements END")
        @self.pg.production("conditional : IF condition THEN statements ELSE statements END")
        def conditional(p):
            if len(p) == 5:
                return If(p[1], p[3])
            else:
                return IfElse(p[1], p[3], p[5])

        @self.pg.production("loop : FOR IDENTIFIER EQUALS value TO value DO statements END")
        def loop(p):
            return Loop(p[1], p[3], p[5], p[7])

        @self.pg.production("condition : expression")
        @self.pg.production("condition : comparison")
        def condition(p):
            return p[0]

        @self.pg.production("comparison : expression EQUAL_EQUAL expression")
        @self.pg.production("comparison : expression NOT_EQUAL expression")
        @self.pg.production("comparison : expression GREATER_THAN expression")
        @self.pg.production("comparison : expression LESS_THAN expression")
        @self.pg.production("comparison : expression GREATER_THAN_EQUAL expression")
        @self.pg.production("comparison : expression LESS_THAN_EQUAL expression")
        def comparison(p):
            return BinOp(p[1], p[0], p[2])

        @self.pg.production("assignment : LET IDENTIFIER EQUALS value")
        @self.pg.production("assignment : LET IDENTIFIER EQUALS object")
        @self.pg.production("assignment : LET IDENTIFIER EQUALS expression")
        def assignment(p):
            return Assignment(p[1].getstr(), p[3])

        @self.pg.production('value : NUMBER')
        def number(p):
            return Number(p[0].value)

        @self.pg.production('value : STRING')
        def string(p):
            return String(p[0].value)

        @self.pg.production('value : BOOLEAN')
        def boolean(p):
            return Boolean(p[0].value)

        @self.pg.production('object : OPEN_BRACE properties CLOSE_BRACE')
        def object(p):
            return Object(p[1])

        @self.pg.production('properties : properties COMMA property')
        @self.pg.production('properties : property')
        def properties(p):
            if len(p) == 1:
                return [p[0]]
            else:
                p[0].append(p[2])
                return p[0]

        @self.pg.production('property : STRING COLON value')
        def property(p):
            return Property(p[0].getstr(), p[2])

        @self.pg.production('expression : term')
        @self.pg.production('expression : term PLUS expression')
        @self.pg.production('expression : term MINUS expression')
        def expression(p):
            if len(p) == 1:
                return p[0]
            else:
                return BinOp(p[1], p[0], p[2])

        @self.pg.production('term : factor')
        @self.pg.production('term : factor TIMES term')
        @self.pg.production('term : factor DIVIDE term')
        def term(p):
            if len(p) == 1:
                return p[0]
            else:
                return BinOp(p[1], p[0], p[2])

        @self.pg.production('factor : IDENTIFIER')
        @self.pg.production('factor : IDENTIFIER OPEN_BRACKET STRING CLOSE_BRACKET')
        @self.pg.production('factor : NUMBER')
        # @self.pg.production('factor : functionCall')
        @self.pg.production('factor : mathFunction OPEN_PAREN expression CLOSE_PAREN')
        @self.pg.production('factor : OPEN_PAREN expression CLOSE_PAREN')
        def factor(p):
            if len(p) == 1:
                if p[0].gettokentype() == "IDENTIFIER":
                    return Identifier(p[0].getstr())
                elif p[0].gettokentype() == "NUMBER":
                    return Number(p[0].value)
                else:
                    return UnOp(p[0], p[1])
            elif len(p) == 3:
                return p[1]
            elif len(p) == 4:
                if p[0].gettokentype() == "SIN" or p[0].gettokentype() == "COS" or p[0].gettokentype() == "TAN" or p[0].gettokentype() == "ASIN" or p[0].gettokentype() == "ACOS" or p[0].gettokentype() == "ATAN" or p[0].gettokentype() == "SINH" or p[0].gettokentype() == "COSH" or p[0].gettokentype() == "TANH" or p[0].gettokentype() == "ASINH" or p[0].gettokentype() == "ACOSH" or p[0].gettokentype() == "ATANH" or p[0].gettokentype() == "EXP" or p[0].gettokentype() == "LOG" or p[0].gettokentype() == "LOG10" or p[0].gettokentype() == "SQRT" or p[0].gettokentype() == "CBRT" or p[0].gettokentype() == "CEIL" or p[0].gettokentype() == "FLOOR" or p[0].gettokentype() == "ABS" or p[0].gettokentype() == "ROUND" or p[0].gettokentype() == "TRUNC" or p[0].gettokentype() == "SIGNUM" or p[0].gettokentype() == "RINT" or p[0].gettokentype() == "MIN" or p[0].gettokentype() == "MAX" or p[0].gettokentype() == "RANDOM":
                    return MathFunction(p[0], p[2])
                elif p[0].gettokentype() == "IDENTIFIER" and p[1].gettokentype() == "OPEN_BRACKET":
                    identifier = Identifier(p[0].getstr())
                    value = identifier.eval()[p[2].getstr()]
                    return value
            else:
                return UnOp(p[0], p[1])

        @self.pg.production('mathFunction : SIN')
        @self.pg.production('mathFunction : COS')
        @self.pg.production('mathFunction : TAN')
        @self.pg.production('mathFunction : ASIN')
        @self.pg.production('mathFunction : ACOS')
        @self.pg.production('mathFunction : ATAN')
        @self.pg.production('mathFunction : SINH')
        @self.pg.production('mathFunction : COSH')
        @self.pg.production('mathFunction : TANH')
        @self.pg.production('mathFunction : ASINH')
        @self.pg.production('mathFunction : ACOSH')
        @self.pg.production('mathFunction : ATANH')
        @self.pg.production('mathFunction : EXP')
        @self.pg.production('mathFunction : LOG')
        @self.pg.production('mathFunction : LOG10')
        @self.pg.production('mathFunction : SQRT')
        @self.pg.production('mathFunction : CBRT')
        @self.pg.production('mathFunction : CEIL')
        @self.pg.production('mathFunction : FLOOR')
        @self.pg.production('mathFunction : ABS')
        @self.pg.production('mathFunction : ROUND')
        @self.pg.production('mathFunction : TRUNC')
        @self.pg.production('mathFunction : SIGNUM')
        @self.pg.production('mathFunction : RINT')
        @self.pg.production('mathFunction : MIN')
        @self.pg.production('mathFunction : MAX')
        @self.pg.production('mathFunction : RANDOM')
        def mathFunction(p):
            return p[0]

        @self.pg.production('println : PRINTLN OPEN_PAREN expression CLOSE_PAREN')
        def program(p):
            return Println(p[2])

        @self.pg.error
        def error_handle(token):
            raise ValueError(token)

    def get_parser(self):
        return self.pg.build()
