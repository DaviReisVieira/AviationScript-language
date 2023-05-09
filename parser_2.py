from rply import ParserGenerator
from ast_1 import *
# program         -> { statement }
# statement       -> ( assignment | conditional | loop | operation | function | println )
# assignment      -> "LET" variable "=" ( value | object | expression )
# value           -> ( number | string | boolean )
# object          -> "{" { property } "}"
# property        -> key value
# key             -> string
# conditional     -> "IF" condition "THEN" { statement } ["ELSE" { statement }] "END"
# loop            -> "FOR" variable "=" value "TO" value "DO" { statement } "END"
# operation       -> ( takeoff | land | waypoint )
# takeoff         -> "TAKEOFF" "{" "AIRCRAFT" aircraftName "RUNWAY" runwayName "FLAPS" flapPosition "SPEED" speed "ALTITUDE" altitude "}"
# land            -> "LAND" "{" "AIRCRAFT" aircraftName "RUNWAY" runwayName "FLAPS" flapPosition "SPEED" speed "ALTITUDE" altitude "}"
# waypoint        -> "WAYPOINT" "{" "WP_NAME" waypointName "SPEED" speed "ALTITUDE" altitude "}"
# function        -> "FUNCTION" functionName "(" [ parameter { "," parameter } ] ")" "{" { statement } "}"
# println         -> "PRINTLN" "(" expression ")"
# functionCall    -> functionName "(" [ expression { "," expression } ] ")"
# parameter       -> variable
# mathFunction    -> "SIN" | "COS" | "TAN" | "ASIN" | "ACOS" | "ATAN" | "SINH" | "COSH" | "TANH" | "ASINH" | "ACOSH" | "ATANH" | "EXP" | "LOG" | "LOG10" | "SQRT" | "CBRT" | "CEIL" | "FLOOR" | "ABS" | "ROUND" | "TRUNC" | "SIGNUM" | "RINT" | "MIN" | "MAX" | "RANDOM"

# condition       -> ( expression | comparison )
# expression      -> term { ( "+" | "-" ) term }
# term            -> factor { ( "*" | "/" ) factor }
# factor          -> variable | number | functionCall | mathFunction "(" expression ")" | "(" expression ")"
# comparison      -> expression ( "==" | "!=" | ">" | "<" | ">=" | "<=" ) expression

# variable        -> letter { letter | digit }
# number          -> [ "-" ] digit { digit } [ "." digit { digit } ]
# string          -> '"' { character } '"'
# character       -> letter | digit | " " | "'" | "." | "," | ";" | ":" | "?" | "!" | "@" | "#" | "$" | "%" | "^" | "&" | "*" | "(" | ")" | "-" | "_" | "+" | "=" | "[" | "]" | "{" | "}" | "|" | "\" | "/" | "<" | ">" | "`" | "~"
# letter          -> ( "A" ... "Z" ) | ( "a" ... "z" )
# digit           -> "0" ... "9"


