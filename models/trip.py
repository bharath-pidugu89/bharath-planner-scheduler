from pydantic import BaseModel, Field


class TripDetails(BaseModel):
    destination: str = "Singapore"

    departure_city: str | None = None
    meeting_date: str | None = None
    meeting_time: str | None = None
    meeting_location: str | None = None

    nights: int | None = None
    sightseeing_days: int = 2

    budget: str | None = None
    hotel_preference: str = "4-star"


class SupervisorDecision(BaseModel):
    ready: bool
    message: str
    trip: TripDetails
    missing_information: list[str] = Field(default_factory=list)