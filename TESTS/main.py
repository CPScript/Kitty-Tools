import requests

def get_kahoot_quiz_id(pin):
    url = f"https://kahoot.it/reserve/session/{pin}/?"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        json_response = response.json()
        quiz_id = json_response.get("uuid")  # The key might differ!
        return quiz_id
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

game_pin = input("Enter the Kahoot game pin: ")

quiz_id = get_kahoot_quiz_id(game_pin)
if quiz_id:
    print(f"The quiz ID for the game pin '{game_pin}' is: {quiz_id}")
else:
    print("Failed to retrieve the quiz ID. Make sure the game pin is correct and try again.")
