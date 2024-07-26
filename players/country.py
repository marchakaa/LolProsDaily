import pycountry

def get_country_code(country_name):
    try:
        country = pycountry.countries.lookup(country_name)
        return country.alpha_2  # For 2-letter code
        # return country.alpha_3  # For 3-letter code
    except LookupError:
        return None

# Example usage
# country_name = "China"
# code = get_country_code(country_name)
# print(f"The code for {country_name} is {code}")