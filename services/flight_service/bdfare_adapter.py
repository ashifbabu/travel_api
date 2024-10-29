def prepare_bdfare_request(params):
    origin_dest = []
    for segment in params['segments']:
        origin_dest.append({
            "originDepRequest": {
                "iatA_LocationCode": segment['origin'],
                "date": segment['departure_date']
            },
            "destArrivalRequest": {
                "iatA_LocationCode": segment['destination']
            }
        })

    pax = []
    for i in range(params.get('adult_count', 1)):
        pax.append({"paxID": f"PAX{i+1}", "ptc": "ADT"})
    for i in range(params.get('child_count', 0)):
        pax.append({"paxID": f"PAX{len(pax)+1}", "ptc": "CHD"})
    for i in range(params.get('infant_count', 0)):
        pax.append({"paxID": f"PAX{len(pax)+1}", "ptc": "INF"})

    return {
        "pointOfSale": "BD",  # Assuming Bangladesh as point of sale
        "request": {
            "originDest": origin_dest,
            "pax": pax,
            "shoppingCriteria": {
                "tripType": get_trip_type(params['trip_type']),
                "travelPreferences": {
                    "vendorPref": params.get('preferred_airlines', []),
                    "cabinCode": params['cabin_class'].capitalize()
                },
                "returnUPSellInfo": True
            }
        }
    }

def get_trip_type(trip_type):
    type_map = {
        "one_way": "Oneway",
        "round_trip": "Return",
        "multi_city": "Circle"
    }
    return type_map.get(trip_type.lower(), "Oneway")