from math import pi, sin, cos, tan, sqrt

rad2deg = 180.0 / pi
EquatorialRadius = 0
eccentricitySquared = 1

ellipsoid = {
    #  Ellipsoid name, Equatorial Radius, square of eccentricity
    "Airy": (6377563, 0.00667054),
    "Australian National": (6378160, 0.006694542),
    "Bessel 1841": (6377397, 0.006674372),
    "Bessel 1841 (Nambia] ": (6377484, 0.006674372),
    "Clarke 1866": (6378206, 0.006768658),
    "Clarke 1880": (6378249, 0.006803511),
    "Everest": (6377276, 0.006637847),
    "Fischer 1960 (Mercury] ": (6378166, 0.006693422),
    "Fischer 1968": (6378150, 0.006693422),
    "GRS 1967": (6378160, 0.006694605),
    "GRS 1980": (6378137, 0.00669438),
    "Helmert 1906": (6378200, 0.006693422),
    "Hough": (6378270, 0.00672267),
    "International": (6378388, 0.00672267),
    "Krassovsky": (6378245, 0.006693422),
    "Modified Airy": (6377340, 0.00667054),
    "Modified Everest": (6377304, 0.006637847),
    "Modified Fischer 1960": (6378155, 0.006693422),
    "South American 1969": (6378160, 0.006694542),
    "WGS 60": (6378165, 0.006693422),
    "WGS 66": (6378145, 0.006694542),
    "WGS-72": (6378135, 0.006694318),
    "WGS-84": (6378137, 0.00669438)
}

def UTMtoLL(ReferenceEllipsoid, northing, easting, zone,):

    # converts UTM coords to lat/long.  Equations from USGS Bulletin 1532
    # East Longitudes are positive, West longitudes are negative.
    # North latitudes are positive, South latitudes are negative
    # Lat and Long are in decimal degrees.
    # Written by Chuck Gantz- chuck.gantz@globalstar.com
    # Converted to Python by Russ Nelson <nelson@crynwr.com>

    k0 = 0.9996
    for i in range(len(ellipsoid)):
        if i == int(ReferenceEllipsoid):
            key_elips = list(ellipsoid.keys())[i-1]
    a = ellipsoid[key_elips][EquatorialRadius]
    eccSquared = ellipsoid[key_elips][eccentricitySquared]
    e1 = (1 - sqrt(1 - eccSquared)) / (1 + sqrt(1 - eccSquared))
    # NorthernHemisphere; //1 for northern hemispher, 0 for southern

    x = easting - 500000.0  # remove 500,000 meter offset for longitude
    y = northing

    ZoneLetter = zone[-1]
    ZoneNumber = int(zone[:-1])
    if not ZoneLetter >= 'N':
        y -= 10000000.0         # remove 10,000,000 meter offset used for S

    # +3 puts origin in middle of zone
    LongOrigin = (ZoneNumber - 1) * 6 - 180 + 3

    eccPrimeSquared = (eccSquared) / (1 - eccSquared)

    M = y / k0
    mu = M / (a * (1 - eccSquared / 4 - 3 * eccSquared ** 2 /
                   64 - 5 * eccSquared ** 3 / 256))

    phi1Rad = (mu + (3 * e1 / 2 - 27 * e1 ** 3 / 32) * sin(2 * mu) +
               (21 * e1 * e1 / 16 - 55 * e1 ** 4 / 32) *
               sin(4 * mu) + (151 * e1 ** 3/ 96) * sin(6 * mu))

    N1 = a / sqrt(1 - eccSquared * sin(phi1Rad) ** 2)
    T1 = tan(phi1Rad) ** 2
    C1 = eccPrimeSquared * cos(phi1Rad) ** 2
    R1 = a * (1 - eccSquared) / pow(1 - eccSquared *
                                    sin(phi1Rad) ** 2, 1.5)
    D = x / (N1 * k0)

    Lat = phi1Rad - (N1 * tan(phi1Rad) / R1) *\
        (D * D / 2 -
         (5 + 3 * T1 + 10 * C1 - 4 * C1 ** 2 - 9 * eccPrimeSquared) *
         D ** 4 / 24 + (61 + 90 * T1 + 298 * C1 + 45 * T1 * T1 - 252 *
                               eccPrimeSquared - 3 * C1 ** 2) *
        D ** 6 / 720)
    Lat = Lat * rad2deg

    Long = (D - (1 + 2 * T1 + C1) * D ** 3 / 6 +
            (5 - 2 * C1 + 28 * T1 - 3 * C1 ** 2 + 8 *
             eccPrimeSquared + 24 * T1 ** 2) *
            D ** 5 / 120) / cos(phi1Rad)
    Long = LongOrigin + Long * rad2deg
    return (Lat, Long)

ellips = 23
z = str(6) + "N"
(lat, lon) = UTMtoLL(ellips, 7193122.574733158, 459708.12017047824 , z)  # UTMtoLL(ellipsoid, n, e, z)
print("  UTMtoLL lon / lat = ",lon,lat)
