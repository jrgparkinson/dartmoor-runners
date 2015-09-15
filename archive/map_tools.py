#This code converts british national grid to lat lon

from math import sqrt, pi, sin, cos, tan, atan2 as arctan2
import csv
import re


def OSGB36toWGS84(E,N):
    # From http://www.hannahfry.co.uk/blog/2012/02/01/converting-british-national-grid-to-latitude-and-longitude-ii

    #E, N are the British national grid coordinates - eastings and northings
    a, b = 6377563.396, 6356256.909     #The Airy 180 semi-major and semi-minor axes used for OSGB36 (m)
    F0 = 0.9996012717                   #scale factor on the central meridian
    lat0 = 49*pi/180                    #Latitude of true origin (radians)
    lon0 = -2*pi/180                    #Longtitude of true origin and central meridian (radians)
    N0, E0 = -100000, 400000            #Northing & easting of true origin (m)
    e2 = 1 - (b*b)/(a*a)                #eccentricity squared
    n = (a-b)/(a+b)

    #Initialise the iterative variables
    lat,M = lat0, 0

    while N-N0-M >= 0.00001: #Accurate to 0.01mm
        lat = (N-N0-M)/(a*F0) + lat;
        M1 = (1 + n + (5./4)*n**2 + (5./4)*n**3) * (lat-lat0)
        M2 = (3*n + 3*n**2 + (21./8)*n**3) * sin(lat-lat0) * cos(lat+lat0)
        M3 = ((15./8)*n**2 + (15./8)*n**3) * sin(2*(lat-lat0)) * cos(2*(lat+lat0))
        M4 = (35./24)*n**3 * sin(3*(lat-lat0)) * cos(3*(lat+lat0))
        #meridional arc
        M = b * F0 * (M1 - M2 + M3 - M4)

        #transverse radius of curvature
    nu = a*F0/sqrt(1-e2*sin(lat)**2)

    #meridional radius of curvature
    rho = a*F0*(1-e2)*(1-e2*sin(lat)**2)**(-1.5)
    eta2 = nu/rho-1

    secLat = 1./cos(lat)
    VII = tan(lat)/(2*rho*nu)
    VIII = tan(lat)/(24*rho*nu**3)*(5+3*tan(lat)**2+eta2-9*tan(lat)**2*eta2)
    IX = tan(lat)/(720*rho*nu**5)*(61+90*tan(lat)**2+45*tan(lat)**4)
    X = secLat/nu
    XI = secLat/(6*nu**3)*(nu/rho+2*tan(lat)**2)
    XII = secLat/(120*nu**5)*(5+28*tan(lat)**2+24*tan(lat)**4)
    XIIA = secLat/(5040*nu**7)*(61+662*tan(lat)**2+1320*tan(lat)**4+720*tan(lat)**6)
    dE = E-E0

    #These are on the wrong ellipsoid currently: Airy1830. (Denoted by _1)
    lat_1 = lat - VII*dE**2 + VIII*dE**4 - IX*dE**6
    lon_1 = lon0 + X*dE - XI*dE**3 + XII*dE**5 - XIIA*dE**7

    #Want to convert to the GRS80 ellipsoid. 
    #First convert to cartesian from spherical polar coordinates
    H = 0 #Third spherical coord. 
    x_1 = (nu/F0 + H)*cos(lat_1)*cos(lon_1)
    y_1 = (nu/F0+ H)*cos(lat_1)*sin(lon_1)
    z_1 = ((1-e2)*nu/F0 +H)*sin(lat_1)

    #Perform Helmut transform (to go between Airy 1830 (_1) and GRS80 (_2))
    s = -20.4894*10**-6 #The scale factor -1
    tx, ty, tz = 446.448, -125.157, + 542.060 #The translations along x,y,z axes respectively
    rxs,rys,rzs = 0.1502,  0.2470,  0.8421  #The rotations along x,y,z respectively, in seconds
    rx, ry, rz = rxs*pi/(180*3600.), rys*pi/(180*3600.), rzs*pi/(180*3600.) #In radians
    x_2 = tx + (1+s)*x_1 + (-rz)*y_1 + (ry)*z_1
    y_2 = ty + (rz)*x_1  + (1+s)*y_1 + (-rx)*z_1
    z_2 = tz + (-ry)*x_1 + (rx)*y_1 +  (1+s)*z_1

    #Back to spherical polar coordinates from cartesian
    #Need some of the characteristics of the new ellipsoid    
    a_2, b_2 =6378137.000, 6356752.3141 #The GSR80 semi-major and semi-minor axes used for WGS84(m)
    e2_2 = 1- (b_2*b_2)/(a_2*a_2)   #The eccentricity of the GRS80 ellipsoid
    p = sqrt(x_2**2 + y_2**2)

    #Lat is obtained by an iterative proceedure:   
    lat = arctan2(z_2,(p*(1-e2_2))) #Initial value
    latold = 2*pi
    while abs(lat - latold)>10**-16:
        lat, latold = latold, lat
        nu_2 = a_2/sqrt(1-e2_2*sin(latold)**2)
        lat = arctan2(z_2+e2_2*nu_2*sin(latold), p)

    #Lon and height are then pretty easy
    lon = arctan2(y_2,x_2)
    H = p/cos(lat) - nu_2

    #Uncomment this line if you want to print the results
    #print [(lat-lat_1)*180/pi, (lon - lon_1)*180/pi]

    #Convert to degrees
    lat = lat*180/pi
    lon = lon*180/pi

    #Job's a good'n. 
    return lat, lon

