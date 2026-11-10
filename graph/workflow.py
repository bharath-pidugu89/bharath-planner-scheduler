import operator
from typing import TypedDict, Annotated

from langgraph.graph import StateGraph, START, END

from agents.research_agents import (
    flight_agent,
    hotel_agent,
    tourism_agent,
)


class ResearchState(TypedDict):
    trip: dict
    results: Annotated[dict, operator.or_]


def run_flight_agent(state: ResearchState):
    result = flight_agent(state["trip"])
    return {"results": {"flights": result}}


def run_hotel_agent(state: ResearchState):
    result = hotel_agent(state["trip"])
    return {"results": {"hotels": result}}


def run_tourism_agent(state: ResearchState):
    result = tourism_agent(state["trip"])
    return {"results": {"tourism": result}}


def build_research_graph():

    builder = StateGraph(ResearchState)

    builder.add_node("flight_agent", run_flight_agent)
    builder.add_node("hotel_agent", run_hotel_agent)
    builder.add_node("tourism_agent", run_tourism_agent)

    # Fan out: all three agents start in the same graph step.
    builder.add_edge(START, "flight_agent")
    builder.add_edge(START, "hotel_agent")
    builder.add_edge(START, "tourism_agent")

    builder.add_edge("flight_agent", END)
    builder.add_edge("hotel_agent", END)
    builder.add_edge("tourism_agent", END)

    return builder.compile()


research_graph = build_research_graph()


def execute_research(trip: dict) -> dict:

    initial_state = {
        "trip": trip,
        "results": {},
    }

    final_state = research_graph.invoke(initial_state)

    return final_state["results"]