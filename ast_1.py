class SymbolTable():
    def __init__(self):
        self.table = {}

    def __getitem__(self, key):
        return self.table[key]

    def __setitem__(self, key, value):
        self.table[key] = value

    def __contains__(self, key):
        return key in self.table

    def __str__(self):
        return str(self.table)

    def __repr__(self):
        return str(self.table)

    def __len__(self):
        return len(self.table)


symbol_table = SymbolTable()


class Node():
    def __init__(self):
        pass

    def eval(self):
        pass


class Statements(Node):
    def __init__(self, statement):
        self.statement = statement

    def add_statement(self, statement):
        self.statement.append(statement)

    def eval(self):
        for statement in self.statement:
            statement.eval()


class Assignment(Node):
    def __init__(self, variable, value):
        self.variable = variable
        self.value = value

    def eval(self):
        return self.value.eval()


class Number(Node):
    def __init__(self, value):
        self.value = value

    def eval(self):
        return self.value


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


# make class Object
class Object(Node):
    def __init__(self, properties):
        self.properties = properties

    def eval(self):
        return self.properties.eval()

# class Properties


class Properties(Node):
    def __init__(self, property):
        self.property = property

    def add_property(self, property):
        self.property.append(property)

    def eval(self):
        for property in self.property:
            property.eval()

# class Property


class Property(Node):
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def eval(self):
        return self.value.eval()

# class Condition


class Condition(Node):
    def __init__(self, left, right, operator):
        self.left = left
        self.right = right
        self.operator = operator

    def eval(self):
        if self.operator == '==':
            return self.left.eval() == self.right.eval()
        elif self.operator == '!=':
            return self.left.eval() != self.right.eval()
        elif self.operator == '>':
            return self.left.eval() > self.right.eval()
        elif self.operator == '<':
            return self.left.eval() < self.right.eval()
        elif self.operator == '>=':
            return self.left.eval() >= self.right.eval()
        elif self.operator == '<=':
            return self.left.eval() <= self.right.eval()
        elif self.operator == '&&':
            return self.left.eval() and self.right.eval()
        elif self.operator == '||':
            return self.left.eval() or self.right.eval()
        else:
            raise Exception('Error: unknown operator {}'.format(self.operator))

# class If


class If(Node):
    def __init__(self, condition, statements):
        self.condition = condition
        self.statements = statements

    def eval(self):
        # if condition is true, execute statements
        if self.condition.eval():
            self.statements.eval()

# class IfElse


class IfElse(Node):
    def __init__(self, condition, statements1, statements2):
        self.condition = condition
        self.statements1 = statements1
        self.statements2 = statements2

    def eval(self):
        # if condition is true, execute statements1
        if self.condition.eval():
            self.statements1.eval()
        # if condition is false, execute statements2
        else:
            self.statements2.eval()

# class  Loop(p[1].getstr(), p[3], p[5], p[7])


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
            self.variable.value = i
            self.statements.eval()

# class Function


class Function(Node):
    def __init__(self, name, parameters, statements):
        self.name = name
        self.parameters = parameters
        self.statements = statements

    def eval(self):
        # add function to symbol table
        symbol_table[self.name] = self

    def call(self, arguments):
        # check if number of arguments matches number of parameters
        if len(arguments) != len(self.parameters):
            raise Exception(
                'Error: number of arguments does not match number of parameters')

        # add arguments to symbol table
        for i in range(len(arguments)):
            symbol_table[self.parameters[i]] = arguments[i]

        # execute function statements
        self.statements.eval()


class Println(Node):
    # class node
    def __init__(self, value):
        self.value = value

    def eval(self):
        # print value
        print(self.value.eval())


class Operation(Node):
    pass


class Expression(Node):
    pass


class FunctionCall(Node):
    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments

    def eval(self):
        # check if function exists
        if self.name not in symbol_table:
            raise Exception(
                'Error: function {} does not exist'.format(self.name))

        # get function from symbol table
        function = symbol_table[self.name]

        # call function
        function.call(self.arguments.eval())


class Arguments(Node):
    def __init__(self, argument):
        self.argument = argument

    def add_argument(self, argument):
        self.argument.append(argument)

    def eval(self):
        arguments = []
        for argument in self.argument:
            arguments.append(argument.eval())
        return arguments
