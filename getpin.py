import curses
import requests

def get_quiz_id(pin):
    url = f'https://kahoot.it/rest/challenges/pin/{pin}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data.get('id', 'Quiz ID not found')
    except requests.exceptions.RequestException as e:
        return f'Error fetching quiz ID: {e}'

def main(stdscr):
    curses.curs_set(0)  
    stdscr.clear()
    stdscr.addstr(0, 0, "Enter Kahoot Quiz Pin:")
    stdscr.refresh()

    pin = stdscr.getstr(1, 0).decode('utf-8')
    
    quiz_id = get_quiz_id(pin)

    stdscr.clear()
    stdscr.addstr(0, 0, f"Quiz ID: {quiz_id}")
    stdscr.addstr(2, 0, "Press any key to exit...")
    stdscr.refresh()
    stdscr.getch()

curses.wrapper(main)
