import random

import cv2
import numpy

# makes variable for image
image = cv2.imread("dog.jpg")

# gets width and height from image
rows = image.shape[0]
columns = image.shape[1]

# prints original width and height
print("Original size: " + str(columns) + " x " + str(rows))

# gets scale number
scale = float(input("Enter the scale factor (1.01 - 1.25 optimal): "))

# calculates new dimensions
new_rows = rows * scale
new_columns = columns * scale
# changes to integer so it is a whole number
# because pixels must be in a whole number
new_rows = int(new_rows)
new_columns = int(new_columns)

# print new dimensions
print("Scaled size: " + str(new_columns) + " x " + str(new_rows))

# makes blank image (array)
new_image = numpy.zeros((new_rows, new_columns, 3), numpy.float32)

# calculate new image copy start point
# middle row minus half height of image
row_difference = (new_rows // 2) - (rows // 2)
# middle column minus half width of image
column_difference = (new_columns // 2) - (columns // 2)

# places original image onto new image
# iterates through each row
for i in range(rows):
    # iterates through each column
    for j in range(columns):
        # new image
        # equals pixel from original image
        new_image[i + row_difference][j + column_difference] = image[i][j]

# randomizes each pixel of border with a random color from original image
# iterates through each row
for i in range(new_rows):
    # iterates through each column
    for j in range(new_columns):
        # upper border
        if i < row_difference:
            random_row = random.randint(0, rows - 1)
            random_column = random.randint(0, columns - 1)
            new_image[i][j] = image[random_row, random_row]
        # bottom border
        if i >= new_rows - row_difference:
            random_row = random.randint(0, rows - 1)
            random_column = random.randint(0, columns - 1)
            new_image[i][j] = image[random_row, random_row]
        # left border
        if j < column_difference:
            random_row = random.randint(0, rows - 1)
            random_column = random.randint(0, columns - 1)
            new_image[i][j] = image[random_row, random_row]
        # right border
        if j >= new_columns - column_difference:
            random_row = random.randint(0, rows - 1)
            random_column = random.randint(0, columns - 1)
            new_image[i][j] = image[random_row, random_row]

"""
# grayscale
# iterates through each row
for i in range(new_rows):
    # iterates through each column
    for j in range(new_columns):
        # pixel equals each pixel
        pixel = new_image[i, j]
        # blue color
        b = pixel[0]
        # green color
        g = pixel[1]
        # red color
        r = pixel[2]
        # grayscale formulaa
        gray = (b + g + r) / 3
        # replaces blue color
        pixel[0] = gray
        # replaces green color
        pixel[1] = gray
        # replaces red color
        pixel[2] = gray
"""

# saves new image
cv2.imwrite("new_dog.jpg", new_image)

# shows nwe image
cv2.imshow("new image", new_image)
