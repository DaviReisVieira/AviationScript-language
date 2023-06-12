import re
import sys
import math


class Token:
    def __init__(self, type: str, value: int | float | str):
        self.type = type
        self.value = value


class SymbolTable:
    def __init__(self):
        self.table = {
            'PI': ('Float', math.pi),
        }

    def getter(self, key):
        return self.table[key]

    def setter(self, key, tuple):
        if key not in self.table:
            sys.stderr.write("Variable not declared")
            sys.exit(1)
        if self.table[key][0] == tuple[0]:
            self.table[key] = tuple
        else:
            sys.stderr.write("Invalid types on setter")
            sys.exit(1)

    def create(self, key, type, tuple):
        if key in self.table:
            sys.stderr.write("Variable already exists")
            sys.exit(1)
        if type == tuple[0]:
            self.table[key] = tuple
        else:
            sys.stderr.write("Invalid type missing")
            sys.exit(1)


symbolTable = SymbolTable()


class FuncTable:
    def __init__(self):
        self.table = {
            'sin': (['Float'], 'Float'),
            'cos': (['Float'], 'Float'),
            'tan': (['Float'], 'Float'),
            'atan2': (['Float', 'Float'], 'Float'),
            'log': (['Float'], 'Float'),
            'sqrt': (['Float'], 'Float'),
            'exp': (['Float'], 'Float'),
            'abs': (['Float'], 'Float'),
            'pow': (['Float', 'Float'], 'Float'),
        }

    def getter(self, key):
        try:
            return self.table[key]
        except KeyError:
            sys.stderr.write("Function not declared")
            sys.exit(1)

    def create(self, name, func_node):
        if name in self.table:
            sys.stderr.write("Function already exists")
            sys.exit(1)

        self.table[name] = (func_node)


funcTable = FuncTable()


class Node:
    def __init__(self, value: str, children: list):
        self.value = value
        self.children = children

    def Evaluate(self, st: SymbolTable) -> int | float | str:
        pass


