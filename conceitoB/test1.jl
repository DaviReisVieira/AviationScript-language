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
