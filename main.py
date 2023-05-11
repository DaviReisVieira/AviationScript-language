from lexerling import Lexer
from parserling import Parser

text_input = """
LET airport1 = { "name": "Aeroporto de partida", "lat": -23.432, "long": -46.533 }
LET airport2 = { "name": "Aeroporto de chegada", "lat": -22.910, "long": -43.163 }
LET waypoint1 = { "waypointName": "WP1", "lat": -23.356, "long": -46.670, "speed": 250, "altitude": 10000 }
LET waypoint2 = { "waypointName": "WP2", "lat": -23.144, "long": -45.787, "speed": 300, "altitude": 12000 }
LET waypoint3 = { "waypointName": "WP3", "lat": -22.910, "long": -43.163, "speed": 350, "altitude": 13000 }

TAKEOFF { AIRCRAFT "AIT" RUNWAY "09R" FLAPS 1 SPEED 150 ALTITUDE 1000 }
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
