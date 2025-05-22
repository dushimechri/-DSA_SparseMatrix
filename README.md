Implementation Summary

The SparseMatrix class is designed with a dictionary-centric structure that:

Keeps track of only the non-zero values in the form of (row, column): value

Minimizes memory usage by excluding zero-value elements

Enables efficient matrix operations by bypassing unnecessary zero computations

Avoids reliance on any pre-existing matrix or template libraries


This implementation adheres strictly to mathematical principles for matrix manipulation:

Addition and subtraction are performed only when both matrices share identical dimensions

Multiplication is valid only if the number of columns in the first matrix equals the number of rows in the second



---

Sparse Matrix Operations in Python

This project delivers a high-performance Python solution for performing sparse matrix operations, aimed primarily at students working on Data Structures and Algorithms assignments. The solution is crafted to optimize both memory efficiency and computational performance when working with large matrices.

Assignment Context

The application fulfills the specifications for Assignment 2 in the Data Structures and Algorithms for Engineers course. It provides:

1. An efficient structure for representing sparse matrices


2. The ability to load matrices from formatted text files


3. Fundamental matrix operations like addition, subtraction, and multiplication


4. Comprehensive validation checks and error management



Setup Instructions

To install the project, run:

git clone https://github.com/dushimechri/DSA_SparseMatrix.git
cd DSA_SparseMatrix


---

How to Use

Running from the Command Line

Execute the following:

python main.py

Upon launch, the program will:

1. Search for input matrices in the sample_inputs/ folder


2. Request the user to choose an operation


3. Perform the selected operation and store the outcome




---

Input File Structure

The tool reads matrices from files that follow this structure:

rows=<number_of_rows> cols=<number_of_columns>
(<row>, <column>, <value>) (<row>, <column>, <value>) ...

Example:

rows=8433 cols=3180 (0, 381, -694) (0, 128, -838) (0, 639, 857)

Formatting Rules:

Spaces are ignored

Only integer values are supported

Zero entries are omitted and not included in the file

Input is validated to ensure the format is correct

API Functionality Overview

The SparseMatrix class offers these features:

Constructor:

matrix = SparseMatrix(rows, cols)  # Initialize an empty matrix

File Loader:

matrix = SparseMatrix.from_file(filepath)  # Create matrix from a file

Element Access:

value = matrix.get_element(row, col)  # Retrieves the value or 0 if unset
matrix.set_element(row, col, value)   # Sets a value or removes it if zero

Matrix Operations:

result = matrix1.add(matrix2)         # Throws error if dimensions mismatch
result = matrix1.subtract(matrix2)    # Throws error if dimensions mismatch
result = matrix1.multiply(matrix2)    # Throws error if sizes are incompatible 
