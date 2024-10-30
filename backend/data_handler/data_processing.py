import pandas as pd


def handle_data():
    """Main function to handle and process Airbnb data.

    Returns:
        lsiting_detailed (DataFrame), airbnb_data (DataFrame)
    """
    listings_detailed, calendar_detailed = read_data()
    airbnb_data = process_data(listings_detailed, calendar_detailed)

    return listings_detailed, airbnb_data


def read_data():
    """Read Airbnb data from CSV files.

    Returns:
        tuple: A tuple containing two DataFrames:
            - listings_detailed: DataFrame with detailed listings.
            - calendar_detailed: DataFrame with calendar information.
    """
    listings_detailed = pd.read_csv("downloads/listings_detailed.csv")
    calendar_detailed = pd.read_csv("downloads/calendar_detailed.csv")

    return listings_detailed, calendar_detailed


def process_data(listings_detailed, calendar_detailed):
    """Process and filter the Airbnb listings and calendar data.

    Args:
        listings_detailed (DataFrame): The detailed listings DataFrame.
        calendar_detailed (DataFrame): The calendar DataFrame.

    Returns:
        DataFrame: A merged DataFrame containing filtered Airbnb data.
    """
    filtered_listings_detailed = filter_listings_detailed(listings_detailed)
    filtered_calendar_detailed = filter_calendar_detailed(calendar_detailed)

    airbnb_data = pd.merge(
        filtered_listings_detailed,
        filtered_calendar_detailed,
        left_on="id",
        right_on="listing_id",
        how="inner",
    )

    return airbnb_data


def filter_listings_detailed(listings_detailed):
    """Filter listings based on specific criteria.

    Args:
        listings_detailed (DataFrame): The detailed listings DataFrame.

    Returns:
        DataFrame: A filtered DataFrame containing only relevant listings.
    """
    relevant_columns = [
        "id",
        "name",
        "description",
        "neighbourhood_cleansed",
        "neighbourhood_group_cleansed",
        "latitude",
        "longitude",
        "property_type",
        "amenities",
        "host_acceptance_rate",
        "number_of_reviews",
        "review_scores_rating",
        "accommodates",
        "minimum_nights",
    ]

    filtered_listings = listings_detailed[relevant_columns]

    # Maintain only airbnbs with host acceptance > 70%
    filtered_listings = filtered_listings[filtered_listings["host_acceptance_rate"].notna()]
    filtered_listings["host_acceptance_rate_numeric"] = (
        filtered_listings["host_acceptance_rate"].str.rstrip("%").astype(float)
    )
    filtered_listings = filtered_listings[filtered_listings["host_acceptance_rate_numeric"] > 70]
    filtered_listings = filtered_listings.drop(columns=["host_acceptance_rate_numeric"])

    # Maintain only airbnbs with 5 or more reviews
    filtered_listings = filtered_listings[filtered_listings["number_of_reviews"] >= 5]

    # Maintain only airbnbs with review score rating > 3
    filtered_listings = filtered_listings[filtered_listings["review_scores_rating"].notna()]
    filtered_listings = filtered_listings[filtered_listings["review_scores_rating"] >= 3.0]

    return filtered_listings


def filter_calendar_detailed(calendar_detailed):
    """Filter calendar data for available dates for Airbnbs.

    Args:
        calendar_detailed (DataFrame): The calendar DataFrame.

    Returns:
        DataFrame: A DataFrame containing listing IDs and their available dates and prices.
    """
    # Filter for only available dates
    available_dates_airbnbs = calendar_detailed[calendar_detailed["available"] == "t"]

    # Group by 'listing_id' and aggregate dates and prices into lists
    airbnb_calendar_information = (
        available_dates_airbnbs.groupby("listing_id")
        .apply(
            lambda x: list(zip(x["date"].to_list(), x["price"].to_list())),
        )
        .reset_index(name="avaliable_dates_prices")
    )

    return airbnb_calendar_information
