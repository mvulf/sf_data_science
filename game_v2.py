"""
Game 'Guess number'.
Computer guess number byself.
"""
import numpy as np

def random_predict(number:int=1) -> int:
    """Random predicting the number

    Args:
        number (int, optional): Inscribed number. Defaults to 1.

    Returns:
        int: Number of retries
    """
    
    count = 0
    
    while True:
        count += 1
        predict_number = np.random.randint(1, 101) # guessed number
        if number == predict_number:
            break # exit, if we guess
    return(count)

# print(f'Number of retries: {random_predict()}')

def score_game(random_predict:callable) -> int:
    """Mean number of retries in 1000 cases

    Args:
        random_predict (callable): Guess function

    Returns:
        int: Mean number of retries
    """

    count_ls = [] # list of retries numbers
    np.random.seed(1) # fix seed for repeatability
    random_array = np.random.randint(1, 101, size=(1000)) # list of inscribed numbers
    
    for number in random_array:
        count_ls.append(random_predict(number))
        
    score = int(np.mean(count_ls)) # calculating mean count of retries
    
    print(f'Your algorithm guesses number with {score} retrying')
    return(score)

if __name__ == '__main__':
    score_game(random_predict)