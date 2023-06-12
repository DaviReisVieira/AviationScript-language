# AviationScript Language

## Introdução

A linguagem _AviationScript_ permite a definição de aeronaves e rotas, bem como a execução de operações de voo.

## Desenvolvedor

Davi Reis Vieira de Souza

## Entregas parciais

- [x] 27/Mar/2023: Linguagem estruturada segundo a EBNF

- [x] 08/Mai/2023: Análise Léxica e Sintática (sem análise semântica e compilação)

## Entrega 1

A entrega 1 consiste na definição da linguagem AviationScript, que é uma linguagem de programação voltada para definir rotas e instruções para aeronaves.

## Entrega 2

A entrega 2 consiste na implementação da análise léxica e sintática da linguagem AviationScript. Estas duas entregas são pré-requisitos para a implementação da análise semântica e da compilação da linguagem. Elas estão na pasta 'rplyVersion'.

## Entrega Final

Utilizei o compilador realizado durante a disciplina - ConceitoB - para implementar a análise léxica e sintática da linguagem AviationScript. A análise semântica e a compilação foram implementadas utilizando a biblioteca rply, que é uma implementação do PLY para a linguagem Python. A pasta 'rplyVersion' contém a implementação da análise léxica e sintática utilizando a biblioteca rply.

## Language Specification

```lua
BLOCK -> { STATEMENT };

STATEMENT -> ( λ | ASSIGNMENT | PRINT | WHILE | IF | FUNCTION | AVIATION_FUNC | MATH_FUNC | RETURN ), "\n";

ASSIGNMENT -> IDENTIFIER, ( CREATING | SETTING, CALLFUNC );

CREATING -> "::", TYPE, [ "=", RELEXPR ];

TYPE -> "Int" | "Float" | "String";

SETTING -> "=", RELEXPR;

CALLFUNC -> "(", [RELEXPR, {",", RELEXPR}] ,")";

PRINT -> "println", "(", RELEXPR, ")";

WHILE -> RELEXPR, "\n", STATEMENT, "end";

IF -> RELEXPR, "\n", { STATEMENT }, [ "else", "\n", STATEMENT ], "end";

FUNCTION -> "function", IDENTIFIER, "("[PARAMETER], ")", "::", TYPE, "\n", STATEMENT, "end";

MATH_FUNC -> MATH_FUNC_NAME, "(", RELEXPR, ")";

AVIATION_FUNC_NAME -> "takeoff" | "land" | "waypoint";

TAKEOFF -> "takeoff", "{", "aircraft", IDENTIFIER, "runway", IDENTIFIER, "flaps", NUMBER, "speed", NUMBER, "altitude", NUMBER, "}";

LAND -> "land", "{", "aircraft", IDENTIFIER, "runway", IDENTIFIER, "flaps", NUMBER, "speed", NUMBER, "altitude", NUMBER, "}";

WAYPOINT -> "waypoint", "{", "wp_name", IDENTIFIER, "speed", NUMBER, "altitude", NUMBER, "}";

MATH_FUNC_NAME -> 'sqrt' | 'sin' | 'cos' | 'tan' | 'atan2' | 'log' | 'exp' | 'abs' | 'pow';

PARAMETER -> IDENTIFIER, "::", TYPE, {",", IDENTIFIER, "::", TYPE};

RETURN -> "return", RELEXPR;

RELEXPR -> EXPRESSION, { ("==" | ">" | "<"), EXPRESSION };

EXPRESSION -> TERM, { ("+" | "-" | "||" | "."), TERM };

TERM -> FACTOR, { ("*" | "/" | "&&"), FACTOR };

FACTOR -> (("+" | "-" | "!"), FACTOR) | NUMBER | STRING | "(", RELEXPR, ")" | IDENTIFIER, ["(", RELEXPR, {",", RELEXPR} ,")"] | ("READLN", "(", ")") | ("MATH_FUNC_NAME", "(", RELEXPR, {",", RELEXPR} ,")");

IDENTIFIER -> LETTER, { LETTER | DIGIT | "_" };

NUMBER -> DIGIT, { DIGIT };

LETTER -> ( a | ... | z | A | ... | Z );

DIGIT -> ( 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 0 );
```

A linguagem AviationScript é uma linguagem de programação voltada para definir rotas e instruções para aeronaves. A seguir, apresento alguns exemplos de uso da linguagem para ilustrar como ela pode ser usada na prática:

## Exemplos

### Exemplo 1: Definir uma rota de voo

