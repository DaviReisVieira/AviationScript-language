
import sys
import math
import numpy as np


class SymbolTable:
    def __init__(self):
        self.table = {
            'PI': math.pi,
        }

    def add(self, name):
        if name not in self.table:
            self.table[name] = None

    def get(self, name):
        if name in self.table:
            return self.table[name]
        else:
            sys.exit("Error: variable not defined")

    def setter(self, name, value):
        if name in self.table:
            self.table[name] = value
        else:
            sys.exit("Error: variable not defined")


symbolTable = SymbolTable()


class Node():
    def __init__(self):
        pass

    def eval(self):
        pass


class Statements(Node):
    def __init__(self, statement):
        self.statements = [statement]

    def add_statement(self, statement):
        self.statements.append(statement)

    def eval(self):
        for statement in self.statements:
            statement.eval()


class Assignment(Node):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def eval(self):
        symbolTable.setter(self.name, self.value.eval())


class Variable(Node):
    def __init__(self, name):
        self.name = name

    def eval(self):
        symbolTable.add(self.name)
        return self.name


class Identifier(Node):
    def __init__(self, name):
        self.name = name

    def eval(self):
        return symbolTable.get(self.name)


class Println():
    def __init__(self, value):
        self.value = value

    def eval(self):
        print(self.value.eval())


class Number():
    def __init__(self, value):
        self.value = value

    def eval(self):
        value = float(self.value)
        if value.is_integer():
            return int(value)
        else:
            return value


class String(Node):
    def __init__(self, value):
        self.value = value

    def eval(self):
        return self.value


class Boolean(Node):
    def __init__(self, value):
        self.value = value

    def eval(self):
        return self.value


class Object(Node):
    def __init__(self, properties):
        self.properties = properties

    def eval(self):
        properties = {}
        for property in self.properties:
            properties[property.name] = property.value
        return properties


class Property(Node):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def eval(self):
        return self.value.eval()


class BinOp(Node):
    def __init__(self, operator, left, right):
        self.left = left
        self.right = right
        self.operator = operator

    def eval(self):
        if self.operator.gettokentype() == 'PLUS':
            return self.left.eval() + self.right.eval()
        elif self.operator.gettokentype() == 'MINUS':
            return self.left.eval() - self.right.eval()
        elif self.operator.gettokentype() == 'TIMES':
            return self.left.eval() * self.right.eval()
        elif self.operator.gettokentype() == 'DIVIDE':
            return self.left.eval() / self.right.eval()
        elif self.operator.gettokentype() == 'EQUAL_EQUAL':
            if self.left.eval() == self.right.eval():
                return True
            else:
                return False
        elif self.operator.gettokentype() == 'NOT_EQUAL':
            if self.left.eval() != self.right.eval():
                return True
            else:
                return False
        elif self.operator.gettokentype() == 'GREATER_THAN':
            if self.left.eval() > self.right.eval():
                return True
            else:
                return False
        elif self.operator.gettokentype() == 'GREATER_THAN_EQUAL':
            if self.left.eval() >= self.right.eval():
                return True
            else:
                return False
        elif self.operator.gettokentype() == 'LESS_THAN':
            if self.left.eval() < self.right.eval():
                return True
            else:
                return False
        elif self.operator.gettokentype() == 'LESS_THAN_EQUAL':
            if self.left.eval() <= self.right.eval():
                return True
            else:
                return False
        else:
            sys.exit("Error: unknown operator")


class UnOp(Node):
    def __init__(self, operator, right):
        self.right = right
        self.operator = operator

    def eval(self):
        if self.operator.gettokentype() == 'PLUS':
            return self.right.eval()
        elif self.operator.gettokentype() == 'MINUS':
            return -self.right.eval()
        else:
            sys.exit("Error: unknown operator")


