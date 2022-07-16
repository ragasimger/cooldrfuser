from random import randint
from string import ascii_letters

# reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,18}$"

def rand_letters():
    alphabets = []
    letters = list(ascii_letters)
    for _ in range(6):
        rand_int = randint(0,51)
        y = letters[rand_int]
        alphabets.append(y)
    return ''.join(alphabets)

def generate_password():
    custom = "$#@!N@l#"
    letters = rand_letters()
    return custom + letters + str(randint(1,1000))

