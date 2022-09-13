Language Specification: Program is written in Python 3.

====================================================================================================
Modular Multiplicative Inverse Calculator
====================================================================================================
# EXECUTING THE PROGRAM:
- command to execute: py InverseCalculator.py
- OR, double click on the InverseCalculator.py file to run.

# DETAILS OF EXECUTION:
- The program will start generating prime number.
- The program will print the test status for each odd number tested. (comment out line no 93 and 94 to disable printing these details).
- Finally after printing the prime number (N), the program will ask for next operation.

# FINDING MULTIPLICATIVE INVERSE OF ANY NUMBER (A) MODULO N:
- Enter any number (A) in decimal notation as input and press ENTER key to find the multiplicative inverse of A modulo N.
- The program will print the inverse in both decimal and binary notations.

# CHECK FOR CORRECTNESS:
- After printing the inverse, the program will calculate (A * inv) mod N and print its result. (the function is defined on line number 129 to 132, and is called on line number 146).
- Alternatively, the correctness can be verified by giving the printed multiplicative inverse (DECIMAL notation) of A as input, and checking if its inverse is same as the previous A mod N. (as done in sample output)
- After printing the result of  ( A * inv ) mod N, the program will again ask for next input. 

# TO STOP THE PROGRAM: 
- Enter anyting except a number as input and press ENTER. (or directly press ENTER, without any input)
- Again press ENTER button to close the terminal/exit the program.

Sample.txt is the sample output.
