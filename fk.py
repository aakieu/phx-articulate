# Import packages first
import numpy as np
np.set_printoptions(suppress=True)

# Link Lengths
a1 = 8.5
a2 = 15
a3 = 15
a4 = 12
link_lengths = np.array([a1, a2, a3, a4])


def rot_x(theta_deg):
    """ 
    Returns rotation matrix 
    """
    
    theta_rad = np.radians(theta_deg)
    rotation_matrix = [[1, 0, 0],
                       [0, np.cos(theta_rad), -np.sin(theta_rad)],
                       [0, np.sin(theta_rad), np.cos(theta_rad)]]
    return np.matrix(rotation_matrix)


def rot_y(theta_deg):
    """ 
    Returns rotation matrix 
    """

    theta_rad = np.radians(theta_deg)
    rotation_matrix = [[np.cos(theta_rad), 0, np.sin(theta_rad)],
                       [0, 1, 0],
                       [-np.sin(theta_rad), 0, np.cos(theta_rad)]]
    return np.matrix(rotation_matrix)


def rot_z(theta_deg):
    """ 
    Returns rotation matrix 
    """

    theta_rad = np.radians(theta_deg)
    rotation_matrix = [[np.cos(theta_rad), -np.sin(theta_rad), 0],
                       [np.sin(theta_rad), np.cos(theta_rad), 0],
                       [0, 0, 1]]
    return np.matrix(rotation_matrix)


def transl(x, y, z):
    """ 
    Returns rotation matrix 
    """

    displace_vector = [[x],
                       [y],
                       [z]]
    return np.matrix(displace_vector)


def htm(rot_matrix, d_vector):
    """ 
    Returns htm matrix
    """
    htm_matrix = np.append(rot_matrix, d_vector, axis=1)
    htm_matrix = np.append(htm_matrix, [[0, 0, 0, 1]], axis=0)
    return htm_matrix


def htm3(theta):
    """
    Input: 1x3 angle array  
    Returns: 4x4 htm matrix
    """
    # h0_1
    r0_1 = np.dot(rot_x(90), rot_y(theta[0]))
    d0_1 = transl(0, 0, a1)
    h0_1 = htm(r0_1, d0_1)
    # h1_2
    r1_2 = rot_z(theta[1])
    x1_2 = a2*np.cos(np.radians(theta[1]))
    y1_2 = a2*np.sin(np.radians(theta[1]))
    z1_2 = 0
    d1_2 = transl(x1_2, y1_2, z1_2)
    h1_2 = htm(r1_2, d1_2)
    # h2_3
    r2_3 = rot_z(theta[2])
    x2_3 = a3*np.cos(np.radians(theta[2]))
    y2_3 = a3*np.sin(np.radians(theta[2]))
    z2_3 = 0
    d2_3 = transl(x2_3, y2_3, z2_3)
    h2_3 = htm(r2_3, d2_3)
    # h0_3
    h0_2 = np.dot(h0_1, h1_2)
    h0_3 = np.dot(h0_2, h2_3)
    return h0_3


def htm4(theta):
    """ 
    Input: 1x4 angle array  
    Returns: 4x4 htm matrix
    """
    h0_3 = htm3(theta)
    # h3_4
    r3_4 = rot_z(theta[3])
    x3_4 = a4 * np.cos(np.radians(theta[3]))
    y3_4 = a4 * np.sin(np.radians(theta[3]))
    z3_4 = 0
    d3_4 = transl(x3_4, y3_4, z3_4)
    h3_4 = htm(r3_4, d3_4)
    h0_4 = np.dot(h0_3, h3_4)
    return h0_4


def fk3(theta):
    """
    Input: 1x3 angle array  
    Returns: 1x3 position array 
    """
    h0_3 = htm3(theta)
    x0_3 = h0_3[0, 3]
    y0_3 = h0_3[1, 3]
    z0_3 = h0_3[2, 3]
    d0_3 = [x0_3, y0_3, z0_3]
    return d0_3


def fk4(theta):
    """
    Input: 1x4 angle array  
    Returns: 1x3 position array
    """
    h0_4 = htm4(theta)
    x0_4 = h0_4[0, 3]
    y0_4 = h0_4[1, 3]
    z0_4 = h0_4[2, 3]
    d0_4 = [x0_4, y0_4, z0_4]
    return d0_4