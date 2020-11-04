from getpass import getpass


class InputControl:
    # Replacing input
    @staticmethod
    def Input(prompt, enforce_lower=False, is_pwd=False):
        if is_pwd:
            user_inp = getpass(prompt)
            return user_inp

        user_inp = input(prompt)

        if user_inp == 'quit':
            exit()

        if enforce_lower:
            user_inp = user_inp.lower()

        return user_inp


if __name__ == '__main__':
    inp = InputControl.my_input("enter: ", is_pwd=True)
    print(inp)