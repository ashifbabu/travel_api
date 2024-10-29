def combine_results(flyhub_results, bdfare_results):
    """
    Combine and normalize results from both Flyhub and Bdfare APIs.
    """
    combined_results = []

    # Process Flyhub results
    if "Results" in flyhub_results:
        for result in flyhub_results["Results"]:
            combined_results.append(
                {
                    "source": "Flyhub",
                    "result_id": result["ResultID"],
                    "is_refundable": result["IsRefundable"],
                    "total_fare": result["TotalFare"],
                    "currency": result["Currency"],
                    "segments": [
                        {
                            "origin": segment["Origin"]["AirportCode"],
                            "destination": segment["Destination"]["AirportCode"],
                            "airline": segment["Airline"]["AirlineName"],
                            "flight_number": segment["Airline"]["AirlineCode"]
                            + segment["FlightNumber"],
                            "departure_time": segment["DepartureDateTime"],
                            "arrival_time": segment["ArrivalDateTime"],
                            "duration": segment["Duration"],
                            "baggage": segment["Baggage"],
                        }
                        for segment in result["Segments"]
                    ],
                }
            )

    # Process Bdfare results
    if "response" in bdfare_results and "offersGroup" in bdfare_results["response"]:
        for offer in bdfare_results["response"]["offersGroup"]:
            combined_results.append(
                {
                    "source": "Bdfare",
                    "result_id": offer["offer"]["offerId"],
                    "is_refundable": offer["offer"]["refundable"],
                    "total_fare": offer["offer"]["price"]["totalPayable"]["total"],
                    "currency": offer["offer"]["price"]["totalPayable"]["currency"],
                    "segments": [
                        {
                            "origin": segment["paxSegment"]["departure"][
                                "iatA_LocationCode"
                            ],
                            "destination": segment["paxSegment"]["arrival"][
                                "iatA_LocationCode"
                            ],
                            "airline": segment["paxSegment"]["marketingCarrierInfo"][
                                "carrierName"
                            ],
                            "flight_number": f"{segment['paxSegment']['marketingCarrierInfo']['carrierDesigCode']}"
                            f"{segment['paxSegment']['flightNumber']}",
                            "departure_time": segment["paxSegment"]["departure"][
                                "aircraftScheduledDateTime"
                            ],
                            "arrival_time": segment["paxSegment"]["arrival"][
                                "aircraftScheduledDateTime"
                            ],
                            "duration": segment["paxSegment"]["duration"],
                            "baggage": next(
                                (
                                    ba["checkIn"][0]["allowance"]
                                    for ba in offer["offer"]["baggageAllowanceList"]
                                    if ba["departure"]
                                    == segment["paxSegment"]["departure"][
                                        "iatA_LocationCode"
                                    ]
                                ),
                                "N/A",
                            ),
                        }
                        for segment in offer["offer"]["paxSegmentList"]
                    ],
                }
            )

    # Sort combined results by total fare
    combined_results.sort(key=lambda x: x["total_fare"])

    return combined_results
