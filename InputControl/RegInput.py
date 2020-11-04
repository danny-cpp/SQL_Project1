import re
from getpass import getpass


class InputControl:
    # Replacing input
    @staticmethod
    def Input(prompt='', enforce_lower=False, is_pwd=False, accept_blank=False, allow_special=False):
        if is_pwd:
            user_inp = getpass(prompt)
            check = re.match("[a-zA-Z0-9]+$", user_inp)
            while not check:
                user_inp = getpass("Password can only contains alphanumeric character. " + prompt)
                check = re.match("[a-zA-Z0-9]+$", user_inp)

            return user_inp

        user_inp = input(prompt)

        if user_inp == 'quit':
            exit()

        if not accept_blank:
            while user_inp == '':
                new_prompt = "Cannot accept blank, please try again. " + prompt
                user_inp = input(new_prompt)

        special_char = ['\'', '-']
        if not allow_special:
            for c in special_char:
                while re.search(c, user_inp):
                    user_inp = input(f"Cannot accept '{c}' as input. " + prompt)
                    break
        else:
            user_inp = user_inp.replace("'", "''")
            user_inp = user_inp.replace("-", "")

        if enforce_lower:
            user_inp = user_inp.lower()

        return user_inp


if __name__ == '__main__':

    a = "a cat where a hat"
    r1 = re.findall(".at", a)
    r2 = re.match(".at", a)
    print(r1, r2)

    u = InputControl.Input(allow_special=True)

    check = re.match("[a-zA-Z0-9]+$", u)

    print(u)
    print(check)
    if not check:
        print("wrong")
    else:
        print("true")