from Login.Display import *
from Backend.Database import *
from Functionality.Menu import *

if __name__ == '__main__':
    print("Loading server...")
    server = Database('Backend/myDB.db')

    # First action is to guide the user through login process
    current_user = None
    while current_user is None:
        current_user = Display.welcomeScreen(server)

    # Then go to main menu where the user can navigate
    print("\n\nWelcome back " + current_user.getName() + "!")
    current_state = 0
    chosen_post = None
    while True:
        current_window = Menu(server, current_user, current_state, chosen_post)
        current_state, chosen_post = current_window.menuNavigate()



