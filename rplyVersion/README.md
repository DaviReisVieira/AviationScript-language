## Language Specification

```lua
program         -> { statement }
statement       -> ( assignment | conditional | loop | operation | function | println )
assignment      -> "LET" variable "=" ( value | object | expression )
value           -> ( number | string | boolean )
object          -> "{" { property } "}"
property        -> key value
key             -> string
conditional     -> "IF" condition "THEN" { statement } ["ELSE" { statement }] "END"
loop            -> "FOR" variable "=" value "TO" value "DO" { statement } "END"
operation       -> ( takeoff | land | waypoint )
takeoff         -> "TAKEOFF" "{" "AIRCRAFT" aircraftName "RUNWAY" runwayName "FLAPS" flapPosition "SPEED" speed "ALTITUDE" altitude "}"
land            -> "LAND" "{" "AIRCRAFT" aircraftName "RUNWAY" runwayName "FLAPS" flapPosition "SPEED" speed "ALTITUDE" altitude "}"
waypoint        -> "WAYPOINT" "{" "WP_NAME" waypointName "SPEED" speed "ALTITUDE" altitude "}"
function        -> "FUNCTION" functionName "(" [ parameter { "," parameter } ] ")" "{" { statement } "}"
println         -> "PRINTLN" "(" expression ")"
functionCall    -> functionName "(" [ expression { "," expression } ] ")"
parameter       -> variable
mathFunction    -> "SIN" | "COS" | "TAN" | "ASIN" | "ACOS" | "ATAN" | "SINH" | "COSH" | "TANH" | "ASINH" | "ACOSH" | "ATANH" | "EXP" | "LOG" | "LOG10" | "SQRT" | "CBRT" | "CEIL" | "FLOOR" | "ABS" | "ROUND" | "TRUNC" | "SIGNUM" | "RINT" | "MIN" | "MAX" | "RANDOM"

condition       -> ( expression | comparison )
expression      -> term { ( "+" | "-" ) term }
term            -> factor { ( "*" | "/" ) factor }
factor          -> variable | number | functionCall | mathFunction "(" expression ")" | "(" expression ")"
comparison      -> expression ( "==" | "!=" | ">" | "<" | ">=" | "<=" ) expression

variable        -> letter { letter | digit }
number          -> [ "-" ] digit { digit } [ "." digit { digit } ]
string          -> '"' { character } '"'
character       -> letter | digit | " " | "'" | "." | "," | "" | ":" | "?" | "!" | "@" | "#" | "$" | "%" | "^" | "&" | "*" | "(" | ")" | "-" | "_" | "+" | "=" | "[" | "]" | "{" | "}" | "|" | "\" | "/" | "<" | ">" | "`" | "~"
letter          -> ( "A" ... "Z" ) | ( "a" ... "z" )
digit           -> "0" ... "9"

```

A linguagem AviationScript é uma linguagem de programação voltada para definir rotas e instruções para aeronaves. A seguir, apresento alguns exemplos de uso da linguagem para ilustrar como ela pode ser usada na prática:

## Exemplos

### Exemplo 1: Definir uma rota de voo

O seguinte exemplo demonstra como usar a linguagem AviationScript para definir uma rota de voo com três waypoints. A rota começa no aeroporto de partida, passa pelo waypoint 1 e 2 e termina no aeroporto de chegada.

```vbnet
LET airport1 = { "name": "Aeroporto de partida", "lat": -23.432, "long": -46.533 }
LET airport2 = { "name": "Aeroporto de chegada", "lat": -22.910, "long": -43.163 }
LET waypoint1 = { "waypointName": "WP1", "lat": -23.356, "long": -46.670, "speed": 250, "altitude": 10000 }
LET waypoint2 = { "waypointName": "WP2", "lat": -23.144, "long": -45.787, "speed": 300, "altitude": 12000 }
LET waypoint3 = { "waypointName": "WP3", "lat": -22.910, "long": -43.163, "speed": 350, "altitude": 13000 }

TAKEOFF { "AIRCRAFT": "Boeing 737", "RUNWAY": "RWY 27", "FLAPS": 10, "SPEED": 200, "ALTITUDE": 5000 }