class MathFunction(UnOp):
    def __init__(self, operator, right):
        self.right = right
        self.operator = operator

    def eval(self):
        if self.operator.gettokentype() == 'SIN':
            return math.sin(self.right.eval())
        elif self.operator.gettokentype() == 'COS':
            return math.cos(self.right.eval())
        elif self.operator.gettokentype() == 'TAN':
            return math.tan(self.right.eval())
        elif self.operator.gettokentype() == 'ASIN':
            return math.asin(self.right.eval())
        elif self.operator.gettokentype() == 'ACOS':
            return math.acos(self.right.eval())
        elif self.operator.gettokentype() == 'ATAN':
            return math.atan(self.right.eval())
        elif self.operator.gettokentype() == 'SINH':
            return math.sinh(self.right.eval())
        elif self.operator.gettokentype() == 'COSH':
            return math.cosh(self.right.eval())
        elif self.operator.gettokentype() == 'TANH':
            return math.tanh(self.right.eval())
        elif self.operator.gettokentype() == 'ASINH':
            return math.asinh(self.right.eval())
        elif self.operator.gettokentype() == 'ACOSH':
            return math.acosh(self.right.eval())
        elif self.operator.gettokentype() == 'ATANH':
            return math.atanh(self.right.eval())
        elif self.operator.gettokentype() == 'EXP':
            return math.exp(self.right.eval())
        elif self.operator.gettokentype() == 'LOG':
            return math.log(self.right.eval())
        elif self.operator.gettokentype() == 'LOG10':
            return math.log10(self.right.eval())
        elif self.operator.gettokentype() == 'SQRT':
            return math.sqrt(self.right.eval())
        elif self.operator.gettokentype() == 'CBRT':
            return math.cbrt(self.right.eval())
        elif self.operator.gettokentype() == 'CEIL':
            return math.ceil(self.right.eval())
        elif self.operator.gettokentype() == 'FLOOR':
            return math.floor(self.right.eval())
        elif self.operator.gettokentype() == 'ABS':
            return abs(self.right.eval())
        elif self.operator.gettokentype() == 'ROUND':
            return round(self.right.eval())
        elif self.operator.gettokentype() == 'TRUNC':
            return math.trunc(self.right.eval())
        elif self.operator.gettokentype() == 'SIGNUM':
            return math.signum(self.right.eval())
        elif self.operator.gettokentype() == 'RINT':
            return math.rint(self.right.eval())
        elif self.operator.gettokentype() == 'MIN':
            return min(self.right.eval())
        elif self.operator.gettokentype() == 'MAX':
            return max(self.right.eval())
        elif self.operator.gettokentype() == 'RANDOM':
            return math.random(self.right.eval())


class Factor(Node):
    def __init__(self, operator, right):
        self.right = right
        self.operator = operator

    def eval(self):
        if self.operator.gettokentype() == 'MINUS':
            return -self.right.eval()
        else:
            sys.exit("Error: unknown operator")


class If(Node):
    def __init__(self, condition, statements):
        self.condition = condition
        self.statements = statements

    def eval(self):
        if self.condition.eval():
            self.statements.eval()


class IfElse(Node):
    def __init__(self, condition, statements1, statements2):
        self.condition = condition
        self.statements1 = statements1
        self.statements2 = statements2

    def eval(self):
        if self.condition.eval():
            self.statements1.eval()
        else:
            self.statements2.eval()


class Loop(Node):
    def __init__(self, variable, start, end, statements):
        self.variable = variable
        self.start = start
        self.end = end
        self.statements = statements

    def eval(self):
        # check if start and end are numbers
        if not isinstance(self.start.eval(), int):
            raise Exception('Error: start value of loop must be a number')
        if not isinstance(self.end.eval(), int):
            raise Exception('Error: end value of loop must be a number')

        # check if start is less than end
        if self.start.eval() > self.end.eval():
            raise Exception(
                'Error: start value of loop must be less than end value')

        # loop through statements
        for i in range(self.start.eval(), self.end.eval() + 1):
            symbolTable.setter(self.variable.name, i)
            self.statements.eval()


class Takeoff(Node):
    def __init__(self, aircraft, runway, flaps, speed, altitude):
        self.aircraft = aircraft
        self.runway = runway
        self.flaps = flaps
        self.speed = speed
        self.altitude = altitude

    def eval(self):
        print("Takeoff: " + self.aircraft.name + " " + self.runway.name + " " + str(self.flaps.eval()) + " " + str(
            self.speed.eval()) + " " + str(self.altitude.eval()))


class Land(Node):
    def __init__(self, aircraft, runway, flaps, speed, altitude):
        self.aircraft = aircraft
        self.runway = runway
        self.flaps = flaps
        self.speed = speed
        self.altitude = altitude

    def eval(self):
        print("Land: " + self.aircraft.name + " " + self.runway.name + " " + str(self.flaps.eval()) + " " + str(
            self.speed.eval()) + " " + str(self.altitude.eval()))


class Waypoint(Node):
    def __init__(self, name, speed, altitude):
        self.name = name
        self.speed = speed
        self.altitude = altitude

    def eval(self):
        print("Waypoint: " + self.name.name + " " +
              str(self.speed.eval()) + " " + str(self.altitude.eval()))
