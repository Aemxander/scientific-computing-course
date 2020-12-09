import copy

import numpy


def create_augmented_matrix():
    array = numpy.empty(12).reshape(3, 4)  # matrix (3 rows x 4 columns) (12 values)
    array[0] = [1, 0, 2, 1]
    array[1] = [2, -1, 3, -1]
    array[2] = [4, 1, 8, 2]
    return array  # returns array


def create_matrix():
    array = numpy.empty(9).reshape(3, 3)  # matrix (3 rows x 3 columns) (9 values)
    array[0] = [1, -1, 0]
    array[1] = [-2, 2, -1]
    array[2] = [0, 1, -2]
    return array  # returns array


def gauss_jordan(array):
    rows = array.shape[0]  # height
    columns = array.shape[1]  # width

    swap_index = 0  # index of swappable rows
    column_max = 0  # max value in column
    abs_column_max = 0  # absolute max value in column
    max_row = 0  # index of row w/ column max

    for column in range(0, columns - 1):  # once per column (excluding result column)

        for row in range(swap_index, rows):  # row swap test
            if abs(array[row][column]) > abs(column_max):  # max magnitude in column
                abs_column_max = abs(array[row][column])
                column_max = array[row][column]
                max_row = row

        if column_max != 0:  # cannot divide by zero
            array[max_row] = array[max_row] / column_max

        if swap_index < rows:  # row swap
            temp_row = copy.deepcopy(array[swap_index])
            array[swap_index] = array[max_row]
            array[max_row] = temp_row

        for row in range(0, rows):  # matrix operation
            if row != swap_index:
                if swap_index < rows:
                    array[row] = array[row] - (array[row][column] * array[swap_index])

        swap_index = swap_index + 1  # increment
        abs_column_max = 0  # reset
        column_max = 0  # reset
        max_row = 0  # reset

    return array  # returns array


def matrix_inverse(array):
    rows = array.shape[0]  # height
    columns = array.shape[1]  # width

    if rows != columns:
        return "Matrix rows and columns must match"

    augmented = numpy.empty(rows * (columns * 2)).reshape(rows, columns * 2)  # matrix (rows x (columns*2))
    new_rows = augmented.shape[0]  # height
    new_columns = augmented.shape[1]  # width

    for row in range(0, rows):  # copies original array
        for column in range(0, columns):
            augmented[row][column] = array[row][column]

    for row in range(0, new_rows):  # adds identity matrix
        for column in range(columns, new_columns):
            if row == (column - rows):
                augmented[row][column] = 1
            else:
                augmented[row][column] = 0

    swap_index = 0  # index of swappable rows
    column_max = 0  # max value in column
    abs_column_max = 0  # absolute max value in column
    max_row = 0  # index of row w/ column max

    for column in range(0, columns):  # once per original columns

        for row in range(swap_index, rows):  # row swap test
            if abs(augmented[row][column]) > abs(column_max):  # max magnitude in column
                abs_column_max = abs(augmented[row][column])
                column_max = augmented[row][column]
                max_row = row

        if column_max != 0:  # cannot divide by zero
            augmented[max_row] = augmented[max_row] / column_max

        if swap_index < rows:  # row swap
            temp_row = copy.deepcopy(augmented[swap_index])
            augmented[swap_index] = augmented[max_row]
            augmented[max_row] = temp_row

        for row in range(0, rows):  # matrix operation
            if row != swap_index:
                if swap_index < rows:
                    augmented[row] = augmented[row] - (augmented[row][column] * augmented[swap_index])

        swap_index = swap_index + 1  # increment
        abs_column_max = 0  # reset
        column_max = 0  # reset
        max_row = 0  # reset

    inverse = numpy.empty(rows * columns).reshape(rows, columns)  # matrix (rows x columns)

    for row in range(0, rows):  # copies inverse array
        for column in range(columns, new_columns):
            inverse[row][column - columns] = augmented[row][column]

    return inverse  # returns array


