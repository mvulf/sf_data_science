"""
Kernel for game 'Guess number'.
Computer guess number byself.

Count of tests is set by test_number. 
Further it can be an attribute of game_kernel class.
"""

import numpy as np

def score_game(test_number:int=1000) -> callable:
    """Decorator for game kernels tests up to test_number times

    Args:
        test_number (int): Number of necessary tests. Defaults to 1000.

    Returns:
        callable: Function for testing game kernel
    """
    
    # Check, that number of tests more then zero
    try:
        if test_number < 1:
            raise ValueError("Test number might be more than zero."
                             + " Set one test")
    except ValueError as e:
        print(e)
        test_number = 1
    
    def test_kernel_decorator(test_kernel:callable) -> callable:
        """Decorator for calculating mean number of retries in 
        test_number cases

        Args:
            test_kernel (callable): Tested guess function

        Returns:
            callable: Mean number of attempts
        """
        
        def score_game_kernel(guess_number:int=None, min_val:int=1, \
            max_val:int=100) -> int:
            """Function for calculating mean number of attempts in 
            test_number cases 

            Args:
                guess_number (int, optional): Number for guessing. 
                    Defaults to None.
                min_val (int, optional): Minimum value of guess number. 
                    Defaults to 1.
                max_val (int, optional): Maximum value of guess number. 
                    Defaults to 100.

            Returns:
                int: Mean number of attempts
            """
            
            # Prepare result-mode for displaying
            if test_number == 1:
                res_type_str = ' '
            else:
                res_type_str = ' on average '
            
            # Get array of guess numbers
            if guess_number is None:
                np.random.seed(1) # Fix seed for repeatability
                number_array = np.random.randint(min_val, max_val+1, \
                    size=(test_number))
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
                current_attempts = test_kernel(number, min_val, \
                    max_val)
                # Check result correctness
                try:
                    if current_attempts:
                        attempts_numbers.append(current_attempts)
                    else:
                        raise ValueError('Get 0 or None')
                except ValueError as e:
                    print(e)
                    return          
            score = int(np.mean(attempts_numbers))
            
            print(f'{test_kernel.__name__} guesses {num_type_str} ' 
                  + f'in range [{min_val}, {max_val}]{res_type_str}in ' 
                  + f'{score} attempts. Total count of tests: {test_number}')
            
            return score
        
        return score_game_kernel
    
    return test_kernel_decorator


def random_predict(guess_number:int=1, min_val:int=1, max_val:int=100) -> int:
    """Random predicting the number

    Args:
        guess_number (int, optional): Guess number. Defaults to 1.
        min_val (int, optional): Minimum value of guess number. Defaults to 1.
        max_val (int, optional): Maximum value of guess number. 
            Defaults to 100.

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
        predict_number = np.random.randint(min_val, max_val+1)
        if predict_number == guess_number:
            break # Exit, if we guess
    return(count)


def random_predict_range_dividing(guess_number:int=1, min_val:int=1, \
    max_val:int=100) -> int:
    """Random predicting the number with dividing search range 
    according to more/less fedback 

    Args:
        guess_number (int, optional): Guess number. Defaults to 1.
        min_val (int, optional): Minimum value of guess number. Defaults to 1.
        max_val (int, optional): Maximum value of guess number. 
            Defaults to 100.

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
        predict_number = np.random.randint(min_val, max_val+1)
        if predict_number > guess_number:
            max_val = predict_number
        elif predict_number < guess_number:
            min_val = predict_number
        else:
            break # Exit, if we guess
    return(count)


def predict_division_two(guess_number:int=1, min_val:int=1, \
    max_val:int=100) -> int:
    """Predicting the number by getting an average value of range, 
    decreasing according to more/less fedback 

    Args:
        guess_number (int, optional): Guess number. Defaults to 1.
        min_val (int, optional): Minimum value of guess number. Defaults to 1.
        max_val (int, optional): Maximum value of guess number. 
            Defaults to 100.

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
        predict_number = (min_val+max_val) // 2
        if predict_number > guess_number:
            max_val = predict_number - 1
        elif predict_number < guess_number:
            min_val = predict_number + 1
        else:
            break # Exit, if we guess
    return(count)


if __name__ == '__main__':
    print('random_predict:', random_predict())
    print('random_predict_range_dividing:', random_predict_range_dividing())
    print('predict_division_two', predict_division_two())