class Parser():
    def __init__(self):
        self.pg = ParserGenerator(
            # A list of all token names accepted by the parser.
            # [
            #     "LET", "IF", "THEN", "ELSE", "END", "FOR", "TO", "DO", "TAKEOFF", "LAND", "WAYPOINT", "FUNCTION", "PRINTLN",
            #     "SIN", "COS", "TAN", "ASIN", "ACOS", "ATAN", "SINH", "COSH", "TANH", "ASINH", "ACOSH", "ATANH", "EXP", "LOG", "LOG10", "SQRT", "CBRT", "CEIL", "FLOOR", "ABS", "ROUND", "TRUNC", "SIGNUM", "RINT", "MIN", "MAX", "RANDOM",
            #     "AIRCRAFT", "RUNWAY", "FLAPS", "SPEED", "ALTITUDE", "WP_NAME",
            #     "PLUS", "MINUS", "MUL", "DIV", "MOD",
            #     "OPEN_PAREN", "CLOSE_PAREN", "OPEN_BRACE", "CLOSE_BRACE", "COMMA", "SEMI", "COLON",
            #     "EQ", "NEQ", "LT", "LE", "GT", "GE",
            #     "NUMBER", "STRING", "BOOLEAN", "IDENTIFIER",
            # ],
            [
                "EQUALS",
                "MUL", "DIV", "MOD", "PLUS", "MINUS", "COMMA",
                "FALSE", "TRUE",
                "LET", "IF", "THEN", "ELSE", "END", "FOR", "TO", "DO", "TAKEOFF", "LAND", "WAYPOINT", "FUNCTION", "PRINTLN", "IDENTIFIER", "NUMBER", "STRING", "EQ", "OPEN_BRACE", "CLOSE_BRACE", "OPEN_PAREN", "CLOSE_PAREN",
            ],
            # A list of precedence rules with ascending precedence, to
            # disambiguate ambiguous production rules.
            precedence=[
                ("left", ["PLUS", "MINUS"]),
                ("left", ["MUL", "DIV", "MOD"]),
                ("left", ["EQ", "NEQ", "LT", "LE", "GT", "GE"]),
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
        @self.pg.production("statement : operation")
        @self.pg.production("statement : function")
        @self.pg.production("statement : println")
        def statement(p):
            return p[0]

        @self.pg.production("assignment : LET IDENTIFIER EQUALS value")
        @self.pg.production("assignment : LET IDENTIFIER EQUALS object")
        @self.pg.production("assignment : LET IDENTIFIER EQUALS expression")
        def assignment(p):
            return Assignment(p[1].getstr(), p[3])

        @self.pg.production("value : number")
        @self.pg.production("value : string")
        @self.pg.production("value : boolean")
        def value(p):
            return p[0]

        @self.pg.production("object : OPEN_BRACE properties CLOSE_BRACE")
        def object(p):
            return Object(p[1])

        @self.pg.production("properties : properties property")
        @self.pg.production("properties : property")
        def properties(p):
            if len(p) == 1:
                return Properties(p[0])
            else:
                p[0].add_property(p[1])
                return p[0]

        @self.pg.production("property : key value")
        def property(p):
            return Property(p[0], p[1])

        @self.pg.production("key : string")
        def key(p):
            return p[0]

        @self.pg.production("conditional : IF condition THEN statements END")
        @self.pg.production("conditional : IF condition THEN statements ELSE statements END")
        def conditional(p):
            if len(p) == 5:
                return If(p[1], p[3])
            else:
                return IfElse(p[1], p[3], p[5])

        @self.pg.production("loop : FOR IDENTIFIER EQ number TO number DO statements END")
        def loop(p):
            return Loop(p[1].getstr(), p[3], p[5], p[7])

        @self.pg.production("operation : TAKEOFF")
        @self.pg.production("operation : LAND")
        @self.pg.production("operation : WAYPOINT")
        def operation(p):
            return Operation(p[0].getstr())

        @self.pg.production("function : FUNCTION IDENTIFIER OPEN_PAREN CLOSE_PAREN statements END")
        # @self.pg.production("function : FUNCTION IDENTIFIER OPEN_PAREN CLOSE_PAREN statements RETURN expression END")
        def function(p):
            if len(p) == 6:
                return Function(p[1].getstr(), p[4])
            else:
                return Function(p[1].getstr(), p[4], p[6])

        @self.pg.production("println : PRINTLN OPEN_PAREN expression CLOSE_PAREN")
        def println(p):
            return Println(p[2])

        @self.pg.production("condition : expression EQ expression")
        # @self.pg.production("condition : expression NEQ expression")
        # @self.pg.production("condition : expression LT expression")
        # @self.pg.production("condition : expression LE expression")
        # @self.pg.production("condition : expression GT expression")
        # @self.pg.production("condition : expression GREATER_THAN_EQUAL expression")
        def condition(p):
            return Condition(p[1], p[0], p[2])

        @self.pg.production("expression : expression PLUS expression")
        @self.pg.production("expression : expression MINUS expression")
        @self.pg.production("expression : expression MUL expression")
        @self.pg.production("expression : expression DIV expression")
        @self.pg.production("expression : expression MOD expression")
        def expression(p):
            return Expression(p[1], p[0], p[2])

        @self.pg.production("expression : MINUS expression")
        def expression_minus(p):
            return Expression("-", Number(0), p[1])

        @self.pg.production("expression : OPEN_PAREN expression CLOSE_PAREN")
        def expression_paren(p):
            return p[1]

        @self.pg.production("expression : function_call")
        def expression_function_call(p):
            return p[0]

        @self.pg.production("function_call : IDENTIFIER OPEN_PAREN CLOSE_PAREN")
        @self.pg.production("function_call : IDENTIFIER OPEN_PAREN arguments CLOSE_PAREN")
        def function_call(p):
            if len(p) == 3:
                return FunctionCall(p[0].getstr())
            else:
                return FunctionCall(p[0].getstr(), p[2])

        @self.pg.production("arguments : arguments COMMA expression")
        @self.pg.production("arguments : expression")
        def arguments(p):
            if len(p) == 1:
                return Arguments(p[0])
            else:
                p[0].add_argument(p[2])
                return p[0]

        @self.pg.production("number : NUMBER")
        def number(p):
            return Number(p[0].getstr())

        @self.pg.production("string : STRING")
        def string(p):
            return String(p[0].getstr())

        @self.pg.production("boolean : TRUE")
        @self.pg.production("boolean : FALSE")
        def boolean(p):
            return Boolean(p[0].getstr())

        @self.pg.error
        def error_handle(token):
            raise ValueError(token)

    def get_parser(self):
        return self.pg.build()
