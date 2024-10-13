import phonenumbers
from phonenumbers import geocoder, carrier, timezone
import folium
from opencage.geocoder import OpenCageGeocode

# API key for OpenCage Geocode
key = "Your API Key Number"

# Input the number
number = input("Enter the phone number with country code : ")

try:
    # Parse the phone number
    check_number = phonenumbers.parse(number)

    # Validate if it's a real number
    if not phonenumbers.is_valid_number(check_number):
        print("Invalid phone number. Please check the input.")
    else:
        # Get country/region info
        number_location = geocoder.description_for_number(check_number, "en")
        print("Country/Region Name: ", number_location)

        # Get carrier (service provider) info
        service_provider = carrier.name_for_number(check_number, "en")
        print("Service Provider: ", service_provider)

        # Get timezone information
        time_zones = timezone.time_zones_for_number(check_number)
        print("Time Zone(s): ", time_zones)

        # Geocoding the location using OpenCage API
        geocoder_service = OpenCageGeocode(key)
        query = str(number_location)
        results = geocoder_service.geocode(query)

        if results and len(results):
            lat = results[0]["geometry"]["lat"]
            lng = results[0]["geometry"]["lng"]
            print(f"Coordinates: Latitude: {lat}, Longitude: {lng}")

            # Creating a map using Folium
            map_location = folium.Map(location=[lat, lng], zoom_start=10)
            folium.Marker([lat, lng], popup=number_location).add_to(map_location)
            
            # Save the map to an HTML file
            map_location.save("My_Location.html")
            print("Location saved to My_Location.html")
        else:
            print("No geocoding results found for the given location.")
except phonenumbers.phonenumberutil.NumberParseException:
    print("Error: The phone number entered is not valid.")
except Exception as e:
    print(f"An error occurred: {e}")