O seguinte exemplo demonstra como usar a linguagem AviationScript para definir uma rota de voo com três waypoints. A rota começa no aeroporto de partida, passa pelo waypoint 1, 2 e 3 e termina no aeroporto de chegada.

```julia
TAKEOFF { "AIRCRAFT": "Boeing 737", "RUNWAY": "RWY 27", "FLAPS": 10, "SPEED": 200, "ALTITUDE": 5000 }

WAYPOINT { "WP_NAME": "VERA", "SPEED": 280, "ALTITUDE": 8000 }
WAYPOINT { "WP_NAME": "DIANO", "SPEED": 450, "ALTITUDE": 10000 }
WAYPOINT { "WP_NAME": "PECEM", "SPEED": 470, "ALTITUDE": 15000 }

LAND { "AIRCRAFT": "Boeing 737", "RUNWAY": "RWY 09", "FLAPS": 20, "SPEED": 150, "ALTITUDE": 5000 }
```

Neste exemplo, a rota começa no aeroporto de partida (airport1), passa pelos waypoints 1, 2 e 3 e termina no aeroporto de chegada (airport2). A rota é definida usando os comandos "WAYPOINT", que especifica a localização do waypoint, bem como a velocidade e altitude em que deve ser atingido. Os comandos "TAKEOFF" e "LAND" são usados para especificar as configurações do avião para decolagem e pouso.

### Exemplo 2: Definir uma função para subida de altitude

```julia
altitude::Float = 10000.0
targetAltitude::Float = 20000.0
climbRate::Float = 500.0
timeToClimb::Float = (targetAltitude - altitude) / climbRate


time::Float = 0.0
t::Float = 1.0
altitudeVar::Float = altitude

while (time < timeToClimb)
    time = time + 1.0
    altitudeVar = altitudeVar + climbRate * t
    WAYPOINT { "WP_NAME": "Climbing To", "SPEED": 250, "ALTITUDE": altitudeVar }
end

WAYPOINT { "WP_NAME": "Cruising at ", "SPEED": 250, "ALTITUDE": targetAltitude }
```

Neste exemplo, estamos modelando o comportamento de uma aeronave subindo até uma altitude alvo de 20.000 pés. Primeiro, definimos as variáveis altitude, targetAltitude, climbRate e timeToClimb para representar a altitude atual da aeronave, a altitude alvo, a taxa de subida desejada e o tempo estimado para chegar à altitude alvo. Usando um loop WHILE, simulamos a subida da aeronave, atualizando a altitude em cada etapa e adicionando um ponto de passagem (waypoint) para a altitude atual em cada iteração. Finalmente, adicionamos outro waypoint para a altitude alvo, indicando que a aeronave está agora em cruzeiro.

## Exemplo 3: Definir uma função para calcular a distância entre dois pontos

```julia
function calculateDistance(lat1::Float, lon1::Float, lat2::Float, lon2::Float)::Float
  R::Int = 6371
  lat1Rad::Float = lat1 * PI / 180
  lat2Rad::Float = lat2 * PI / 180
  deltaLat::Float = (lat2 - lat1) * PI / 180
  deltaLon::Float = (lon2 - lon1) * PI / 180
  a::Float = sin(deltaLat / 2) * sin(deltaLat / 2) + cos(lat1Rad) * cos(lat2Rad) * sin(deltaLon / 2) * sin(deltaLon / 2)
  c::Float = 2 * atan2(sqrt(a), sqrt(1 - a))
  distance::Float = R * c
  return distance
end
```

## Exemplo 4: Definir uma função para converter Knots para Km/h

```julia
function convertKnotsToKmPerHour(knots::Float)::Float
    kmPerHour::Float
    kmPerHour = knots * 1.852
    return kmPerHour
end
```

## Exemplo 5: Definir uma função para converter Pés para Metros

```julia
function convertFeetToMeters(feet::Float)::Float
    meters::Float = feet * 0.3048
    return meters
end
```

## Exemplo 6: Definir uma função para calcular Heading

```julia
function calculateHeading(lat1::Float, lon1::Float, lat2::Float, lon2::Float)::Float
    lat1Rad::Float = lat1 * PI / 180
    lat2Rad::Float = lat2 * PI / 180
    deltaLon::Float = (lon2 - lon1) * PI / 180
    y::Float = sin(deltaLon) * cos(lat2Rad)
    x::Float = cos(lat1Rad) * sin(lat2Rad) - sin(lat1Rad) * cos(lat2Rad) * cos(deltaLon)
    heading::Float = atan2(y, x) * 180 / PI
    return y
end
```