def gaussian(array):
    rows = array.shape[0]  # height
    columns = array.shape[1]  # width

    swap_index = 0  # index of swappable rows
    column_max = 0  # max value in column
    max_row = 0  # index of row w/ column max

    for column in range(0, columns - 1):  # once per column (excluding result column)

        for row in range(swap_index, rows):  # row swap test
            if abs(array[row][column]) > abs(column_max):  # max magnitude in column
                column_max = array[row][column]
                max_row = row

        if swap_index < rows:  # row swap
            temp_row = copy.deepcopy(array[swap_index])
            array[swap_index] = array[max_row]
            array[max_row] = temp_row

        for row in range(swap_index, rows):  # matrix operation
            if row != swap_index:
                if swap_index < rows:
                    array[row] = array[row] - ((array[row][column] / column_max) * array[swap_index])

        swap_index = swap_index + 1  # increment
        column_max = 0  # reset
        max_row = 0  # reset

    # bootleg algebra code
    # should make this scale
    c = array[rows - 1][columns - 1] / array[rows - 1][columns - 2]
    b = (array[rows - 2][columns - 1] - (c * array[rows - 2][columns - 2])) / array[rows - 2][columns - 3]
    a = (array[rows - 3][columns - 1] - (c * array[rows - 3][columns - 2]) - (b * array[rows - 3][columns - 3])) / \
        array[rows - 3][columns - 4]

    return [array, a, b, c]  # returns list


def gaussian_determinant(array):
    rows = array.shape[0]  # height
    columns = array.shape[1]  # width

    swap_index = 0  # index of swappable rows
    column_max = 0  # max value in column
    max_row = 0  # index of row w/ column max
    swaps = 0  # number of swaps

    for column in range(0, columns):  # once per column

        for row in range(swap_index, rows):  # row swap test
            if abs(array[row][column]) > abs(column_max):  # max magnitude in column
                column_max = array[row][column]
                max_row = row

        if max_row != swap_index:  # row swap
            if swap_index < rows:
                temp_row = copy.deepcopy(array[swap_index])
                array[swap_index] = array[max_row]
                array[max_row] = temp_row
                swaps = swaps + 1

        for row in range(swap_index, rows):  # matrix operation
            if row != swap_index:
                if swap_index < rows:
                    array[row] = array[row] - ((array[row][column] / column_max) * array[swap_index])

        swap_index = swap_index + 1  # increment
        column_max = 0  # reset
        max_row = 0  # reset

    determinant = 1  # default multiplication value

    for index in range(0, rows):  # calculates determinant
        determinant = determinant * array[index][index]
    determinant = determinant * (-1) ** swaps

    return [array, determinant]  # returns list


def format_array(array):  # formats array ".2f"
    formatted = copy.deepcopy(array)
    rows = formatted.shape[0]  # height
    columns = formatted.shape[1]  # width

    for row in range(0, rows):
        for column in range(0, columns):
            formatted[row][column] = round(formatted[row][column], 2)

    return formatted


def main():
    array1 = create_augmented_matrix()
    print("Augmented Array")
    print(array1)

    array_gj = gauss_jordan(array1)
    print("\nGauss-Jordan Elimination")
    print(array_gj)

    array2 = create_augmented_matrix()

    array_g = gaussian(array2)
    formatted_array_g = format_array(array_g[0])
    print("\nGaussian Elimination")
    print("A = " + str(array_g[1]) + "; B = " + str(array_g[2]) + "; C = " + str(array_g[3]))
    print(formatted_array_g)

    array3 = create_matrix()
    print("\nArray")
    print(array3)

    array_mi = matrix_inverse(array3)
    print("\nInverse using Gauss-Jordan")
    print(array_mi)

    array4 = create_matrix()

    array_gd = gaussian_determinant(array4)
    print("\nGaussian Determinant")
    print("Determinant = " + str(array_gd[1]))
    print(array_gd[0])


main()
