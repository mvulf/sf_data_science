# Project 0. Game: Guess number

## Content

[1. Project description](https://github.com/mvulf/sf_data_science/tree/main/project_0/README.md#Project-description)

[2. Case details](https://github.com/mvulf/sf_data_science/tree/main/project_0/README.md#Case-details)

[3. Data specification](https://github.com/mvulf/sf_data_science/tree/main/project_0/README.md#Data-specification)

[4. Project stages](https://github.com/mvulf/sf_data_science/tree/main/project_0/README.md#Project-stages)

[5. Results](https://github.com/mvulf/sf_data_science/tree/main/project_0/README.md#Results)

[6. Conclusion](https://github.com/mvulf/sf_data_science/tree/main/project_0/README.md#Conclusion)

### Project description

It's a simple project for creating project-template in GitHub.

Goal: guess a random number for a minimum number of attempts.

:arrow_up:[to content](https://github.com/mvulf/sf_data_science/tree/main/project_0/README.md#Content)

### Case details
Necessary to write a program for guessing a random number for a minimum number of attempts.

**Conditions:**
- There is a random number in range 0 to 100. The program might guess the random number.
- Algorithm can get information about qualitative difference: is a predict number more or less then the random number.

**Quality metric**

Mean number of attempts in case of 1000 repeating. Might be less then 20.

**Practice:**
- Writing Python-code according to PEP-8.
- Working with IDE and GitHub.

:arrow_up:[to content](https://github.com/mvulf/sf_data_science/tree/main/project_0/README.md#Content)

### Data specification
No external data.

:arrow_up:[to content](https://github.com/mvulf/sf_data_science/tree/main/project_0/README.md#Content)

### Project stages
1. Repository design.

2. Base game kernel design.
    
    - Function decorator have been created for retrieving quality metric: mean number of attempts. There can be different values of test numbers.
    - The game kernel has the possibility to get different range of guessing value. It's possible to set a random or manual value for guessing.
    - The game kernel has different checks for the received values.
 
3. Guess algorithm design.


:arrow_up:[to content](https://github.com/mvulf/sf_data_science/tree/main/project_0/README.md#Content)

### Results

Two algorithms with satisfied metrics have been created.

- Algorithm 'random_predict_range_dividing' predicting the number with dividing search range according to "more/less" fedback.
- Algorithm 'predict_division_two' predicting the number by getting an average value of range, which is decreasing according to "more/less" fedback.

Both algorithms were compared with random method:
- 'random_predict' guesses random numbers in range [1, 100] on average in 101 attempts. Total count of tests: 1000
- 'random_predict_range_dividing' guesses random numbers in range [1, 100] on average in 9 attempts. Total count of tests: 1000
- 'predict_division_two' guesses random numbers in range [1, 100] on average in 5 attempts. Total count of tests: 1000

:arrow_up:[to content](https://github.com/mvulf/sf_data_science/tree/main/project_0/README.md#Content)

### Conclusion

Algorithm 'predict_division_two' is the shortest method for guessing a random number in comparison with other introduced methods. It guesses random numbers in range [1, 100] on average in 5 attempts. Total count of tests was 1000.

:arrow_up:[to content](https://github.com/mvulf/sf_data_science/tree/main/project_0/README.md#Content)