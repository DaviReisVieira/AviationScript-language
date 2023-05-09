from lexerling import Lexer
from parserling import Parser

text_input = """
LET altitude = 10000
LET targetAltitude = 20000
LET climbRate = 500
LET timeToClimb = (targetAltitude - altitude) / climbRate
LET t = 0
FOR t = 0 TO 10 DO
  LET altitude = altitude + climbRate * t
  PRINTLN(altitude)
END
"""

lexer = Lexer().get_lexer()
tokens = lexer.lex(text_input)


def token_generator(token_list):
    for token in token_list:
        yield token


# Remova a parte que adiciona o token de final de arquivo ($end)
tokens = list(filter(lambda t: t.gettokentype() != '$end', tokens))

tokens = token_generator(tokens)

# for token in tokens:
#     print(token.gettokentype(), token.value)

print('-' * 50)
pg = Parser()
pg.parse()
parser = pg.get_parser()
parser.parse(tokens).eval()
