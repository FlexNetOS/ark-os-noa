#!/usr/bin/env python3
"""
ark-os-noa Agent CLI

Command-line interface for interacting with coding agents in the ark-os-noa platform.
This tool provides easy access to development automation agents.
"""

import sys
from pathlib import Path
from typing import List, Optional
import json

# Add project root to Python path
ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

try:
    import typer
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
except ImportError:
    print("Missing dependencies. Please install with:")
    print("pip install typer rich")
    sys.exit(1)

from coding_agents import agent_registry, ServiceGeneratorAgent

app = typer.Typer(help="ark-os-noa Coding Agents CLI")
console = Console()

@app.command()
def list_agents():
    """List all available coding agents"""
    # Initialize agents to register them
    ServiceGeneratorAgent()
    
    agents = agent_registry.list_agents()
    
    if not agents:
        console.print("No agents registered", style="yellow")
        return
    
    table = Table(title="Available Coding Agents")
    table.add_column("Agent Name", style="cyan")
    table.add_column("Description", style="green")
    
    descriptions = {
        "service-generator": "Generate new microservice boilerplate",
    }
    
    for agent_name in agents:
        description = descriptions.get(agent_name, "No description available")
        table.add_row(agent_name, description)
    
    console.print(table)

@app.command()
def generate_service(
    name: str = typer.Argument(..., help="Name of the service to generate"),
    endpoints: Optional[List[str]] = typer.Option(None, "--endpoint", "-e", help="Endpoints to include")
):
    """Generate a new microservice"""
    
    console.print(f"🚀 Generating service: {name}", style="bold blue")
    
    try:
        # Initialize agent (this will register it)
        agent = ServiceGeneratorAgent()
        
        result = agent.execute(
            service_name=name,
            endpoints=endpoints or ["/", "/health", "/process"]
        )
        
        if result["success"]:
            console.print("✅ Service generated successfully!", style="bold green")
            
            # Show created files
            files_table = Table(title="Files Created")
            files_table.add_column("File Path", style="cyan")
            
            for file_path in result["files_created"]:
                files_table.add_row(file_path)
            
            console.print(files_table)
            
            # Show next steps
            next_steps_panel = Panel(
                "\n".join(f"• {step}" for step in result["next_steps"]),
                title="Next Steps",
                border_style="green"
            )
            console.print(next_steps_panel)
            
        else:
            console.print(f"❌ Error: {result['error']}", style="bold red")
            
    except Exception as e:
        console.print(f"❌ Error generating service: {e}", style="bold red")
        raise typer.Exit(1)

@app.command()
def health_check():
    """Check the health of the development environment"""
    console.print("🏥 Checking environment health...", style="bold blue")
    
    checks = []
    
    # Check workspace structure
    required_files = ["requirements.txt", "docker-compose.yml", "services", "tests"]
    for file_path in required_files:
        path = Path(file_path)
        if path.exists():
            checks.append((file_path, "✅", "green"))
        else:
            checks.append((file_path, "❌", "red"))
    
    # Check virtual environment
    if Path("venv").exists():
        checks.append(("Virtual Environment", "✅", "green"))
    else:
        checks.append(("Virtual Environment", "⚠️", "yellow"))
    
    # Display results
    health_table = Table(title="Environment Health Check")
    health_table.add_column("Component", style="cyan")
    health_table.add_column("Status", style="white")
    
    for component, status, color in checks:
        health_table.add_row(component, status)
    
    console.print(health_table)

@app.command()
def run_service(
    name: str = typer.Argument(..., help="Name of the service to run"),
    port: int = typer.Option(8000, "--port", "-p", help="Port to run the service on"),
    reload: bool = typer.Option(True, "--reload/--no-reload", help="Enable auto-reload")
):
    """Run a specific service"""
    import subprocess
    
    service_path = Path(f"services/{name}/main.py")
    
    if not service_path.exists():
        console.print(f"❌ Service '{name}' not found at {service_path}", style="bold red")
        raise typer.Exit(1)
    
    console.print(f"🚀 Starting service '{name}' on port {port}", style="bold green")
    
    cmd = [
        "uvicorn", 
        f"services.{name}.main:app",
        "--host", "0.0.0.0",
        "--port", str(port)
    ]
    
    if reload:
        cmd.append("--reload")
    
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        console.print("\n👋 Service stopped", style="yellow")
    except Exception as e:
        console.print(f"❌ Error running service: {e}", style="bold red")

@app.command()
def logs(
    agent: str = typer.Argument(..., help="Agent name to view logs for"),
    format: str = typer.Option("pretty", "--format", "-f", help="Output format: pretty or json")
):
    """View agent execution logs"""
    log_path = Path(f"logs/{agent}_execution.json")
    
    if not log_path.exists():
        console.print(f"❌ No logs found for agent '{agent}'", style="bold red")
        raise typer.Exit(1)
    
    with open(log_path) as f:
        log_data = json.load(f)
    
    if format == "json":
        console.print_json(data=log_data)
    else:
        # Pretty format
        logs_table = Table(title=f"Execution Logs for {agent}")
        logs_table.add_column("Timestamp", style="cyan")
        logs_table.add_column("Action", style="green")
        logs_table.add_column("Details", style="white")
        
        for entry in log_data:
            details = json.dumps(entry.get("details", {}), indent=2) if entry.get("details") else ""
            logs_table.add_row(
                entry["timestamp"],
                entry["action"],
                details
            )
        
        console.print(logs_table)

if __name__ == "__main__":
    app()