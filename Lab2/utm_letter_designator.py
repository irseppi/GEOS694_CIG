import numpy as np

def utm_letter_designator(lat):
    """
    Determines the UTM letter designator a given latitude. Returns 'Z' if 
    latitude is outside the UTM limits (84N to 80S).

    Written by Chuck Gantz- chuck.gantz@globalstar.com
    Args:
    lat (str): latitude in decimal degrees
    
    Returns:
    str: UTM letter designator
    """
    
    latitudes = [84.001] + list(np.arange(72, -81, -8))
    designation_codes = ["X","W","V","U","T","S","R","Q","P","N","M"
                         ,"L","K","J","H","G","F","E","D","C"]
    utm_designations = {}
    for i in range(len(latitudes)-1):
        utm_designations[designation_codes[i]] = (latitudes[i], latitudes[i+1])
        
    for designation, coords in utm_designations.items():
        lat_max, lat_min = coords
        if lat_min <= lat < lat_max:
            return designation
    else:
        return "Z"    

if __name__ == "__main__":
    latitudes = [85, 84, 64, 0, -1, -79.9999, 200]
    for latitude in latitudes:
        print(f"lat {latitude} = {utm_letter_designator(latitude)}")