class BinOp(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def Evaluate(self, st: SymbolTable):
        left_value = self.children[0].Evaluate(st)
        right_value = self.children[1].Evaluate(st)

        type_left = left_value[0]
        type_right = right_value[0]

        if (type_left == 'Int' and type_right == 'Int') or (type_left == 'Float' and type_right == 'Float') or (type_left == 'Float' and type_right == 'Int') or (type_left == 'Int' and type_right == 'Float'):
            if self.value == '+':
                return ('Float', left_value[1] + right_value[1])
            elif self.value == '-':
                return ('Float', left_value[1] - right_value[1])
            elif self.value == '*':
                return ('Float', left_value[1] * right_value[1])
            elif self.value == '/':
                return ('Float', left_value[1] / right_value[1])
            elif self.value == '||':
                return ('Float', left_value[1] or right_value[1])
            elif self.value == '&&':
                return ('Float', left_value[1] and right_value[1])

        if self.value == '==':
            if left_value[1] == right_value[1]:
                return ('Int', 1)
            else:
                return ('Int', 0)
        elif self.value == '>':
            if left_value[1] > right_value[1]:
                return ('Int', 1)
            else:
                return ('Int', 0)
        elif self.value == '<':
            if left_value[1] < right_value[1]:
                return ('Int', 1)
            else:
                return ('Int', 0)
        elif self.value == '.':
            return ('String', str(left_value[1]) + str(right_value[1]))
        else:
            sys.stderr.write("Invalid types on BinOp")
            sys.exit(1)


class UnOp(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def Evaluate(self, st: SymbolTable):
        left_node = self.children[0].Evaluate(st)

        if left_node[0] == 'Int':
            if self.value == '-':
                return ('Int', -left_node[1])
            elif self.value == '+':
                return ('Int', +left_node[1])
            elif self.value == '!':
                return ('Int', not left_node[1])
            else:
                sys.stderr.write("Invalid operator")
                sys.exit(1)

        elif left_node[0] == 'Float':
            if self.value == '-':
                return ('Float', -left_node[1])
            elif self.value == '+':
                return ('Float', +left_node[1])
            elif self.value == '!':
                return ('Float', not left_node[1])
            else:
                sys.stderr.write("Invalid operator")
                sys.exit(1)
        else:
            sys.stderr.write("Invalid type")
            sys.exit(1)


class IntVal(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def Evaluate(self, st: SymbolTable):
        return ('Int', self.value)


class FloatVal(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def Evaluate(self, st: SymbolTable):
        return ('Float', self.value)


class StringVal(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def Evaluate(self, st: SymbolTable):
        return ('String', self.value)


class NoOp(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def Evaluate(self, st: SymbolTable):
        return ('Int', 0)


class Ident(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def Evaluate(self, st: SymbolTable):
        return st.getter(self.value)


class Assign(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def Evaluate(self, st):
        st.setter(self.children[0].value, self.children[1].Evaluate(st))


class PrintLn(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def Evaluate(self, st: SymbolTable):
        print(self.children[0].Evaluate(st)[1])


class Waypoint(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def Evaluate(self, st: SymbolTable):
        print("------------- Waypoint Procedure ------------")
        print(" - Waypoint: " + self.children[0].value)
        print(" - Speed: " + str(self.children[1].Evaluate(st)[1]), "kts")
        print(" - Altitude: " + str(self.children[2].Evaluate(st)[1]), "ft")
        print("---------------------------------------------")


class Takeoff(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def Evaluate(self, st: SymbolTable):
        print("------------- Takeoff Procedure -------------")
        print(" - Aircraft: " + self.children[0].value)
        print(" - Runway: " + self.children[1].value)
        print(" - Flaps: " + str(self.children[2].Evaluate(st)[1]))
        print(" - Speed: " + str(self.children[3].Evaluate(st)[1]), "kts")
        print(" - Altitude: " + str(self.children[4].Evaluate(st)[1]), "ft")
        print("---------------------------------------------")


class Land(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def Evaluate(self, st: SymbolTable):
        print("------------- Landing Procedure -------------")
        print(" - Aircraft: " + self.children[0].value)
        print(" - Runway: " + self.children[1].value)
        print(" - Flaps: " + str(self.children[2].Evaluate(st)[1]), "º")
        print(" - Speed: " + str(self.children[3].Evaluate(st)[1]), "kts")
        print(" - Altitude: " + str(self.children[4].Evaluate(st)[1]), "ft")
        print("---------------------------------------------")


class MathFunc(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def Evaluate(self, st: SymbolTable):
        if self.value == 'sqrt':
            return ('Float', math.sqrt(self.children[0].Evaluate(st)[1]))
        elif self.value == 'sin':
            return ('Float', math.sin(self.children[0].Evaluate(st)[1]))
        elif self.value == 'cos':
            return ('Float', math.cos(self.children[0].Evaluate(st)[1]))
        elif self.value == 'tan':
            return ('Float', math.tan(self.children[0].Evaluate(st)[1]))
        elif self.value == 'atan2':
            return ('Float', math.atan2(self.children[0].Evaluate(st)[1], self.children[1].Evaluate(st)[1]))
        elif self.value == 'log':
            return ('Float', math.log(self.children[0].Evaluate(st)[1]))
        elif self.value == 'exp':
            return ('Float', math.exp(self.children[0].Evaluate(st)[1]))
        elif self.value == 'abs':
            return ('Float', abs(self.children[0].Evaluate(st)[1]))
        elif self.value == 'pow':
            return ('Float', math.pow(self.children[0].Evaluate(st)[1], self.children[1].Evaluate(st)[1]))
        else:
            sys.stderr.write("Invalid function")
            sys.exit(1)


class Block(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def Evaluate(self, st: SymbolTable):
        for child in self.children:
            result = child.Evaluate(st)
            if result != None and result[0] == 'return':
                return result[1]


class ReadLine(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def Evaluate(self, st: SymbolTable):
        input_value = input()
        if input_value.isdigit():
            return ('Int', int(input_value))
        elif input_value.replace('.', '', 1).isdigit():
            return ('Float', float(input_value))


class While(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def Evaluate(self, st: SymbolTable):
        while self.children[0].Evaluate(st)[1]:
            self.children[1].Evaluate(st)


class If(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def Evaluate(self, st: SymbolTable):
        if self.children[0].Evaluate(st)[1]:
            self.children[1].Evaluate(st)
        else:
            self.children[2].Evaluate(st)


class VarDec(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def Evaluate(self, st: SymbolTable):
        st.create(
            self.children[0].value, self.value, self.children[1].Evaluate(st))


class FuncDec(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def Evaluate(self, st: SymbolTable):
        funcTable.create(self.children[0].value, self)


class FuncCall(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def Evaluate(self, st: SymbolTable):
        funcDec = funcTable.getter(self.value)
        funcSymbolTable = SymbolTable()
        if (len(funcDec.children) - 2) != len(self.children):
            sys.stderr.write("Invalid number of arguments")
            sys.exit(1)
        for i in range(len(self.children)):
            funcDec.children[i + 1].Evaluate(funcSymbolTable)
            funcSymbolTable.setter(
                funcDec.children[i + 1].children[0].value, self.children[i].Evaluate(st))
        return funcDec.children[-1].Evaluate(funcSymbolTable)


class Return(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def Evaluate(self, st: SymbolTable):
        return ('return', self.children[0].Evaluate(st))


class Tokenizer:
    def __init__(self, source: str, position: int, next: Token):
        self.source = source
        self.position = position
        self.next = next
        self.reserved_words = ['println', 'while', 'if', 'else',
                               'end', 'readline', 'String', 'Int', 'Float', 'function', 'return',
                               'sqrt', 'sin', 'cos', 'tan', 'atan2', 'log', 'exp', 'abs', 'pow',
                               'TAKEOFF', 'WAYPOINT', 'LAND']
        self.math_functions = ['sqrt', 'sin', 'cos',
                               'tan', 'atan2', 'log', 'exp', 'abs', 'pow']
        self.LETTERS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.DIGITS = '0123456789'

    def selectNext(self):
        if self.position >= len(self.source):
            self.next = Token('EOF', None)
            return

        char = self.source[self.position]
        while char == ' ':
            self.position += 1
            if self.position >= len(self.source):
                self.next = Token('EOF', None)
                return
            char = self.source[self.position]
        if char == '+':
            self.position += 1
            self.next = Token('ADD', "+")
        elif char == '-':
            self.position += 1
            self.next = Token('SUB', "-")
        elif char == '!':
            self.position += 1
            self.next = Token('NOT', "!")
        elif char == '|':
            start = self.position
            self.position += 1
            if self.position >= len(self.source):
                sys.stderr.write("Invalid token")
                sys.exit(1)
            char = self.source[self.position]
            if char == '|':
                self.position += 1
                self.next = Token('OR', "||")
            else:
                sys.stderr.write("Invalid token")
                sys.exit(1)
        elif char == '>':
            self.position += 1
            self.next = Token('GT', ">")
        elif char == '<':
            self.position += 1
            self.next = Token('LT', "<")
        elif char == '*':
            self.position += 1
            self.next = Token('MULT', "*")
        elif char == '/':
            self.position += 1
            self.next = Token('DIV', "/")
        elif char == '&':
            start = self.position
            self.position += 1
            if self.position >= len(self.source):
                sys.stderr.write("Invalid token size")
                sys.exit(1)
            char = self.source[self.position]
            if char == '&':
                self.position += 1
                self.next = Token('AND', "&&")
            else:
                sys.stderr.write("Invalid token &")
                sys.exit(1)
        elif char == '{':
            self.position += 1
            self.next = Token('LBRACE', "{")
        elif char == '}':
            self.position += 1
            self.next = Token('RBRACE', "}")
        elif char == '(':
            self.position += 1
            self.next = Token('LPAREN', "(")
        elif char == ')':
            self.position += 1
            self.next = Token('RPAREN', ")")
        elif char == '=':
            self.position += 1
            if self.position >= len(self.source):
                sys.stderr.write("Invalid token size =")
                sys.exit(1)
            char = self.source[self.position]
            if char == '=':
                self.position += 1
                self.next = Token('EQ', "==")
            else:
                self.next = Token('ASSIGN', "=")
        elif char == ':':
            self.position += 1
            if self.position >= len(self.source):
                sys.stderr.write("Invalid token size :")
                sys.exit(1)
            char = self.source[self.position]
            if char == ':':
                self.position += 1
                self.next = Token('COLON', "::")
            else:
                self.position += 1
                self.next = Token('SINGLE_COLON', ":")
        elif char == '.':
            self.position += 1
            self.next = Token('CONCAT', ".")
        elif char == ',':
            self.position += 1
            self.next = Token('COMMA', ",")
        elif char == '"':
            start = self.position
            self.position += 1
            if self.position >= len(self.source):
                sys.stderr.write("Invalid token size '")
                sys.exit(1)
            char = self.source[self.position]
            while char != '"':
                self.position += 1
                if self.position >= len(self.source):
                    sys.stderr.write("Invalid token size' while")
                    sys.exit(1)
                char = self.source[self.position]
            self.next = Token('STRING', self.source[start+1:self.position])
            self.position += 1
        elif char == '\n':
            self.position += 1
            self.next = Token('NEWLINE', "\n")
        elif char in self.DIGITS:
            start = self.position
            while self.position < len(self.source) and self.source[self.position] in self.DIGITS:
                self.position += 1
            if self.position < len(self.source) and self.source[self.position] == '.':
                self.position += 1
                while self.position < len(self.source) and self.source[self.position] in self.DIGITS:
                    self.position += 1
                self.next = Token('FLOAT', float(
                    self.source[start:self.position]))
            else:
                self.next = Token('INT', int(self.source[start:self.position]))
        elif char in self.LETTERS:
            start = self.position
            while self.position < len(self.source) and (self.source[self.position] in self.LETTERS or self.source[self.position] in self.DIGITS or self.source[self.position] == '_'):
                self.position += 1
            if self.source[start:self.position] in self.reserved_words:
                if self.source[start:self.position] in self.math_functions:
                    self.next = Token(
                        'MATH_FUNCTION', self.source[start:self.position])
                else:
                    self.next = Token(
                        self.source[start:self.position].upper(), self.source[start:self.position])
            else:
                self.next = Token(
                    'IDENTIFIER', self.source[start:self.position])
        else:
            sys.stderr.write("Invalid token size general")
            sys.exit(1)


class Parser:
    def __init__(self, tokenizer: Tokenizer):
        self.tokenizer = tokenizer

    def parseFactor():
        if Parser.tokenizer.next.type == 'INT':
            value = IntVal(int(Parser.tokenizer.next.value), [])
            Parser.tokenizer.selectNext()
            return value
        elif Parser.tokenizer.next.type == 'FLOAT':
            value = FloatVal(float(Parser.tokenizer.next.value), [])
            Parser.tokenizer.selectNext()
            return value
        if Parser.tokenizer.next.type == 'STRING':
            value = StringVal(Parser.tokenizer.next.value, [])
            Parser.tokenizer.selectNext()
            return value
        elif Parser.tokenizer.next.type == 'IDENTIFIER':
            identifier = Parser.tokenizer.next.value
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type == 'LPAREN':
                func_args = []
                Parser.tokenizer.selectNext()
                if Parser.tokenizer.next.type != 'RPAREN':
                    func_args.append(Parser.parseRelExpression())
                    while Parser.tokenizer.next.type != 'RPAREN':
                        if Parser.tokenizer.next.type != 'COMMA':
                            sys.stderr.write(
                                'Expected COMMA token on parseFactor')
                            sys.exit(1)
                        Parser.tokenizer.selectNext()
                        func_args.append(Parser.parseRelExpression())
                value = FuncCall(identifier, func_args)
                Parser.tokenizer.selectNext()
                return value
            else:
                return Ident(identifier, [])
        elif Parser.tokenizer.next.type == 'MATH_FUNCTION':
            math_function_ident = Parser.tokenizer.next.value
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type == 'LPAREN':
                Parser.tokenizer.selectNext()
                expression = Parser.parseRelExpression()
                if Parser.tokenizer.next.type == 'COMMA':
                    Parser.tokenizer.selectNext()
                    expression2 = Parser.parseRelExpression()
                    expression = [expression, expression2]
                    math_function = MathFunc(
                        math_function_ident, expression)
                    if Parser.tokenizer.next.type != 'RPAREN':
                        sys.stderr.write(
                            'Expected RPAREN token on parseFactor Math RPAREN 1')
                        sys.exit(1)
                    Parser.tokenizer.selectNext()
                    return math_function
                else:
                    if Parser.tokenizer.next.type != 'RPAREN':
                        sys.stderr.write(
                            'Expected RPAREN token on parseFactor Math RPAREN 2')
                        sys.exit(1)
                    math_function = MathFunc(
                        math_function_ident, [expression])
                    Parser.tokenizer.selectNext()
                    return math_function
        elif Parser.tokenizer.next.type == 'SUB':
            Parser.tokenizer.selectNext()
            value = UnOp('-', [Parser.parseFactor()])
            return value
        elif Parser.tokenizer.next.type == 'ADD':
            Parser.tokenizer.selectNext()
            value = UnOp('+', [Parser.parseFactor()])
            return value
        elif Parser.tokenizer.next.type == 'NOT':
            Parser.tokenizer.selectNext()
            value = UnOp('!', [Parser.parseFactor()])
            return value
        elif Parser.tokenizer.next.type == 'LPAREN':
            Parser.tokenizer.selectNext()
            result = Parser.parseRelExpression()
            if Parser.tokenizer.next.type != 'RPAREN':
                sys.stderr.write('1 - Expected RPAREN token on parseFactor')
                sys.exit(1)
            Parser.tokenizer.selectNext()
            return result
        elif Parser.tokenizer.next.type == 'READLINE':
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type != 'LPAREN':
                sys.stderr.write('Expected LPAREN token on parseFactor')
                sys.exit(1)
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type != 'RPAREN':
                sys.stderr.write('2 - Expected RPAREN token on parseFactor')
                sys.exit(1)
            Parser.tokenizer.selectNext()
            return ReadLine([], [])
        else:
            sys.stderr.write(
                'Expected INT or FLOAT or LPAREN token on parseFactor')
            sys.exit(1)

    @staticmethod
    def parseTerm():
        result = Parser.parseFactor()

        while Parser.tokenizer.next.type == "MULT" or Parser.tokenizer.next.type == "DIV" or Parser.tokenizer.next.type == "AND":
            op_type = Parser.tokenizer.next.type
            Parser.tokenizer.selectNext()
            if op_type == "MULT":
                result = BinOp('*', [result, Parser.parseFactor()])
            elif op_type == "DIV":
                result = BinOp('/', [result, Parser.parseFactor()])
            elif op_type == "AND":
                result = BinOp('&&', [result, Parser.parseFactor()])
            else:
                sys.stderr.write("Invalid MULT DIV")
                sys.exit(1)
        if Parser.tokenizer.next.type == "INT":
            sys.stderr.write("Expected INT token on parseTerm")
            sys.exit(1)
        elif Parser.tokenizer.next.type == "FLOAT":
            sys.stderr.write("Expected FLOAT token on parseTerm")
            sys.exit(1)
        else:
            return result

    @staticmethod
    def parseExpression():
        result = Parser.parseTerm()

        while Parser.tokenizer.next.type == 'ADD' or Parser.tokenizer.next.type == 'SUB' or Parser.tokenizer.next.type == 'OR' or Parser.tokenizer.next.type == 'CONCAT':
            op_type = Parser.tokenizer.next.type
            Parser.tokenizer.selectNext()
            if op_type == 'ADD':
                result = BinOp('+', [result, Parser.parseTerm()])
            elif op_type == 'SUB':
                result = BinOp('-', [result, Parser.parseTerm()])
            elif op_type == 'OR':
                result = BinOp('||', [result, Parser.parseTerm()])
            elif op_type == 'CONCAT':
                result = BinOp('.', [result, Parser.parseTerm()])
            else:
                sys.stderr.write('Invalid token')
                sys.exit(1)

        return result

    @staticmethod
    def parseRelExpression():
        result = Parser.parseExpression()

        while Parser.tokenizer.next.type == 'LT' or Parser.tokenizer.next.type == 'GT' or Parser.tokenizer.next.type == 'EQ':
            if Parser.tokenizer.next.type == 'LT':
                Parser.tokenizer.selectNext()
                result = BinOp('<', [result, Parser.parseExpression()])
            elif Parser.tokenizer.next.type == 'GT':
                Parser.tokenizer.selectNext()
                result = BinOp('>', [result, Parser.parseExpression()])
            elif Parser.tokenizer.next.type == 'EQ':
                Parser.tokenizer.selectNext()
                result = BinOp('==', [result, Parser.parseExpression()])
            else:
                sys.stderr.write('Invalid token')
                sys.exit(1)

        return result

    @staticmethod
    def parseStatement():
        if Parser.tokenizer.next.type == 'IDENTIFIER':
            identifier = Ident(Parser.tokenizer.next.value, [])
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type == 'ASSIGN':
                Parser.tokenizer.selectNext()
                assign = Assign("", [identifier, Parser.parseRelExpression()])
                if Parser.tokenizer.next.type != 'NEWLINE':
                    sys.stderr.write(
                        '1 - Expected NEWLINE token on parseStatement')
                    sys.exit(1)
                return assign
            elif Parser.tokenizer.next.type == 'COLON':
                Parser.tokenizer.selectNext()
                if Parser.tokenizer.next.type == 'INT':
                    Parser.tokenizer.selectNext()
                    if Parser.tokenizer.next.type == 'NEWLINE':
                        return VarDec("Int", [identifier, IntVal(0, [])])
                    elif Parser.tokenizer.next.type == 'ASSIGN':
                        Parser.tokenizer.selectNext()
                        return VarDec("Int", [identifier, Parser.parseRelExpression()])
                if Parser.tokenizer.next.type == 'FLOAT':
                    Parser.tokenizer.selectNext()
                    if Parser.tokenizer.next.type == 'NEWLINE':
                        return VarDec("Float", [identifier, FloatVal(0.0, [])])
                    elif Parser.tokenizer.next.type == 'ASSIGN':
                        Parser.tokenizer.selectNext()
                        return VarDec("Float", [identifier, Parser.parseRelExpression()])
                elif Parser.tokenizer.next.type == 'STRING':
                    Parser.tokenizer.selectNext()
                    if Parser.tokenizer.next.type == 'NEWLINE':
                        return VarDec("String", [identifier, StringVal(" ", [])])
                    elif Parser.tokenizer.next.type == 'ASSIGN':
                        Parser.tokenizer.selectNext()
                        return VarDec("String", [identifier, Parser.parseRelExpression()])
                else:
                    sys.stderr.write(
                        'Expected INT or FLOAT or STRING token on parseStatement')
                    sys.exit(1)
            elif Parser.tokenizer.next.type == 'LPAREN':
                Parser.tokenizer.selectNext()
                parameters = []
                if Parser.tokenizer.next.type != 'RPAREN':
                    parameters.append(Parser.parseRelExpression())
                    while Parser.tokenizer.next.type != 'RPAREN':
                        if Parser.tokenizer.next.type != 'COMMA':
                            sys.stderr.write(
                                'Expected COMMA token on parseStatement')
                            sys.exit(1)
                        Parser.tokenizer.selectNext()
                        parameters.append(Parser.parseRelExpression())
                Parser.tokenizer.selectNext()
                if Parser.tokenizer.next.type != 'NEWLINE':
                    sys.stderr.write(
                        'Expected NEWLINE token on parseStatement')
                    sys.exit(1)
                return FuncCall(identifier, parameters)

            else:
                sys.stderr.write('Expected ASSIGN token on parseStatement')
                sys.exit(1)
        elif Parser.tokenizer.next.type == 'RETURN':
            Parser.tokenizer.selectNext()
            return_statement = Return("", [Parser.parseRelExpression()])
            if Parser.tokenizer.next.type != 'NEWLINE':
                sys.stderr.write(
                    'Expected NEWLINE token on parseStatement')
                sys.exit(1)
            return return_statement
        elif Parser.tokenizer.next.type == 'FUNCTION':
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type != 'IDENTIFIER':
                sys.stderr.write(
                    'Expected IDENTIFIER token on parseStatement')
                sys.exit(1)
            funct_iden_node = Ident(Parser.tokenizer.next.value, [])
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type != 'LPAREN':
                sys.stderr.write(
                    'Expected LPAREN token on parseStatement')
                sys.exit(1)
            Parser.tokenizer.selectNext()
            parameters = []
            if Parser.tokenizer.next.type != 'RPAREN':
                if Parser.tokenizer.next.type != 'IDENTIFIER':
                    sys.stderr.write(
                        'Expected IDENTIFIER token on parseStatement')
                    sys.exit(1)
                identifier = Ident(Parser.tokenizer.next.value, [])
                Parser.tokenizer.selectNext()
                if Parser.tokenizer.next.type != 'COLON':
                    sys.stderr.write(
                        'Expected COLON token on parseStatement')
                    sys.exit(1)
                Parser.tokenizer.selectNext()
                if Parser.tokenizer.next.type != 'INT' and Parser.tokenizer.next.type != 'STRING' and Parser.tokenizer.next.type != 'FLOAT':
                    sys.stderr.write(
                        'Expected INT or FLOAT or STRING token on parseStatement')
                    sys.exit(1)
                if Parser.tokenizer.next.type == 'INT':
                    parameters.append(
                        VarDec("Int", [identifier, IntVal(0, [])]))
                elif Parser.tokenizer.next.type == 'STRING':
                    parameters.append(
                        VarDec("String", [identifier, StringVal(" ", [])]))
                elif Parser.tokenizer.next.type == 'FLOAT':
                    parameters.append(
                        VarDec("Float", [identifier, FloatVal(0.0, [])]))
                Parser.tokenizer.selectNext()
                while Parser.tokenizer.next.type != 'RPAREN':
                    if Parser.tokenizer.next.type != 'COMMA':
                        sys.stderr.write(
                            'Expected COMMA token on parseStatement')
                        sys.exit(1)
                    Parser.tokenizer.selectNext()
                    if Parser.tokenizer.next.type != 'IDENTIFIER':
                        sys.stderr.write(
                            'Expected IDENTIFIER token on parseStatement')
                        sys.exit(1)
                    identifier = Ident(Parser.tokenizer.next.value, [])
                    Parser.tokenizer.selectNext()
                    if Parser.tokenizer.next.type != 'COLON':
                        sys.stderr.write(
                            'Expected COLON token on parseStatement')
                        sys.exit(1)
                    Parser.tokenizer.selectNext()
                    if Parser.tokenizer.next.type != 'INT' and Parser.tokenizer.next.type != 'FLOAT' and Parser.tokenizer.next.type != 'STRING':
                        sys.stderr.write(
                            'Expected INT or FLOAT or STRING token on parseStatement')
                        sys.exit(1)
                    if Parser.tokenizer.next.type == 'INT':
                        parameters.append(
                            VarDec("Int", [identifier, IntVal(0, [])]))
                    elif Parser.tokenizer.next.type == 'FLOAT':
                        parameters.append(
                            VarDec("Float", [identifier, FloatVal(0.0, [])]))
                    elif Parser.tokenizer.next.type == 'STRING':
                        parameters.append(
                            VarDec("String", [identifier, StringVal(" ", [])]))
                    Parser.tokenizer.selectNext()
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type != 'COLON':
                sys.stderr.write(
                    'Expected COLON token on parseStatement')
                sys.exit(1)
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type != 'INT' and Parser.tokenizer.next.type != 'FLOAT' and Parser.tokenizer.next.type != 'STRING':
                sys.stderr.write(
                    'Expected INT or FLOAT or STRING token on parseStatement')
                sys.exit(1)
            function_type = Parser.tokenizer.next.type
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type != 'NEWLINE':
                sys.stderr.write(
                    'Expected NEWLINE token on parseStatement')
                sys.exit(1)
            statements = []
            Parser.tokenizer.selectNext()
            while Parser.tokenizer.next.type != 'END':
                statements.append(Parser.parseStatement())
                Parser.tokenizer.selectNext()
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type != 'NEWLINE':
                sys.stderr.write(
                    'Expected NEWLINE token on parseStatement')
                sys.exit(1)
            return FuncDec(function_type, [funct_iden_node]+parameters+[Block("", statements)])
        elif Parser.tokenizer.next.type == 'PRINTLN':
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type == 'LPAREN':
                Parser.tokenizer.selectNext()
                expression = Parser.parseRelExpression()
                if Parser.tokenizer.next.type != 'RPAREN':
                    sys.stderr.write('Expected RPAREN token on parseStatement')
                    sys.exit(1)
                println = PrintLn("", [expression])
                Parser.tokenizer.selectNext()
                if Parser.tokenizer.next.type != 'NEWLINE':
                    sys.stderr.write(
                        '2 - Expected NEWLINE token on parseStatement')
                    sys.exit(1)
                return println
            else:
                sys.stderr.write('Expected LPAREN token on parseStatement')
                sys.exit(1)

        elif Parser.tokenizer.next.type == 'LAND':
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type == 'LBRACE':
                Parser.tokenizer.selectNext()
                if Parser.tokenizer.next.type != 'STRING' and Parser.tokenizer.next.value != 'AIRCRAFT':
                    sys.stderr.write(
                        'Expected STRING token on parseStatement LAND1')
                    sys.exit(1)
                Parser.tokenizer.selectNext()
                if Parser.tokenizer.next.type != 'SINGLE_COLON':
                    sys.stderr.write(
                        'Expected SINGLE_COLON token on parseStatement')
                    sys.exit(1)
                Parser.tokenizer.selectNext()
                aircraft = Parser.parseRelExpression()
                if Parser.tokenizer.next.type != 'COMMA':
                    sys.stderr.write(
                        'Expected COMMA token on parseStatement')
                    sys.exit(1)
                Parser.tokenizer.selectNext()
                if Parser.tokenizer.next.type != 'STRING' and Parser.tokenizer.next.value != 'RUNWAY':
                    sys.stderr.write(
                        'Expected STRING token on parseStatement LAND3')
                    sys.exit(1)
                Parser.tokenizer.selectNext()
                if Parser.tokenizer.next.type != 'SINGLE_COLON':
                    sys.stderr.write(
                        'Expected SINGLE_COLON token on parseStatement')
                    sys.exit(1)
                Parser.tokenizer.selectNext()
                runway = Parser.parseRelExpression()
                if Parser.tokenizer.next.type != 'COMMA':
                    sys.stderr.write(
                        'Expected COMMA token on parseStatement')
                    sys.exit(1)
                Parser.tokenizer.selectNext()
                if Parser.tokenizer.next.type != 'STRING' and Parser.tokenizer.next.value != 'FLAPS':
                    sys.stderr.write(
                        'Expected STRING token on parseStatement LAND5')
                    sys.exit(1)
                Parser.tokenizer.selectNext()
                if Parser.tokenizer.next.type != 'SINGLE_COLON':
                    sys.stderr.write(
                        'Expected SINGLE_COLON token on parseStatement')
                    sys.exit(1)
                Parser.tokenizer.selectNext()
                flaps = Parser.parseRelExpression()
                if Parser.tokenizer.next.type != 'COMMA':
                    sys.stderr.write(
                        'Expected COMMA token on parseStatement')
                    sys.exit(1)
                Parser.tokenizer.selectNext()
                if Parser.tokenizer.next.type != 'STRING' and Parser.tokenizer.next.value != 'SPEED':
                    sys.stderr.write(
                        'Expected STRING token on parseStatement LAND6')
                    sys.exit(1)
                Parser.tokenizer.selectNext()
                if Parser.tokenizer.next.type != 'SINGLE_COLON':
                    sys.stderr.write(
                        'Expected SINGLE_COLON token on parseStatement')
                    sys.exit(1)
                Parser.tokenizer.selectNext()
                speed = Parser.parseRelExpression()
                if Parser.tokenizer.next.type != 'COMMA':
                    sys.stderr.write(
                        'Expected COMMA token on parseStatement')
                    sys.exit(1)
                Parser.tokenizer.selectNext()
                if Parser.tokenizer.next.type != 'STRING' and Parser.tokenizer.next.value != 'ALTITUDE':
                    sys.stderr.write(
                        'Expected STRING token on parseStatement LAND7')
                    sys.exit(1)
                Parser.tokenizer.selectNext()
                if Parser.tokenizer.next.type != 'SINGLE_COLON':
                    sys.stderr.write(
                        'Expected SINGLE_COLON token on parseStatement')
                    sys.exit(1)
                Parser.tokenizer.selectNext()
                altitude = Parser.parseRelExpression()
                if Parser.tokenizer.next.type != 'RBRACE':
                    sys.stderr.write(
                        'Expected RBRACE token on parseStatement')
                    sys.exit(1)
                Parser.tokenizer.selectNext()
                if Parser.tokenizer.next.type != 'NEWLINE':
                    sys.stderr.write(
                        'Expected NEWLINE token on parseStatement')
                    sys.exit(1)
                return Land("", [aircraft, runway, flaps, speed, altitude])

        elif Parser.tokenizer.next.type == 'WAYPOINT':
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type == 'LBRACE':
                Parser.tokenizer.selectNext()
                if Parser.tokenizer.next.type != 'STRING' and Parser.tokenizer.next.value != 'WP_NAME':
                    sys.stderr.write(
                        'Expected STRING token on parseStatement WAYPOINT1')
                    sys.exit(1)
                Parser.tokenizer.selectNext()
                if Parser.tokenizer.next.type != 'SINGLE_COLON':
                    sys.stderr.write(
                        'Expected SINGLE_COLON token on parseStatement')
                    sys.exit(1)
                Parser.tokenizer.selectNext()
                waypointName = Parser.parseRelExpression()
                if Parser.tokenizer.next.type != 'COMMA':
                    sys.stderr.write(
                        'Expected COMMA token on parseStatement')
                    sys.exit(1)
                Parser.tokenizer.selectNext()
                if Parser.tokenizer.next.type != 'STRING' and Parser.tokenizer.next.value != 'SPEED':
                    sys.stderr.write(
                        'Expected STRING token on parseStatement WAYPOINT3')
                    sys.exit(1)
                Parser.tokenizer.selectNext()
                if Parser.tokenizer.next.type != 'SINGLE_COLON':
                    sys.stderr.write(
                        'Expected SINGLE_COLON token on parseStatement')
                    sys.exit(1)
                Parser.tokenizer.selectNext()
                speed = Parser.parseRelExpression()
                if Parser.tokenizer.next.type != 'COMMA':
                    sys.stderr.write(
                        'Expected COMMA token on parseStatement')
                    sys.exit(1)
                Parser.tokenizer.selectNext()
                if Parser.tokenizer.next.type != 'STRING' and Parser.tokenizer.next.value != 'ALTITUDE':
                    sys.stderr.write(
                        'Expected STRING token on parseStatement WAYPOINT4')
                    sys.exit(1)
                Parser.tokenizer.selectNext()
                if Parser.tokenizer.next.type != 'SINGLE_COLON':
                    sys.stderr.write(
                        'Expected SINGLE_COLON token on parseStatement')
                    sys.exit(1)
                Parser.tokenizer.selectNext()
                altitude = Parser.parseRelExpression()
                if Parser.tokenizer.next.type != 'RBRACE':
                    sys.stderr.write(
                        'Expected RBRACE token on parseStatement')
                    sys.exit(1)
                Parser.tokenizer.selectNext()
                if Parser.tokenizer.next.type != 'NEWLINE':
                    sys.stderr.write(
                        'Expected NEWLINE token on parseStatement')
                    sys.exit(1)
                return Waypoint(waypointName, [waypointName, speed, altitude])

        elif Parser.tokenizer.next.type == 'TAKEOFF':
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type == 'LBRACE':
                Parser.tokenizer.selectNext()
                if Parser.tokenizer.next.type != 'STRING' and Parser.tokenizer.next.value != 'AIRCRAFT':
                    sys.stderr.write(
                        'Expected STRING token on parseStatement TAKEOFF1')
                    sys.exit(1)
                Parser.tokenizer.selectNext()
                if Parser.tokenizer.next.type != 'SINGLE_COLON':
                    sys.stderr.write(
                        'Expected SINGLE_COLON token on parseStatement')
                    sys.exit(1)
                Parser.tokenizer.selectNext()
                aircraft = Parser.parseRelExpression()
                if Parser.tokenizer.next.type != 'COMMA':
                    sys.stderr.write(
                        'Expected COMMA token on parseStatement')
                    sys.exit(1)
                Parser.tokenizer.selectNext()
                if Parser.tokenizer.next.type != 'STRING' and Parser.tokenizer.next.value != 'RUNWAY':
                    sys.stderr.write(
                        'Expected STRING token on parseStatement TAKEOFF3')
                    sys.exit(1)
                Parser.tokenizer.selectNext()
                if Parser.tokenizer.next.type != 'SINGLE_COLON':
                    sys.stderr.write(
                        'Expected SINGLE_COLON token on parseStatement')
                    sys.exit(1)
                Parser.tokenizer.selectNext()
                runway = Parser.parseRelExpression()
                if Parser.tokenizer.next.type != 'COMMA':
                    sys.stderr.write(
                        'Expected COMMA token on parseStatement')
                    sys.exit(1)
                Parser.tokenizer.selectNext()
                if Parser.tokenizer.next.type != 'STRING' and Parser.tokenizer.next.value != 'FLAPS':
                    sys.stderr.write(
                        'Expected STRING token on parseStatement TAKEOFF5')
                    sys.exit(1)
                Parser.tokenizer.selectNext()
                if Parser.tokenizer.next.type != 'SINGLE_COLON':
                    sys.stderr.write(
                        'Expected SINGLE_COLON token on parseStatement')
                    sys.exit(1)
                Parser.tokenizer.selectNext()
                flaps = Parser.parseRelExpression()
                if Parser.tokenizer.next.type != 'COMMA':
                    sys.stderr.write(
                        'Expected COMMA token on parseStatement')
                    sys.exit(1)
                Parser.tokenizer.selectNext()
                if Parser.tokenizer.next.type != 'STRING' and Parser.tokenizer.next.value != 'SPEED':
                    sys.stderr.write(
                        'Expected STRING token on parseStatement TAKEOFF6')
                    sys.exit(1)
                Parser.tokenizer.selectNext()
                if Parser.tokenizer.next.type != 'SINGLE_COLON':
                    sys.stderr.write(
                        'Expected SINGLE_COLON token on parseStatement')
                    sys.exit(1)
                Parser.tokenizer.selectNext()
                speed = Parser.parseRelExpression()
                if Parser.tokenizer.next.type != 'COMMA':
                    sys.stderr.write(
                        'Expected COMMA token on parseStatement')
                    sys.exit(1)
                Parser.tokenizer.selectNext()
                if Parser.tokenizer.next.type != 'STRING' and Parser.tokenizer.next.value != 'ALTITUDE':
                    sys.stderr.write(
                        'Expected STRING token on parseStatement TAKEOFF7')
                    sys.exit(1)
                Parser.tokenizer.selectNext()
                if Parser.tokenizer.next.type != 'SINGLE_COLON':
                    sys.stderr.write(
                        'Expected SINGLE_COLON token on parseStatement')
                    sys.exit(1)
                Parser.tokenizer.selectNext()
                altitude = Parser.parseRelExpression()
                if Parser.tokenizer.next.type != 'RBRACE':
                    sys.stderr.write(
                        'Expected RBRACE token on parseStatement')
                    sys.exit(1)
                Parser.tokenizer.selectNext()
                if Parser.tokenizer.next.type != 'NEWLINE':
                    sys.stderr.write(
                        'Expected NEWLINE token on parseStatement')
                    sys.exit(1)
                return Takeoff("", [aircraft, runway, flaps, speed, altitude])

        elif Parser.tokenizer.next.type == 'MATH_FUNCTION':
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type == 'LPAREN':
                Parser.tokenizer.selectNext()
                expression = Parser.parseRelExpression()
                if Parser.tokenizer.next.type == 'COMMA':
                    Parser.tokenizer.selectNext()
                    expression2 = Parser.parseRelExpression()
                    expression = [expression, expression2]
                    math_function = MathFunc(
                        Parser.tokenizer.next.value, expression)
                    if Parser.tokenizer.next.type != 'RPAREN':
                        sys.stderr.write(
                            'Expected RPAREN token on parseStatement')
                        sys.exit(1)
                    Parser.tokenizer.selectNext()
                    if Parser.tokenizer.next.type != 'NEWLINE':
                        sys.stderr.write(
                            'Expected NEWLINE token on parseStatement')
                        sys.exit(1)
                    return math_function
                else:
                    if Parser.tokenizer.next.type != 'RPAREN':
                        sys.stderr.write(
                            'Expected RPAREN token on parseStatement')
                        sys.exit(1)
                    Parser.tokenizer.selectNext()
                    if Parser.tokenizer.next.type != 'NEWLINE':
                        sys.stderr.write(
                            'Expected NEWLINE token on parseStatement')
                        sys.exit(1)
                    return MathFunc(Parser.tokenizer.next.value, expression)

            else:
                sys.stderr.write(
                    'Expected LPAREN token on parseStatement math func')
                sys.exit(1)

        elif Parser.tokenizer.next.type == 'WHILE':
            Parser.tokenizer.selectNext()
            expression = Parser.parseRelExpression()
            if Parser.tokenizer.next.type != 'NEWLINE':
                sys.stderr.write(
                    'Expected NEWLINE token on parseStatement while')
                sys.exit(1)
            Parser.tokenizer.selectNext()
            statements_nodes = []
            while Parser.tokenizer.next.type != 'END':
                statements_nodes.append(Parser.parseStatement())
                Parser.tokenizer.selectNext()
            return While("", [expression, Block("", statements_nodes)])
        elif Parser.tokenizer.next.type == 'IF':
            Parser.tokenizer.selectNext()
            expression = Parser.parseRelExpression()
            if Parser.tokenizer.next.type != 'NEWLINE':
                sys.stderr.write('Expected NEWLINE token on parseStatement if')
                sys.exit(1)
            Parser.tokenizer.selectNext()
            statements_nodes = []
            while Parser.tokenizer.next.type != 'END' and Parser.tokenizer.next.type != 'ELSE':
                statements_nodes.append(Parser.parseStatement())
                Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type == 'ELSE':
                Parser.tokenizer.selectNext()
                if Parser.tokenizer.next.type != 'NEWLINE':
                    sys.stderr.write(
                        'Expected NEWLINE token on parseStatement else')
                    sys.exit(1)
                Parser.tokenizer.selectNext()
                statements_nodes_2 = []
                while Parser.tokenizer.next.type != 'END':
                    statements_nodes_2.append(Parser.parseStatement())
                    Parser.tokenizer.selectNext()
                return If("", [expression, Block("", statements_nodes), Block("", statements_nodes_2)])
            else:
                return If("", [expression, Block("", statements_nodes), NoOp("", [])])
        elif Parser.tokenizer.next.type == 'NEWLINE':
            return NoOp("", [])
        else:
            sys.stderr.write(
                'Expected IDENTIFIER or PRINTLN token on parseStatement')
            sys.exit(1)

    @staticmethod
    def parseBlock():
        Parser.tokenizer.selectNext()
        statements_nodes = []
        while Parser.tokenizer.next.type != 'EOF':
            statements_nodes.append(Parser.parseStatement())
            Parser.tokenizer.selectNext()
        return Block("", statements_nodes)

    @staticmethod
    def run(code: str):
        Parser.tokenizer = Tokenizer(PrePro.filter(code), 0, None)
        result = Parser.parseBlock()

        if Parser.tokenizer.next.type != 'EOF':
            sys.stderr.write('No EOF')
            sys.exit(1)
        result.Evaluate(symbolTable)


class PrePro:
    @staticmethod
    def filter(code: str):
        code = re.sub(re.compile("#.*"), '', code)
        return code


if __name__ == '__main__':
    if len(sys.argv) == 2:
        with open(sys.argv[1], 'r') as f:
            code = f.read()
        Parser.run(code)
    elif len(sys.argv) == 1:
        sys.stderr.write("No code provided")
        sys.exit(1)
    else:
        sys.stderr.write("Too many arguments")
        sys.exit(1)
