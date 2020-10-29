from Login.Display import *
from Backend.Database import *
from Functionality.Menu import *

if __name__ == '__main__':
    print("Loading server...")
    server = Database('Backend/myDB.db')

    # First action is to guide the user through login process
    # current_user = None
    # while current_user is None:
    #     current_user = Display.welcomeScreen(server)

    # Then go to main menu where the user can navigate
    current_user = User("u100", "Steve Jobs", "abcde", "San Francisco", "2020-09-09")

    current_state = 0
    while True:
        current_window = Menu(server, current_user, current_state)
        current_state = current_window.menuNavigate()



