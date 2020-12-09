import cv2
import numpy


def initialize(filename):
    image = cv2.imread(filename)
    return image


def grayscale(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return image


def gradient(image):
    columns = image.shape[1]  # height
    rows = image.shape[0]  # width
    image_copy1 = numpy.zeros((rows, columns), numpy.float64)  # x gradient
    image_copy2 = numpy.zeros((rows, columns), numpy.float64)  # y gradient

    for i in range(rows):
        for j in range(columns):
            if (j - 1) >= 0 and (j + 1) < columns:  # x gradient
                gray1 = image[i, j - 1]  # left
                gray2 = image[i, j + 1]  # right
                gradient = int(gray1) - int(gray2)
                image_copy1[i, j] = gradient

            if (i - 1) >= 0 and (i + 1) < rows:  # y gradient
                gray1 = image[i - 1, j]  # top
                gray2 = image[i + 1, j]  # bottom
                gradient = int(gray1) - int(gray2)
                image_copy2[i, j] = gradient

    return image_copy1, image_copy2  # x gradient, y gradient


def calculate_xx_yy_xy(image1, image2):  # x gradient, y gradient
    columns = image1.shape[1]
    rows = image1.shape[0]

    array1 = numpy.zeros((rows, columns), numpy.float64)  # xx
    array2 = numpy.zeros((rows, columns), numpy.float64)  # yy
    array3 = numpy.zeros((rows, columns), numpy.float64)  # xy

    array_sum1 = numpy.zeros((rows, columns), numpy.float64)  # xx
    array_sum2 = numpy.zeros((rows, columns), numpy.float64)  # yy
    array_sum3 = numpy.zeros((rows, columns), numpy.float64)  # xy

    # xx/yy/xy
    for i in range(rows):
        for j in range(columns):
            gray = image1[i, j]
            array1[i][j] = int(gray) * int(gray)  # xx

            gray = image2[i, j]
            array2[i][j] = int(gray) * int(gray)  # yy

            gray1 = image1[i, j]
            gray2 = image2[i, j]
            array3[i][j] = int(gray1) * int(gray2)  # xy

    # 9 pixel sum of xx/yy/xy
    for i in range(rows):
        for j in range(columns):
            if (i - 1) >= 0 and (j - 1) >= 0 and (i + 1) < rows and (j + 1) < columns:
                # xx
                array_sum1[i][j] = array1[i - 1][j - 1] + array1[i - 1][j] + array1[i - 1][j + 1] + \
                                   array1[i][j - 1] + array1[i][j] + array1[i][j + 1] + \
                                   array1[i + 1][j - 1] + array1[i + 1][j] + array1[i + 1][j + 1]

                # yy
                array_sum2[i][j] = array2[i - 1][j - 1] + array2[i - 1][j] + array2[i - 1][j + 1] + \
                                   array2[i][j - 1] + array2[i][j] + array2[i][j + 1] + \
                                   array2[i + 1][j - 1] + array2[i + 1][j] + array2[i + 1][j + 1]

                # xy
                array_sum3[i][j] = array3[i - 1][j - 1] + array3[i - 1][j] + array3[i - 1][j + 1] + \
                                   array3[i][j - 1] + array3[i][j] + array3[i][j + 1] + \
                                   array3[i + 1][j - 1] + array3[i + 1][j] + array3[i + 1][j + 1]

    return array_sum1, array_sum2, array_sum3  # xx, yy, xy


def cornerness(xx, yy, xy):  # xx, yy, xy
    columns = xx.shape[1]
    rows = xx.shape[0]
    array = numpy.zeros((rows, columns), numpy.float64)  # cornerness values

    for i in range(rows):
        for j in range(columns):
            det = (xx[i][j] * yy[i][j]) - ((xy[i][j]) ** 2)
            trace = xx[i][j] + yy[i][j]

            array[i][j] = det - (0.05 * (trace ** 2))

    return array  # cornerness values


def ranking_cornerness(array, percentage):  # cornerness values, percentage (ex. 90 = 90%)
    columns = array.shape[1]
    rows = array.shape[0]
    threshold = numpy.zeros((rows, columns), numpy.float64)  # 0 or 1 values

    largest = 0
    for i in range(rows):
        for j in range(columns):
            if array[i][j] > largest:
                largest = array[i][j]

    test = (percentage / 100) * largest
    for i in range(rows):
        for j in range(columns):
            if array[i][j] > test:
                threshold[i][j] = 1
            else:
                threshold[i][j] = 0

    return threshold  # marked locations


def ranking_number(array, number):  # cornerness values, number of circles
    columns = array.shape[1]
    rows = array.shape[0]
    array_copy = numpy.zeros((rows, columns), numpy.float64)  # cornerness values
    threshold = numpy.zeros((rows, columns), numpy.float64)  # 0 or 1 values

    # copies cornerness values
    for i in range(rows):
        for j in range(columns):
            array_copy[i][j] = array[i][j]

    # calculates largest values
    # places index values into list
    largest_list = []
    largest = 0
    i_reset = 0
    j_reset = 0
    for val in range(number):
        for i in range(rows):
            for j in range(columns):
                if array_copy[i][j] > largest:
                    largest = array_copy[i][j]
                    i_reset = i
                    j_reset = j
        largest_list.append([i_reset, j_reset])
        array_copy[i_reset][j_reset] = 0
        largest = 0

    # marks index values with 1
    for index in largest_list:
        threshold[index[0], index[1]] = 1

    return threshold  # marked locations


def draw_circles(array, image):
    columns = array.shape[1]
    rows = array.shape[0]

    for i in range(rows):
        for j in range(columns):
            if array[i][j] == 1:
                cv2.circle(image, (j, i), 3, (0, 0, 255), -1)  # draws circles

    return image


def visualize_grayscale(array):  # cornerness values
    columns = array.shape[1]
    rows = array.shape[0]
    visualize = numpy.zeros((rows, columns), numpy.float64)  # grayscale

    largest = 0
    smallest = 0
    for i in range(rows):
        for j in range(columns):
            if array[i][j] > largest:
                largest = array[i][j]
            if array[i][j] < smallest:
                smallest = array[i][j]

    for i in range(rows):
        for j in range(columns):
            visualize[i][j] = ((array[i][j] - smallest) / (largest - smallest)) * 255

    return visualize


def visualize_color(array):  # cornerness values
    columns = array.shape[1]
    rows = array.shape[0]
    visualize = numpy.zeros((rows, columns, 3), numpy.float64)  # colors

    largest = 0
    smallest = 0
    for i in range(rows):
        for j in range(columns):
            if array[i][j] > largest:
                largest = array[i][j]
            if array[i][j] < smallest:
                smallest = array[i][j]

    difference = largest - smallest
    first = 0.25 * difference
    second = 0.5 * difference
    third = 0.75 * difference
    count1 = 0
    count2 = 0
    count3 = 0
    count4 = 0
    for i in range(rows):
        for j in range(columns):
            if array[i][j] <= first and array[i][j] >= smallest:  # green - blue (0,0-255,255)
                visualize[i][j][0] = 255
                visualize[i][j][1] = 255 - (((array[i][j] - smallest) / (first - smallest)) * 255)
                visualize[i][j][2] = 0
                count1 = count1 + 1

            if array[i][j] <= second and array[i][j] > first:  # yellow - green (0-255,255,0)
                visualize[i][j][0] = 0
                visualize[i][j][1] = 255
                visualize[i][j][2] = 255 - (((array[i][j] - first) / (second - first)) * 255)
                count2 = count2 + 1

            if array[i][j] <= third and array[i][j] > second:  # orange - yellow (255,165-255,0)
                visualize[i][j][0] = 0
                visualize[i][j][1] = 165 + ((((array[i][j] - second) / (third - second)) * 255) / 1.5454)
                visualize[i][j][2] = 255
                count3 = count3 + 1

            if array[i][j] > third and array[i][j] <= largest:  # red - orange (255,0-165,0)
                visualize[i][j][0] = 0
                visualize[i][j][1] = (((array[i][j] - third) / (largest - third)) * 255) / 1.5454
                visualize[i][j][2] = 255
                count4 = count4 + 1

    print(str(smallest) + " smallest")
    print(str(largest) + " largest")
    print(str(difference) + " difference")

    print(str(smallest) + " - " + str(first) + " first range")
    print(str(first) + " - " + str(second) + " second range")
    print(str(second) + " - " + str(third) + " third range")
    print(str(third) + " - " + str(largest) + " fourth range")

    print(str(count1) + " pixels in first range")
    print(str(count2) + " pixels in second range")
    print(str(count3) + " pixels in third range")
    print(str(count4) + " pixels in fourth range")

    return visualize


def main():
    filename = "image.jpg"

    image1 = initialize(filename)

    image_grayscale = grayscale(image1)  # grayscale

    x_gradient, y_gradient = gradient(image_grayscale)  # gradients

    array_xx, array_yy, array_xy = calculate_xx_yy_xy(x_gradient, y_gradient)  # xx, yy, xy

    r = cornerness(array_xx, array_yy, array_xy)  # cornerness

    marked_corners = ranking_cornerness(r,5) #rank by percentage of cornerness
    ##    marked_corners = ranking_number(r, 200) #rank by number of corners

    image2 = initialize(filename)

    image_circles = draw_circles(marked_corners, image2)

    ##    gray = visualize_grayscale(r)
    ##    color = visualize_color(r)

    cv2.imwrite("results_" + filename, image_circles)
    cv2.imshow(filename, image_circles)


main()
