import requests

def get_kahoot_quiz_id(pin):
    url = f"https://kahoot.it/reserve/session/{pin}/?"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)import requests
import json

def reserve_session(pin):
    try:
        response = requests.post(f'https://play.kahoot.it/reserve/session/{pin}/')
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as err:
        print("Error reserving session: ", err)
        return None

def solve_challenge(challenge):
    pass

game_pin = input("Enter the Kahoot game PIN: ")

reservation = reserve_session(game_pin)

if reservation:
    challenge = reservation.get('challenge')

    if challenge:
        quiz_id = solve_challenge(challenge)
        print('Quiz ID: ', quiz_id)
    else:
        print('No challenge found in the response.')
else:
    print('Failed to reserve a Kahoot session.')

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
    print("Failed to retrieve the quiz ID.")
