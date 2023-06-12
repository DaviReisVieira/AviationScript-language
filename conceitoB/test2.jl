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

println("Distance: ")

lat1::Float = -23.432
lon1::Float = -46.533
lat2::Float = -22.910
lon2::Float = -43.163
println(calculateDistance(lat1, lon1, lat2, lon2))

function convertKnotsToKmPerHour(knots::Float)::Float
    kmPerHour::Float
    kmPerHour = knots * 1.852
    return kmPerHour
end

println("Knots to km/h: ")

knots::Float = 10.0
println(convertKnotsToKmPerHour(knots))

function convertFeetToMeters(feet::Float)::Float
    meters::Float = feet * 0.3048
    return meters
end

println("Feet to meters: ")

altitudeInFeets::Float = 10.0
println(convertFeetToMeters(altitudeInFeets))

function calculateHeading(lat1::Float, lon1::Float, lat2::Float, lon2::Float)::Float
    lat1Rad::Float = lat1 * PI / 180
    lat2Rad::Float = lat2 * PI / 180
    deltaLon::Float = (lon2 - lon1) * PI / 180
    y::Float = sin(deltaLon) * cos(lat2Rad)
    x::Float = cos(lat1Rad) * sin(lat2Rad) - sin(lat1Rad) * cos(lat2Rad) * cos(deltaLon)
    heading::Float = atan2(y, x) * 180 / PI
    return y
end


println("Heading: ")
println(calculateHeading(lat1, lon1, lat2, lon2))
