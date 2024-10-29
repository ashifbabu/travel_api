def prepare_flyhub_request(params):
    segments = []
    for segment in params["segments"]:
        segments.append(
            {
                "Origin": segment["origin"],
                "Destination": segment["destination"],
                "CabinClass": get_cabin_class(params["cabin_class"]),
                "DepartureDateTime": segment["departure_date"],
            }
        )

    return {
        "AdultQuantity": params.get("adult_count", 1),
        "ChildQuantity": params.get("child_count", 0),
        "InfantQuantity": params.get("infant_count", 0),
        "EndUserIp": params.get("user_ip", "127.0.0.1"),
        "JourneyType": get_journey_type(params["trip_type"]),
        "Segments": segments,
    }


def get_cabin_class(cabin_class):
    cabin_map = {"economy": "1", "premium_economy": "2", "business": "3", "first": "4"}
    return cabin_map.get(cabin_class.lower(), "1")


def get_journey_type(trip_type):
    type_map = {"one_way": "1", "round_trip": "2", "multi_city": "3"}
    return type_map.get(trip_type.lower(), "1")
