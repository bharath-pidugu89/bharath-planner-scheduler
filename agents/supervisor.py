import os
from datetime import date
import time
import random

from google.genai.errors import ServerError

from dotenv import load_dotenv
from google import genai
from google.genai import types

from models.trip import TripDetails, SupervisorDecision

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")

if not API_KEY:
    raise ValueError(
        "GEMINI_API_KEY is missing. Add it to your .env file."
    )

client = genai.Client(api_key=API_KEY)


class SupervisorAgent:

    def __init__(self):
        self.conversation = []
        self.trip = TripDetails()

    def process_message(self, user_message: str) -> SupervisorDecision:

        self.conversation.append(
            f"User: {user_message}"
        )

        today = date.today().isoformat()

        prompt = f"""
                    You are the Supervisor Agent of a multi-agent travel planning system.

                    Today's date is {today}.
                    Use this date to resolve relative dates such as tomorrow and next Friday.

                    The destination for this trip is Singapore.

                    Your responsibilities:
                    1. Understand the user's travel and meeting requirements.
                    2. Extract information into the TripDetails schema.
                    3. Preserve information from earlier messages.
                    4. Identify missing information and ask concise clarification questions.
                    5. Set ready=true only when all required information is available.

                    Required information:
                    - departure_city
                    - meeting_date
                    - meeting_time
                    - meeting_location
                    - number of hotel nights

                    The user may express dates and durations in natural language.
                    Convert dates to YYYY-MM-DD.
                    Use 24-hour time where possible.

                    If the user says "two days stay", do not silently assume
                    whether that means two nights. Ask for clarification.

                    Do not invent a departure city, meeting time or venue.

                    Do not search, book, reserve or purchase anything.
                    This version uses mock research agents only.

                    CURRENT TRIP INFORMATION:
                    {self.trip.model_dump_json(indent=2)}

                    CONVERSATION:
                    {chr(10).join(self.conversation)}

                    Return a structured SupervisorDecision.
                    If information is missing, ready must be false and message
                    must ask the user for the missing details.
                    If all required information is available, ready must be true
                    and message should briefly explain that research will begin.
                    """

        response = None

        for attempt in range(1, 4):

            try:
                print(
                    f"\n[Supervisor] Gemini request "
                    f"attempt {attempt}/3..."
                )

                response = client.models.generate_content(
                    model=MODEL,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        response_schema=SupervisorDecision,
                        temperature=0.2,
                    ),
                )

                break

            except ServerError as error:

                if attempt == 3:
                    raise

                delay = (2 ** attempt) + random.uniform(0, 1)

                print(
                    f"[Supervisor] Gemini temporarily unavailable. "
                    f"Retrying in {delay:.1f} seconds..."
                )

                time.sleep(delay)

        decision = response.parsed

        if decision is None:
            raise RuntimeError(
                "Gemini did not return a valid structured response."
            )

        # Preserve previously collected details.
        updated = self.trip.model_dump()

        for key, value in decision.trip.model_dump().items():
            if value is not None:
                updated[key] = value

        self.trip = TripDetails.model_validate(updated)

        return decision