"""
Submission for Assignment 2 of Introduction to Robotics (BCCS-9402) course

Submitted by: Aniket Sharma (2019BCS-008)

Problem statement:
Write a program to transform frame A to frame B, then input position of a point in a frame and output position of the same point in another frame.

INPUT:

It takes 8 values from user which are as follows:
    1. (float) Angle in degrees by which to rotate frame A about x-axis
    2. (float) Angle in degreesby which to rotate frame A about y-axis
    3. (float) Angle in degreesby which to rotate frame A about z-axis
    4. (float) Distance in units by which to translate frame A about x-axis
    5. (float) Distance in units by which to translate frame A about y-axis
    6. (float) Distance in units by which to translate frame A about z-axis
    7. (character[A/B]) Frame in which the point is known to user
    8. (3 space-separated integers) Coordinates of the known point

OUTPUT:

    1. (numpy array) new coordinates

Example:
Program to transform frame A to frame B, then input position of a point in a frame and output position of the same point in another frame

Following transformations can be performed:
1. Rotation about x-axis
2. Rotation about y-axis
3. Rotation about z-axis
4. Translation about x-axis
5. Translation about y-axis
6. Translation about z-axis

Enter angle to rotate x-axis (in degrees): 0
Enter angle to rotate y-axis (in degrees): 0
Enter angle to rotate z-axis (in degrees): 30
Enter translation from x-axis: 10
Enter translation from y-axis: 5
Enter translation from z-axis: 0
Point is known in frame? (A/B): B

Enter position of the point in the frame: 3 7 0

Position of the point in other frame is: (9.098076211353316, 12.562177826491071, 0.0)
"""

import numpy as np
import math


def get_input():
    """
    Method to take input from user.

    INPUT:

    It takes 8 values from user which are as follows:
    1. (float) Angle in degrees by which to rotate frame A about x-axis
    2. (float) Angle in degreesby which to rotate frame A about y-axis
    3. (float) Angle in degreesby which to rotate frame A about z-axis
    4. (float) Distance in units by which to translate frame A about x-axis
    5. (float) Distance in units by which to translate frame A about y-axis
    6. (float) Distance in units by which to translate frame A about z-axis
    7. (character[A/B]) Frame in which the point is known to user
    8. (3 space-separated integers) Coordinates of the known point

    OUTPUT:

    1. (numpy array) Coordinates given by user
    2. (numpy array) transformation matrix for the given transformations
    """

    print('Program to transform frame A to frame B, then input position of a point in a frame and output position of the same point in another frame')
    print('\nFollowing transformations can be performed:')
    print('1. Rotation about x-axis')
    print('2. Rotation about y-axis')
    print('3. Rotation about z-axis')
    print('4. Translation about x-axis')
    print('5. Translation about y-axis')
    print('6. Translation about z-axis')

    # The angles are taken in degrees from user but are converted to radians for computation
    rotation_x = int(input('\nEnter angle to rotate x-axis (in degrees): '))
    rotation_x = math.pi/180*rotation_x
    rotation_y = int(input('Enter angle to rotate y-axis (in degrees): '))
    rotation_y = math.pi/180*rotation_y
    rotation_z = int(input('Enter angle to rotate z-axis (in degrees): '))
    rotation_z = math.pi/180*rotation_z

    translation_x = int(input('Enter translation from x-axis: '))
    translation_y = int(input('Enter translation from y-axis: '))
    translation_z = int(input('Enter translation from z-axis: '))

    frame_known = ''
    while frame_known != 'a' and frame_known != 'b':
        frame_known = input('Point is known in frame? (A/B): ').lower()
        if frame_known != 'a' and frame_known != 'b':
            print('Two frames are \'A\' or \'B\'')

    initial_coordinates = np.array(list(
        map(int, input('\nEnter position of the point in the frame: ').split())))

    # returns: coordinates given by user and transformation matrix for given transformations
    return initial_coordinates, calculate_transformation_matrix(rotation_x, rotation_y, rotation_z, translation_x, translation_y, translation_z, frame_known)


def calculate_transformation_matrix(rotation_x, rotation_y, rotation_z, translation_x, translation_y, translation_z, frame_known):
    """
    Method to calculate the transformation matrix.

    INPUT:

    1. (float) Angle in degrees by which to rotate frame A about x-axis
    2. (float) Angle in degreesby which to rotate frame A about y-axis
    3. (float) Angle in degreesby which to rotate frame A about z-axis
    4. (float) Distance in units by which to translate frame A about x-axis
    5. (float) Distance in units by which to translate frame A about y-axis
    6. (float) Distance in units by which to translate frame A about z-axis
    7. (character[A/B]) Frame in which the point is known to user

    OUTPUT:

    1. (numpy array) transformation matrix for the given transformations
    """

    # rotation matrix for rotation about x-axis
    rx = np.array([[1, 0, 0],
                   [0, math.cos(rotation_x), -math.sin(rotation_x)],
                   [0, math.sin(rotation_x), math.cos(rotation_x)]])

    # rotation matrix for rotation about y-axis
    ry = np.array([[math.cos(rotation_y), 0, math.sin(rotation_y)],
                   [0, 1, 0],
                   [-math.sin(rotation_y), 0, math.cos(rotation_y)]])

    # rotation matrix for rotation about z-axis
    rz = np.array([[math.cos(rotation_z), -math.sin(rotation_z), 0],
                   [math.sin(rotation_z), math.cos(rotation_z), 0],
                   [0, 0, 1]])

    # final rotation matrix is the matrix multiplication of all three rotation matrices
    r = rz @ ry @ rx

    # if point is known is frame 'A' we need inverse transformation matrix
    if frame_known == 'a':
        # displacement matrix representing displacement about 3 axes
        d = np.array([[translation_x], [translation_y], [translation_z]])
        temp = -r.T@d
        temp = np.vstack((temp, [1]))

        transformation_matrix = np.hstack(
            (np.vstack((r.T, np.array([0, 0, 0]))), temp))

        return transformation_matrix

    elif frame_known == 'b':
        # displacement matrix representing displacement about 3 axes
        d = np.array([[translation_x], [translation_y], [translation_z], [1]])

        transformation_matrix = np.hstack(
            (np.vstack((r, np.array([0, 0, 0]))), d))

        return transformation_matrix


def transform(initial_coordinates, transformation_matrix):
    """
    Method to calculate new coordinates.

    INPUT:

    1. (numpy array) Coordinates given by user
    2. (numpy array) transformation matrix for the given transformations

    OUTPUT:

    1. (numpy array) new coordinates
    """

    # 1 is appending to the coordinates for matrix multiplication
    initial_coordinates = np.hstack((initial_coordinates, 1))
    final_coordinates = transformation_matrix@initial_coordinates

    # removing '1' in the last dimension
    return final_coordinates[:3]


def print_final_answer(final_coordinates):
    """
    Method to print the answer.

    INPUT:

    1. (numpy array) new coordinates
    """

    print('\nPosition of the point in other frame is: ({}, {}, {})'.format(
          final_coordinates[0], final_coordinates[1], final_coordinates[2]))


if __name__ == '__main__':
    initial_coordinates, transformation_matrix = get_input()
    final_coordinates = transform(initial_coordinates, transformation_matrix)
    print_final_answer(final_coordinates)
