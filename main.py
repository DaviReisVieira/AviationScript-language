from lexerling import Lexer
from parserling import Parser

text_input = """
LET i = 0
FOR i = 0 TO 10 DO
    PRINTLN(i)
END
"""

lexer = Lexer().get_lexer()
tokens = lexer.lex(text_input)


def token_generator(token_list):
    for token in token_list:
        # print(token)
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
