"""
Kernel for game 'Guess number'.
Computer guess number byself.

Count of tests is set by test_number. 
Further it can be an attribute of game_kernel class.
"""

import numpy as np

# Set up count of tests
test_number = 1000


def score_game(test_number:int=1) -> callable:
    """Decorator for game kernels tests up to test_number times

    Args:
        test_number (int): Number of necessary tests. Defaults to 1.

    Returns:
        callable: Function for testing game kernel
    """
    
    # Check, that number of tests more then zero
    try:
        if test_number < 1:
            raise ValueError("Test number might be more than zero. Set one test")
    except ValueError as e:
        print(e)
        test_number = 1
    
    def test_kernel_decorator(test_kernel:callable) -> callable:
        """Decorator for calculating mean number of retries in test_number cases

        Args:
            test_kernel (callable): Tested guess function

        Returns:
            callable: Mean number of attempts
        """
        
        def score_game_kernel(guess_number:int=None, min_val:int=1, max_val:int=100) -> int:
            """Function for calculating mean number of attempts in test_number cases 

            Args:
                guess_number (int, optional): Number for guessing. Defaults to None.
                min_val (int, optional): Minimum value of guess number. Defaults to 1.
                max_val (int, optional): Maximum value of guess number. Defaults to 100.

            Returns:
                int: Mean number of attempts
            """
            
            # if test_number == 1:
            #     # Get attempts for single test
            #     if guess_number is None: # Is used because theoretically guess_number can be equal to 0
            #         guess_number = np.random.randint(min_val, max_val+1)
            #         num_type_str = 'a random'
            #     else:
            #         num_type_str = 'your'
                   
            #     score = test_kernel(guess_number, min_val, max_val)
            #     print(f'{test_kernel.__name__} guesses {num_type_str} number in range [{min_val}, {max_val}] with {score} attempts')
            
            # else: 
            
            # Get array of guess numbers
            if guess_number is None:
                np.random.seed(1) # Fix seed for repeatability
                number_array = np.random.randint(min_val, max_val+1, size=(test_number))
                if test_number == 1:
                    num_type_str = 'a random number'
                else:
                    num_type_str = 'random numbers'
            else:
                number_array = np.full(test_number, guess_number)
                num_type_str = 'your number'
            
            # Calculating mean count of attempts for test_number tests
            attempts_numbers = []
            for number in number_array:
                attempts_numbers.append(test_kernel(number, min_val, max_val))
            score = int(np.mean(attempts_numbers))
            print(f'{test_kernel.__name__} guesses {num_type_str} in range [{min_val}, {max_val}] in an average of {score} attempts. Total count of tests: {test_number}')
            
            return score
        
        return score_game_kernel
    
    return test_kernel_decorator


@score_game(test_number)
def random_predict(guess_number:int=1, min_val:int=1, max_val:int=100) -> int:
    """Random predicting the number

    Args:
        guess_number (int, optional): Guess number. Defaults to 1.
        min_val (int, optional): Minimum value of guess number. Defaults to 1.
        max_val (int, optional): Maximum value of guess number. Defaults to 100.

    Returns:
        int: Number of attempts
    """
    
    count = 0
    
    # Check, that guess number in guess range
    try:
        if not(min_val<=guess_number<=max_val):
            raise ValueError("Guess number out of range")
    except ValueError as e:
        print(e)
        return
        
    while True:
        count += 1
        predict_number = np.random.randint(min_val, max_val+1) # Guessed number
        if guess_number == predict_number:
            break # Exit, if we guess
    return(count)


@score_game(test_number)
def random_predict_range_dividing(guess_number:int=1, min_val:int=1, max_val:int=100) -> int:
    """Random predicting the number with dividing search range according to more/less fedback 

    Args:
        guess_number (int, optional): Guess number. Defaults to 1.
        min_val (int, optional): Minimum value of guess number. Defaults to 1.
        max_val (int, optional): Maximum value of guess number. Defaults to 100.

    Returns:
        int: Number of attempts
    """
    
    count = 0
    
    # Check, that guess number in guess range
    try:
        if not(min_val<=guess_number<=max_val):
            raise ValueError("Guess number out of range")
    except ValueError as e:
        print(e)
        return
        
    while True:
        count += 1
        predict_number = np.random.randint(min_val, max_val+1) # Guessed number
        if guess_number == predict_number:
            break # Exit, if we guess
    return(count)


if __name__ == '__main__':
    random_predict()