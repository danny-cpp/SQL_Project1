from Login.Display import *
from Backend.Database import *
from Functionality.Menu import *
import sys

if __name__ == '__main__':
    # loading server
    # if len(sys.argv) != 2:
    #     raise ValueError('Please provide a valid path to the server. ')

    # Backend/myDB.db
    print("Loading server...")
    server = Database("Backend/myDB.db")

    # First action is to guide the user through login process
    # current_user = None
    # while current_user is None:
    #     current_user = Display.welcomeScreen(server)

    # Then go to main menu where the user can navigate
    # print("\n\nWelcome back " + current_user.getName() + "!")
    current_state = 10
    chosen_post = None
    current_window = Menu(server, current_state, chosen_post)
    while True:
        # current_window = Menu(server, current_state, chosen_post)
        current_window.setPID(chosen_post)
        current_window.setServer(server)
        current_window.setstate(current_state)
        current_state, chosen_post = current_window.menuNavigate()



