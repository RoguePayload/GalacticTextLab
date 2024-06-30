import os
import time
import asyncio
import aiohttp
from aiohttp import ClientSession

# ANSI escape sequences for text colors
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"

# Clear screen function
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Asynchronous function to validate API keys
async def validate_api_keys(session: ClientSession, nasa_key: str, ibm_key: str) -> bool:
    try:
        # Example validation URLs (replace with actual validation endpoints)
        nasa_url = f"https://api.nasa.gov/planetary/apod?api_key={nasa_key}"
        ibm_url = "https://gateway.watsonplatform.net/assistant/api/v1/workspaces?version=2018-09-20"
        
        async with session.get(nasa_url) as nasa_response:
            nasa_valid = nasa_response.status == 200
        async with session.get(ibm_url, headers={"Authorization": f"Basic {ibm_key}"}) as ibm_response:
            ibm_valid = ibm_response.status == 200
        
        return nasa_valid and ibm_valid
    except Exception as e:
        print(f"Error validating API keys: {e}")
        return False

# Function to request API keys from the user
def request_api_keys():
    nasa_key = input("Enter NASA API Key: ")
    ibm_key = input("Enter IBM Watson API Key: ")
    os.environ['NASA_API_KEY'] = nasa_key
    os.environ['IBM_WATSON_API_KEY'] = ibm_key
    return nasa_key, ibm_key

# Main function
async def main():
    clear_screen()
    nasa_key = os.getenv('NASA_API_KEY')
    ibm_key = os.getenv('IBM_WATSON_API_KEY')
    
    async with aiohttp.ClientSession() as session:
        if nasa_key and ibm_key:
            if await validate_api_keys(session, nasa_key, ibm_key):
                print("API Keys validated successfully.")
            else:
                print("Invalid API Keys. Please enter valid keys.")
                nasa_key, ibm_key = request_api_keys()
                if not await validate_api_keys(session, nasa_key, ibm_key):
                    print("Invalid API Keys. Proceeding without API Keys.")
        else:
            response = input("API Keys not found. Do you want to add them? (y/n): ")
            if response.lower() == 'y':
                nasa_key, ibm_key = request_api_keys()
                if not await validate_api_keys(session, nasa_key, ibm_key):
                    print("Invalid API Keys. Proceeding without API Keys.")
    
    time.sleep(2)
    display_welcome_screen()

# Function to display welcome screen
def display_welcome_screen():
    clear_screen()
    print(GREEN + r"""
  ____       _            _   _        _____         _     _          _     
 / ___| __ _| | __ _  ___| |_(_) ___  |_   _|____  _| |_  | |    __ _| |__  
| |  _ / _` | |/ _` |/ __| __| |/ __|   | |/ _ \ \/ / __| | |   / _` | '_ \ 
| |_| | (_| | | (_| | (__| |_| | (__    | |  __/>  <| |_  | |__| (_| | |_) |
 \____|\__,_|_|\__,_|\___|\__|_|\___|   |_|\___/_/\_\\__| |_____\__,_|_.__/ 
          
    """ + RESET)
    time.sleep(2)
    print(YELLOW + "Welcome to Galactic Text Lab" + RESET)
    time.sleep(2)
    print(GREEN + "Developed by Rogue Payload" + RESET)
    time.sleep(2)
    display_menu()

# Function to display menu
def display_menu():
    clear_screen()
    print(RED + "MENU OPTIONS:" + RESET)
    print(YELLOW + "1. Hypothetical Simulator")
    print("2. Mathematical Operations")
    print("3. Educational Resources")
    print("4. Developer")
    print("5. Data Visualization")
    print("6. Exit" + RESET)
    choice = input("Enter your choice: ")
    handle_menu_choice(choice)

# Function to handle menu choice
def handle_menu_choice(choice):
    if choice == '1':
        import simulator
        simulator.run()
    elif choice == '2':
        import mathematical
        mathematical.run()
    elif choice == '3':
        import education
        education.run()
    elif choice == '4':
        show_developer_info()
    elif choice == '5':
        import data_visualization
        data_visualization.run()
    elif choice == '6':
        exit_program()
    else:
        print("Invalid choice. Please try again.")
        display_menu()

# Function to show developer info
def show_developer_info():
    clear_screen()
    print("Developed by Rogue Payload")
    print("Contact: rogue.payload@example.com")
    input("Press Enter to return to the menu.")
    display_menu()

# Function to exit program
def exit_program():
    clear_screen()
    print("Thank you for using Galactic Text Lab!")
    time.sleep(2)
    clear_screen()

# Run the main function
if __name__ == "__main__":
    asyncio.run(main())
