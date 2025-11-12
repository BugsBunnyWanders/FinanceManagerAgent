"""Main application entry point for Finance Manager Agent."""
import os
import sys
import asyncio
from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from root_agent import root_agent
from database.connection import db_connection

# Load environment variables
load_dotenv()

# Application constants
APP_NAME = "finance_manager_app"
USER_ID = os.getenv('USER_ID', 'default_user')


def initialize_application():
    """Initialize the application and check configuration."""
    print("=" * 60)
    print("Finance Manager Agent - Personal Finance Coach")
    print("=" * 60)
    print()
    
    # Check for API key
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key or api_key == 'your_google_api_key_here':
        print("❌ Error: GOOGLE_API_KEY not configured!")
        print("Please set your Google API key in the .env file.")
        print("Copy env_example.txt to .env and add your API key.")
        sys.exit(1)
    
    print("✓ Google API key configured")
    
    # Test database connection
    try:
        db = db_connection.database
        print(f"✓ Connected to database: {db.name}")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("Please ensure MongoDB is running and connection string is correct.")
        sys.exit(1)
    
    print()
    print("=" * 60)
    print("Welcome! I'm your personal finance advisor. 💰")
    print("I can help you:")
    print("  • Set and track financial goals")
    print("  • Monitor expenses and account balance")
    print("  • Provide personalized savings recommendations")
    print("  • Alert you about spending patterns")
    print()
    print("Type 'quit' or 'exit' to end the conversation.")
    print("=" * 60)
    print()


async def call_agent_async(runner, session_id: str, query: str):
    """
    Sends a query to the agent and processes the response.
    
    Args:
        runner: The ADK Runner instance
        session_id: The session identifier
        query: User's query text
        
    Returns:
        str: The agent's final response text
    """
    # Prepare the user's message in ADK format
    new_message = types.Content(
        role='user',
        parts=[types.Part(text=query)]
    )
    
    final_response_text = ""
    
    try:
        # Execute the agent logic and process events
        async for event in runner.run_async(
            user_id=USER_ID,
            session_id=session_id,
            new_message=new_message
        ):
            # Check for the final response event
            if event.is_final_response():
                if event.content and event.content.parts:
                    # Extract text response from the first part
                    final_response_text = event.content.parts[0].text
                elif event.actions and hasattr(event.actions, 'escalate') and event.actions.escalate:
                    # Handle escalation
                    final_response_text = f"Agent escalated: {event.error_message if hasattr(event, 'error_message') else 'Unknown error'}"
                break
    except Exception as e:
        final_response_text = f"Error processing request: {str(e)}"
    
    return final_response_text


async def main_async():
    """Main conversation loop using ADK Runner with session management."""
    initialize_application()
    
    # Initialize the InMemory session service for local development
    session_service = InMemorySessionService()
    
    # Create a session for the conversation (await since it's async)
    session_id = f"session_{USER_ID}_001"
    session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=session_id
    )
    
    print(f"✓ Session created: {session.id}")
    print()
    
    # Initialize the ADK Runner
    runner = Runner(
        agent=root_agent,
        app_name=APP_NAME,
        session_service=session_service
    )
    
    print(f"✓ Runner initialized for agent '{runner.agent.name}'")
    print()
    
    # Main conversation loop
    while True:
        try:
            # Get user input
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            # Check for exit commands
            if user_input.lower() in ['quit', 'exit', 'bye', 'goodbye']:
                print()
                print("Finance Advisor: Goodbye! Keep up the great work with your finances! 💪")
                print()
                break
            
            # Send message and get response using the runner
            print("Finance Advisor: ", end="", flush=True)
            
            # Call the agent asynchronously
            response_text = await call_agent_async(runner, session_id, user_input)
            
            # Display response
            if response_text:
                print(response_text)
            else:
                print("I apologize, I couldn't generate a response. Could you try rephrasing that?")
            
            print()
            
        except KeyboardInterrupt:
            print("\n")
            print("Finance Advisor: Goodbye! Keep up the great work with your finances! 💪")
            print()
            break
        
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("Please try again or type 'quit' to exit.")
            print()
    
    # Clean up
    db_connection.close()
    print("✓ Application closed successfully")


def main():
    """Entry point - runs the async main function."""
    asyncio.run(main_async())


if __name__ == "__main__":
    main()

