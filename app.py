import json
import traceback

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from agents.supervisor import SupervisorAgent
from graph.workflow import execute_research

console = Console()


def show_trip_summary(trip: dict):

    table = Table(title="Confirmed Trip Information")

    table.add_column("Field", style="cyan")
    table.add_column("Value", style="green")

    for key, value in trip.items():
        table.add_row(key.replace("_", " ").title(), str(value))

    console.print(table)


def show_results(results: dict):

    console.print(
        Panel(
            "[bold green]All research agents completed![/bold green]",
            title="Supervisor",
        )
    )

    for category, result in results.items():

        console.print(
            Panel(
                json.dumps(result, indent=2, ensure_ascii=False),
                title=category.upper(),
                border_style="blue",
            )
        )


def main():

    supervisor = SupervisorAgent()

    console.print(
        Panel(
            "[bold cyan]Multi-Agent Travel Planner[/bold cyan]\n"
            "Powered by Gemini + LangGraph\n\n"
            "Type your travel requirements below.\n"
            "Type 'exit' to quit.",
            title="Welcome",
        )
    )

    while True:

        user_message = console.input(
            "\n[bold white]You:[/bold white] "
        ).strip()

        if user_message.lower() in {"exit", "quit"}:
            console.print("[yellow]Goodbye![/yellow]")
            break

        if not user_message:
            continue

        try:
            decision = supervisor.process_message(user_message)

            console.print(
                Panel(
                    decision.message,
                    title="Supervisor Agent",
                    border_style="magenta",
                )
            )

            trip = supervisor.trip.model_dump()

            required_fields = [
                "departure_city",
                "meeting_date",
                "meeting_time",
                "meeting_location",
                "nights",
            ]

            missing = [
                field for field in required_fields
                if trip.get(field) is None
            ]

            # Validate completeness in Python too.
            if not decision.ready or missing:

                if missing:
                    console.print(
                        "[yellow]Still required: "
                        + ", ".join(missing)
                        + "[/yellow]"
                    )

                continue

            show_trip_summary(trip)

            console.print(
                "\n[bold green]Supervisor:[/bold green] "
                "All required information is available. "
                "Starting the three research agents..."
            )

            results = execute_research(trip)

            show_results(results)

            console.print(
                "\n[bold cyan]Research completed.[/bold cyan] "
                "These are mock results, not actual travel offers."
            )

            console.print(
                "[dim]Next milestone: schedule and review agents.[/dim]"
            )

            # This first prototype handles one trip per session.
            break

       
        
        except Exception as error:
            console.print(
                f"\n[bold red]Application error:[/bold red] "
                f"{type(error).__name__}: {error}"
            )
            
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()