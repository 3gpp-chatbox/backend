from neo4j import GraphDatabase
import os
from rich.console import Console
from dotenv import load_dotenv

console = Console()

def test_connection():
    # Load environment variables
    load_dotenv()
    
    # Get connection details
    uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    username = os.getenv("NEO4J_USERNAME", "neo4j")
    password = os.getenv("NEO4J_PASSWORD")
    
    # Print connection details (without password)
    console.print("\n[blue]Connection Details:[/blue]")
    console.print(f"URI: {uri}")
    console.print(f"Username: {username}")
    console.print(f"Password is {'set' if password else 'not set'}")
    
    try:
        # Try to connect
        console.print("\n[blue]Attempting to connect...[/blue]")
        driver = GraphDatabase.driver(uri, auth=(username, password))
        
        # Test the connection
        with driver.session() as session:
            result = session.run("RETURN 1 as test")
            result.single()
        
        driver.close()
        console.print("[green]✓ Connection successful![/green]")
        return True
        
    except Exception as e:
        console.print("[red]✗ Connection failed![/red]")
        console.print(f"[yellow]Error: {str(e)}[/yellow]")
        
        # Provide specific guidance based on error
        if "address resolved to no hosts" in str(e).lower():
            console.print("\n[yellow]Possible issues:[/yellow]")
            console.print("1. Neo4j is not running")
            console.print("2. Wrong port number")
            console.print("3. Neo4j is running on a different host")
            console.print("\n[blue]Solutions:[/blue]")
            console.print("1. Start Neo4j service/desktop")
            console.print("2. Check if port 7687 is correct")
            console.print("3. Verify the URI in .env file")
        
        elif "unauthorized" in str(e).lower():
            console.print("\n[yellow]Possible issues:[/yellow]")
            console.print("1. Wrong username/password")
            console.print("2. Database credentials not updated")
            console.print("\n[blue]Solutions:[/blue]")
            console.print("1. Check credentials in Neo4j Desktop/Browser")
            console.print("2. Update .env file with correct credentials")
            console.print("3. If using new installation, change default password")
        
        return False

if __name__ == "__main__":
    console.print("[bold blue]Neo4j Connection Test[/bold blue]")
    test_connection() 