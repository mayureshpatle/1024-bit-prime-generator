# 128-bit Polynomial Multiplication in $GF(2^{128})$

Language Specification: Program is written in Python 3.

# AIM: 
To find the multiplication of two 128-bit polynomials in $𝐺𝐹(2^{128})$ modulo prime polynomial $𝑥^{128} + 𝑥^7 + 𝑥^2 + 𝑥 + 1$

# EXECUTING THE PROGRAM:
- command to execute: py PolyMul.py
- OR, double click on the PolyMul.py file and select run using python 3.

# INPUT FORMAT:
- The program  reads two  sequences of integers representing the input polynomials
- The polynomials are represented as a sequence of SPACE SEPARATED integers
- For example, $x^8 + x^2 + 1$ will be represented as: 8 2 1
- The integers can be entered in any order (not necessarily decreasing)
- If same integer is entered more than once for the same polynomial, then it will be considered only once, for example 7 7 1 will be considered as 7 1
- These integers must be between 127 to 0 (both inclusive) 

# OUTPUT FORMAT:
- The program outputs the sequence of integers representing the output polynomial.
- Same as input format, but the integers will always be in decreasing order (with no duplicates)

# DETAILS OF EXECUTION:
- The program will ask for two 128-bit polynomial (as described in INPUT FORMAT).
- Inputs that don't follow INPUT FORMAT will generate Invalid Input Error.
- Finally after printing the result (or Error), the program will ask for next operation.

# GIVING ANOTHER INPUT:
- Enter 1 when prompted (after result or error) and press ENTER key to run for another input.

# TO STOP THE PROGRAM: 
- Enter anyting except 1 as input (after result or error) and press ENTER. (or directly press ENTER, without any input)
- Again press ENTER button to close the terminal/exit the program.

### sample.txt is the sample output.
