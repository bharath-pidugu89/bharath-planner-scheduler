from graph.workflow import execute_research

sample_trip = {
    "destination": "Singapore",
    "departure_city": "Frankfurt",
    "meeting_date": "2026-11-11",
    "meeting_time": "10:00",
    "meeting_location": "Marina Bay",
    "nights": 2,
    "sightseeing_days": 2,
    "budget": "Moderate",
    "hotel_preference": "4-star",
}

results = execute_research(sample_trip)

assert "flights" in results
assert "hotels" in results
assert "tourism" in results

print("\nAll three mock agents returned results successfully!")