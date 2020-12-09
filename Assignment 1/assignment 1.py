import math

import cv2
import numpy


def multiply_matrices(array1, array2):
    if (array1.shape[1] == array2.shape[0]):
        rows = array1.shape[0]
        columns = array2.shape[1]
        product = numpy.zeros((rows, columns), numpy.float64)
        for i in range(len(array1)):
            for j in range(len(array2[0])):
                for k in range(len(array2)):
                    product[i][j] += array1[i][k] * array2[k][j]
        return product
    return "Invalid matrix dimensions"


def initialize(filename):  # pass the filename
    image = cv2.imread(filename)  # saves image as variable

    return image  # returns the image


def border(image):  # pass the image
    columns = image.shape[1]  # gets width from image
    rows = image.shape[0]  # gets height from image

    print("Original size: " + str(columns) + " x " + str(rows) + "\n")  # prints original width and height

    scale = float(input("Enter the scale factor: "))  # gets scale number

    new_columns = columns * scale  # calculates new width
    new_rows = rows * scale  # calculates new height

    new_columns = int(new_columns)  # converts width to integer
    new_rows = int(new_rows)  # converts height to integer

    print("\nScaled size: " + str(new_columns) + " x " + str(new_rows))  # print new dimensions

    new_image = numpy.zeros((new_rows, new_columns, 3), numpy.float32)  # makes blank image (array)

    # calculate new image copy start point
    column_difference = (new_columns // 2) - (columns // 2)  # middle column minus half width of image
    row_difference = (new_rows // 2) - (rows // 2)  # middle row minus half height of image

    # places original image onto new image
    for y in range(rows):  # iterates through each row
        for x in range(columns):  # iterates through each column
            new_image[y + row_difference][x + column_difference] = image[y][
                x]  # transfers pixel information using coordinates

    return new_image  # returns image with border


def rotate(new_image):  # pass border image
    new_columns = new_image.shape[1]  # gets width from image
    new_rows = new_image.shape[0]  # gets height from image

    theta_degrees = float()  # variable for input
    total_degrees = float()  # variable for sum of inputs
    while theta_degrees != -1:  # continues until input is -1
        theta_degrees = float(input("\nEnter number of degrees to rotate (-1 to stop): "))  # gets input
        if theta_degrees != -1:  # only continues if input isn't -1
            total_degrees = total_degrees + theta_degrees  # increases sum of degrees
            theta_radians = total_degrees * (math.pi / 180)  # converts degrees to radians

            rotated_image = numpy.zeros((new_rows, new_columns, 3), numpy.float32)  # makes blank image (array)

            # rotates image
            for y in range(new_rows):  # iterates through each row
                for x in range(new_columns):  # iterates through each column

                    x_t = (x - (new_columns / 2))  # converts x with origin in center (transposed x)
                    y_t = (y - (new_rows / 2))  # converts y with origin in center (transposed y)

                    x_r = ((x_t * math.cos(theta_radians)) - (
                                y_t * math.sin(theta_radians)))  # rotates x pixel (rotated x)
                    y_r = ((x_t * math.sin(theta_radians)) + (
                                y_t * math.cos(theta_radians)))  # rotates y pixel (rotated y)

                    x_f = (x_r + (new_columns / 2))  # converts x with default origin (final x)
                    y_f = (y_r + (new_rows / 2))  # converts y with default origin (final y)

                    x_f = int(x_f)  # converts final x to int (pixel coordinate)
                    y_f = int(y_f)  # converts final y to int (pixel coordinate)

                    if (x_f < new_columns) and (y_f < new_rows):  # cuts off pixels that are out of range
                        rotated_image[y_f][x_f] = new_image[y][x]  # transfers pixel information using coordinates

    return rotated_image  # returns rotated image


def color_error(border_image, rotated_image, theta_degrees):  # pass border image and rotated image
    new_columns = border_image.shape[1]  # gets width from image
    new_rows = border_image.shape[0]  # gets height from image

    distance_sum = float(0)
    theta_radians = theta_degrees * (math.pi / 180)

    for y in range(new_rows):  # iterates through each row
        for x in range(new_columns):  # iterates through each column

            x_t = (x - (new_columns / 2))  # converts x with origin in center (transposed x)
            y_t = (y - (new_rows / 2))  # converts y with origin in center (transposed y)

            x_r = ((x_t * math.cos(theta_radians)) - (y_t * math.sin(theta_radians)))  # rotates x pixel (rotated x)
            y_r = ((x_t * math.sin(theta_radians)) + (y_t * math.cos(theta_radians)))  # rotates y pixel (rotated y)

            x_f = (x_r + (new_columns / 2))  # converts x with default origin (final x)
            y_f = (y_r + (new_rows / 2))  # converts y with default origin (final y)

            x_f = int(x_f)  # converts final x to int (pixel coordinate)
            y_f = int(y_f)  # converts final y to int (pixel coordinate)

            if (x_f < new_columns) and (y_f < new_rows):
                border_pixel = border_image[y, x]
                border_b = border_pixel[0]  # blue color
                border_g = border_pixel[1]  # green color
                border_r = border_pixel[2]  # red color

                rotated_pixel = rotated_image[y_f, x_f]
                rotated_b = rotated_pixel[0]  # blue color
                rotated_g = rotated_pixel[1]  # green color
                rotated_r = rotated_pixel[2]  # red color

                distance = float(
                    ((border_b - rotated_b) ** 2) + ((border_g - rotated_g) ** 2) + ((border_r - rotated_r) ** 2))
                distance_sqrt = float(math.sqrt(distance))
                distance_sum = distance_sum + distance_sqrt

    total_pixels = float(new_columns * new_rows)
    color_error_value = float(distance_sum / total_pixels)

    return color_error_value


def rounding_error(border_image, rotated_image, theta_degrees):
    new_columns = border_image.shape[1]  # gets width from image
    new_rows = border_image.shape[0]  # gets height from image

    error_sum = float(0)
    theta_radians = theta_degrees * (math.pi / 180)

    for y in range(new_rows):  # iterates through each row
        for x in range(new_columns):  # iterates through each column

            x_t = (x - (new_columns / 2))  # converts x with origin in center (transposed x)
            y_t = (y - (new_rows / 2))  # converts y with origin in center (transposed y)

            x_r = ((x_t * math.cos(theta_radians)) - (y_t * math.sin(theta_radians)))  # rotates x pixel (rotated x)
            y_r = ((x_t * math.sin(theta_radians)) + (y_t * math.cos(theta_radians)))  # rotates y pixel (rotated y)

            x_f = (x_r + (new_columns / 2))  # converts x with default origin (final x)
            y_f = (y_r + (new_rows / 2))  # converts y with default origin (final y)

            x_float = x_f  # saves float value
            y_float = y_f  # saves float value

            x_f = int(x_f)  # converts final x to int (pixel coordinate)
            y_f = int(y_f)  # converts final y to int (pixel coordinate)

            if (x_f < new_columns) and (y_f < new_rows):
                x_difference = x_float - x_f
                y_difference = y_float - y_f
                error_sum = error_sum + x_difference + y_difference

    total_pixels = float(new_columns * new_rows)
    rounding_error_value = float(error_sum / total_pixels)

    return rounding_error_value


def main():
    array1 = numpy.zeros((3, 4), numpy.float64)
    array1[0] = [1, 2, 3, 4]
    array1[1] = [5, 6, 7, 8]
    array1[2] = [-1, -2, -3, -4]

    array2 = numpy.zeros((4, 3), numpy.float64)
    array2[0] = [1, 2, 3]
    array2[1] = [-7, 8, -9]
    array2[2] = [10, 20, 30]
    array2[3] = [3, 5, 7]

    print("array1")
    print(array1)
    print("array2")
    print(array2)
    print("array1 * array2")
    print(multiply_matrices(array1, array2))
    print("")

    filename = "Ramen.jpg"  # makes variable for image
    theta_degrees = 360  # makes variable for degrees

    image = initialize(filename)  # initialize returns image
    border_image = border(image)  # add_border returns image with border
    rotated_image = rotate(border_image)  # rotate returns rotated image

    color_error_value = color_error(border_image, rotated_image, theta_degrees)
    print("\nColor error = " + str(color_error_value))

    rounding_error_value = rounding_error(border_image, rotated_image, theta_degrees)
    print("\nRounding error = " + str(rounding_error_value))

    cv2.imwrite("rotated" + filename, rotated_image)
    cv2.imshow("new" + filename, rotated_image)


main()
