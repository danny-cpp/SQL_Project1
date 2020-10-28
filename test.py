from Login.Display import *
from Backend.Database import *

if __name__ == '__main__':
    print("Loading server...")
    server = Database('Backend/myDB.db')

    # First action is to guide the user through login process
    current_user = None
    while current_user is None:
        Display.welcomeScreen(server)



    # Then go to main menu where the user can navigate