def GR_to_NE( gr ):
    # From https://www.ordnancesurvey.co.uk/business-and-government/help-and-support/web-services/os-openspace/tutorials/bill-chadwick-eastings-and-northings-from-grid-reference.html

    gr = gr.strip().replace( ' ', '' )
    if len(gr) == 0 or len(gr) % 2 == 1 or len(gr) > 12:
        return None, None

    gr = gr.upper()
    if gr[0] not in 'STNOH' or gr[1] == 'I' :
        return None, None

    e = n = 0
    c = gr[0]

    if c == 'T' :
        e = 500000
    elif c == 'N' :
        n = 500000
    elif c == 'O' :
        e = 500000
        n = 500000
    elif c == 'H':
        n = 10000000

    c = ord(gr[1]) - 66
    if c <= 8 : # I
        c += 1

    e += (c % 5) * 100000
    n += (4 - c/5) * 100000

    c = gr[2:]
    try :

        #Get the first half of the gridref
        s = c[:int(len(c)/2)]
        while len(s) < 5 :
            s += '0'

        e += int( s )

        # Get the second half of the gridref
        s = c[-int(len(c)/2):]
        while len(s) < 5 :
            s += '0'

        n += int( s )

    except Exception as e:
        print('Caught exception %s' % e)
        return None,None

    return e,n

# 5x5 grid letters, missing I
alphabet = 'ABCDEFGHJKLMNOPQRSTUVWXYZ'

def grid2xy(false_easting, false_northing, gridsizes, grid_ref):
    '''Convert grid reference to coordinates'''
    # false easting and northing
    easting = -false_easting
    northing = -false_northing

    # convert letter(s) to easting and northing offset
    for n in range(0, len(gridsizes)):
        letter = grid_ref[n]
        idx = alphabet.index(letter)
        col = (idx % 5)
        row = 4 - ((idx) / 5)
        easting += (col * gridsizes[n])
        northing += (row * gridsizes[n])

    # numeric components of grid reference
    grid_ref = grid_ref[len(gridsizes):] # remove the letters
    halfway = int(len(grid_ref)/2)
    e = '{:0<5}'.format(grid_ref[0:halfway])
    e = '{}.{}'.format(e[0:5],e[5:])
    n = '{:0<5}'.format(grid_ref[halfway:])
    n = '{}.{}'.format(n[0:5],n[5:])
    easting += float(e)
    northing += float(n)

    return easting, northing

def british2xy(grid_ref):
    # From http://snorf.net/blog/2014/08/12/converting-british-national-grid-and-irish-grid-references/
    false_easting = 1000000
    false_northing = 500000
    false_northing = 260000#By trial and error
    gridsizes = [500000, 100000]
    return grid2xy(false_easting, false_northing, gridsizes, grid_ref)

def os_grid_ref_to_lat_lon(gr):
    re_gr = re.compile(r'^SX([0-9]{3})([0-9]{3})$')
    m = re.match(re_gr, gr)
    gr = "SX" + m.group(1) + "00" + m.group(2) + "00"
    print(gr)
    #e,n = GR_to_NE(gr)
    e,n = british2xy(gr)
    print("%s, %s" % (e,n))
    if e and n:
        lat, lon = OSGB36toWGS84(e, n)
    else:
        lat, lon = None, None

    print("%s, %s" % (lat, lon))
    print("==========")
    return lat, lon

#Read in from a file
# BNG = csv.reader(open('BNG.csv', 'rU'), delimiter = ',')
# BNG.next()
#
# #Get the output file ready
# outputFile = open('BNGandLatLon.csv', 'wb')
# output=csv.writer(outputFile,delimiter=',')
# output.writerow(['Lat', 'Lon', 'E', 'N'])
#
# #Loop through the data
# for E,N in BNG:
#     lat, lon = OSGB36toWGS84(float(E), float(N))
#     output.writerow([str(lat), str(lon), str(E), str(N)])
# #Close the output file
# outputFile.close()


