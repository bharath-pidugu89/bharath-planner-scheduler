import time
from rich.console import Console

console = Console()


def flight_agent(trip: dict) -> dict:
    console.print(
        "\n[bold cyan]Agent 1 Working:[/bold cyan] "
        "Checking available flights (MOCK DATA)..."
    )

    time.sleep(2)

    return {
        "agent": "Flight Research Agent",
        "status": "completed",
        "departure": trip.get("departure_city"),
        "destination": trip.get("destination"),
        "options": [
            {
                "airline": "Example Airways",
                "departure": "10:30",
                "arrival": "07:00 (+1 day)",
                "price": "€620",
            },
            {
                "airline": "Sample Airlines",
                "departure": "14:00",
                "arrival": "09:30 (+1 day)",
                "price": "€570",
            },
        ],
        "note": "Illustrative mock data. Not real flight offers.",
    }


def hotel_agent(trip: dict) -> dict:
    console.print(
        "\n[bold yellow]Agent 2 Working:[/bold yellow] "
        "Finding four-star hotels (MOCK DATA)..."
    )

    time.sleep(2.5)

    return {
        "agent": "Hotel Research Agent",
        "status": "completed",
        "destination": trip.get("destination"),
        "nights": trip.get("nights"),
        "options": [
            {
                "name": "Example Marina Hotel",
                "category": "4-star",
                "price_per_night": "€145",
                "location": "Marina Bay",
            },
            {
                "name": "Sample City Hotel",
                "category": "4-star",
                "price_per_night": "€115",
                "location": "City Centre",
            },
        ],
        "note": "Illustrative mock data. Not real hotel availability.",
    }


def tourism_agent(trip: dict) -> dict:
    console.print(
        "\n[bold green]Agent 3 Working:[/bold green] "
        "Researching tourist attractions (MOCK DATA)..."
    )

    time.sleep(3)

    return {
        "agent": "Tourism Research Agent",
        "status": "completed",
        "destination": trip.get("destination"),
        "attractions": [
            "Gardens by the Bay",
            "Marina Bay Sands area",
            "Merlion Park",
            "Sentosa Island",
            "Chinatown",
            "Singapore Botanic Gardens",
        ],
        "note": "Illustrative shortlist. Opening hours and access not verified.",
    }