WAYPOINT { "WP_NAME": waypoint1.waypointName, "SPEED": waypoint1.speed, "ALTITUDE": waypoint1.altitude }
WAYPOINT { "WP_NAME": waypoint2.waypointName, "SPEED": waypoint2.speed, "ALTITUDE": waypoint2.altitude }
WAYPOINT { "WP_NAME": waypoint3.waypointName, "SPEED": waypoint3.speed, "ALTITUDE": waypoint3.altitude }

LAND { "AIRCRAFT": "Boeing 737", "RUNWAY": "RWY 09", "FLAPS": 20, "SPEED": 150, "ALTITUDE": 5000 }
```

Neste exemplo, a rota começa no aeroporto de partida (airport1), passa pelos waypoints 1, 2 e 3 e termina no aeroporto de chegada (airport2). A rota é definida usando os comandos "WAYPOINT", que especifica a localização do waypoint, bem como a velocidade e altitude em que deve ser atingido. Os comandos "TAKEOFF" e "LAND" são usados para especificar as configurações do avião para decolagem e pouso.

### Exemplo 2: Definir uma função para calcular a distância entre dois pontos

```vbnet
LET altitude = 10000
LET targetAltitude = 20000
LET climbRate = 500
LET timeToClimb = (targetAltitude - altitude) / climbRate

FOR t = 0 TO timeToClimb DO
{
  LET altitude = altitude + climbRate * t
  WAYPOINT { WP_NAME "Climbing to " targetAltitude "ft" SPEED 250 ALTITUDE altitude }
}

WAYPOINT { WP_NAME "Cruising at " targetAltitude "ft" SPEED 450 ALTITUDE targetAltitude }
```

Neste exemplo, estamos modelando o comportamento de uma aeronave subindo até uma altitude alvo de 20.000 pés. Primeiro, definimos as variáveis altitude, targetAltitude, climbRate e timeToClimb para representar a altitude atual da aeronave, a altitude alvo, a taxa de subida desejada e o tempo estimado para chegar à altitude alvo. Usando um loop FOR, simulamos a subida da aeronave, atualizando a altitude em cada etapa e adicionando um ponto de passagem (waypoint) para a altitude atual em cada iteração. Finalmente, adicionamos outro waypoint para a altitude alvo, indicando que a aeronave está agora em cruzeiro.

## Exemplo 3: Definir uma função para calcular a distância entre dois pontos

```vbnet
FUNCTION calculateDistance(lat1, lon1, lat2, lon2) {
  const R = 6371 // raio médio da Terra em km
  const lat1Rad = lat1 * PI / 180
  const lat2Rad = lat2 * PI / 180
  const deltaLat = (lat2 - lat1) * PI / 180
  const deltaLon = (lon2 - lon1) * PI / 180
  const a = sin(deltaLat / 2) * sin(deltaLat / 2) + cos(lat1Rad) * cos(lat2Rad) * sin(deltaLon / 2) * sin(deltaLon / 2)
  const c = 2 * atan2(sqrt(a), sqrt(1 - a))
  const distance = R * c
  RETURN distance
}
```

## Exemplo 4: Definir uma função para converter Knots para Km/h

```vbnet
FUNCTION convertKnotsToKmPerHour(knots) {
  const kmPerHour = knots * 1.852
  RETURN kmPerHour
}
```

## Exemplo 5: Definir uma função para converter Pés para Metros

```vbnet
FUNCTION convertFeetToMeters(feet) {
  const meters = feet * 0.3048
  RETURN meters
}
```

## Exemplo 6: Definir uma função para calcular Heading

```vbnet
FUNCTION calculateHeading(lat1, lon1, lat2, lon2) {
  const lat1Rad = lat1 * PI / 180
  const lat2Rad = lat2 * PI / 180
  const deltaLon = (lon2 - lon1) * PI / 180
  const y = sin(deltaLon) * cos(lat2Rad)
  const x = cos(lat1Rad) * sin(lat2Rad) - sin(lat1Rad) * cos(lat2Rad) * cos(deltaLon)
  const heading = atan2(y, x) * 180 / PI
  RETURN heading
}
```
