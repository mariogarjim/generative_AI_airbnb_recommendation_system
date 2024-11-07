import numpy as np

# TODO : Extend to multiple landmarks approach

def filter_data(airbnb_df, user_context):
    """Filter data from user needs

    Args:
        airbnb_df (DataFrame): Df with airbnbs information
        user_context (dict): Dict with context about user needs
        Example of user context:
            {'destination': 'Museo del Prado',
            'latitude': 40.4138,
            'longitude': -3.6922,
            'travel_date': '2024-03-11',
            'travelers': 2,
            'budget': 100}
    """
    # Filter Airbnbs with enough space to accommodate the number 
    #of people travelling
    print(user_context)
    travelers = user_context["travelers"]
    if travelers:
        airbnb_df = airbnb_df[airbnb_df["accommodates"] >= travelers]
    
    # Filter Airbnbs that are avaliable in travel date below traveler budget
    budget = user_context["budget"]
    if budget:
        airbnb_df = filter_airbnbs_by_date_and_budget(airbnb_df, 
                                                    travel_date=user_context["travel_date"], 
                                                    budget=budget,
                                                    )
    
    # Order Airbnbs by distance to destination
    airbnb_df = order_airbnbs_by_distance_to_destination(airbnb_df, 
                                                         destination_lat=user_context["latitude"], 
                                                         destination_lon=user_context["longitude"],
                                                        )
    
    return airbnb_df

def keep_avaliable_within_budget_airbnbs(airbnb_df_dates_prices, travel_date, budget):
    """Keep airbnbs that are avaliable in travel date and within budget.
    
    Transdorm avaliable_dates_prices columns keeping only avaliable airbnbs within budget

    Args:
        airbnb_df_dates_prices (dict): Dict of date-price
        travel_date (str): Travel date
        budget (int): Budget

    Returns:
        (date, price) for airbnb if avaliable and in budget, None if not avaliable. 
    """
    if travel_date not in airbnb_df_dates_prices:
        return None
    if float(airbnb_df_dates_prices[travel_date].replace('$','').replace(",","")
             .strip()) > budget:
        return None
    return airbnb_df_dates_prices[travel_date]
    
    
def filter_airbnbs_by_date_and_budget(airbnb_df, travel_date, budget):
    """Filter airbnbs by user travel date and budget

    Args:
        airbnb_df (DataFrame): Airbnbn df
        travel_date (str): Travel date
        budget (int): Budget

    Returns:
        airbnb_df (DataFrame): Filtered airbnb df
    """
    airbnb_df.loc[:, "avaliable_dates_prices"] = airbnb_df["avaliable_dates_prices"].apply(
        lambda aval_dates_prices: keep_avaliable_within_budget_airbnbs(
            airbnb_df_dates_prices = aval_dates_prices,
            travel_date=travel_date, 
            budget=budget,
        ),
    )
    
    airbnb_df = airbnb_df[airbnb_df["avaliable_dates_prices"].notna()]
    
    return airbnb_df


def harvesine(lat1, lon1, lat2, lon2):
    """Harvesine distance
    
    https://en.wikipedia.org/wiki/Haversine_formula
    """
    # Convert decimal degrees to radians 
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula 
    dlat = lat2 - lat1 
    dlon = lon2 - lon1 
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    radius_km = 6371  # Radius of Earth in kilometers.
    return c * radius_km

def order_airbnbs_by_distance_to_destination(airbnb_df, destination_lat, destination_lon):
    """Order airbnbs by distance to destination

    Args:
        airbnb_df (DataFrame): Airbnbn df
        destination_lat (float): Destination latitude
        destination_lon (float): Destination longitude

    Returns:
        airbnb_df (DataFrame): Filtered airbnb df
    """
    airbnb_df["distance_to_destination"] = airbnb_df.apply(
        lambda airbnb: harvesine(lat1=destination_lat, lon1=destination_lon, 
                                 lat2=airbnb["latitude"], lon2=airbnb["longitude"]),
        axis = 1,
    )
    
    airbnb_df = airbnb_df.sort_values(by="distance_to_destination")
    
    return airbnb_df