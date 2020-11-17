from Login.Display import *
from Backend.Database import *
from Functionality.Menu import *
import sys

if __name__ == '__main__':
    # loading server
    if len(sys.argv) != 2:
        raise ValueError('Please provide a valid path to the server. ')

    if not os.path.isfile(sys.argv[1]):
        raise Exception("Not a valid database filepath")

    # Backend/myDB.db
    print("Loading server...")
    server = Database(sys.argv[1])

    logout_flag = False
    while True:
        if logout_flag:
            print("LOGOUT SUCCESSFULLY!")

        # First action is to guide the user through login process
        current_user = None
        while current_user is None:
            current_user = Display.welcomeScreen(server)

        logout_flag = True

        # Then go to main menu where the user can navigate
        print("\n\nWelcome back " + current_user.getName() + "!")
        current_state = 0
        chosen_post = None
        while current_state != 10:
            current_window = Menu(server, current_user, current_state, chosen_post)
            current_state, chosen_post = current_window.menuNavigate()


