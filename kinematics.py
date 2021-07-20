# Import packages first
import numpy as np
np.set_printoptions(suppress=True)

# Link Lengths
a1 = 8.5
a2 = 15
a3 = 15
a4 = 12
link_lengths = np.array([a1, a2, a3, a4])


def rot_x(theta):
    """ Returns rotation matrix about the x-axis for a given rotation of 'theta'.

    Parameters
    ----------
    theta : angle (in degrees) rotated about the corresponding axis

    Returns 
    -------
    rotation matrix : numpy.matrix size 3 x 3

    """
    theta_rad = np.radians(theta)
    rotation_matrix = [[1, 0, 0],
                       [0, np.cos(theta_rad), -np.sin(theta_rad)],
                       [0, np.sin(theta_rad), np.cos(theta_rad)]]
    return np.matrix(rotation_matrix)


def rot_y(theta):
    """ Returns rotation matrix about the y-axis for a given rotation of 'theta'.

    Parameters
    ----------
    theta : angle (in degrees) rotated about the corresponding axis

    Returns 
    -------
    rotation matrix : numpy.matrix size 3 x 3

    """
    theta_rad = np.radians(theta)
    rotation_matrix = [[np.cos(theta_rad), 0, np.sin(theta_rad)],
                       [0, 1, 0],
                       [-np.sin(theta_rad), 0, np.cos(theta_rad)]]
    return np.matrix(rotation_matrix)


def rot_z(theta):
    """ Returns rotation matrix about the z-axis for given rotation of 'theta'. 

    Parameters
    ----------
    theta : angle (in degrees) rotated about the corresponding axis

    Returns 
    -------
    rotation matrix : numpy.matrix size 3 x 3

    """
    theta_rad = np.radians(theta)
    rotation_matrix = [[np.cos(theta_rad), -np.sin(theta_rad), 0],
                       [np.sin(theta_rad), np.cos(theta_rad), 0],
                       [0, 0, 1]]
    return np.matrix(rotation_matrix)


def transl(x, y, z):
    """ Returns displacement vector for given translation 'x', 'y', 'z'.  

    Parameters
    ----------
    x, y, z : translation values in the x,y,z axis

    Returns 
    -------
    displacement vector : numpy.matrix size 3 x 1

    """
    displace_vector = [[x],
                       [y],
                       [z]]
    return np.matrix(displace_vector)


def htm(rotation_matrix, displacement_vector):
    """ Creates homogeneous transformation matrix (HTM) for given 'rotation_matrix' and 'displacement_vector'. 

    Parameters
    ----------
    rotation_matrix : numpy.matrix of size 3x3 
    displacement_vector : numpy.matrix of size 3x1 

    Returns 
    -------
    HTM : numpy.matrix size 4 x 4

    """
    htm_matrix = np.append(rotation_matrix, displacement_vector, axis=1)
    htm_matrix = np.append(htm_matrix, [[0, 0, 0, 1]], axis=0)
    return htm_matrix


def htm0_3(joint_rotations):
    """ Returns homogeneous transformation matrix (HTM) for given 'joint_rotations' from Base, Shoulder, and Elbow Joint respectively.

    Parameters
    ----------
    joint_rotations : numpy.matrix of size 1x3

    Returns 
    -------
    HTM : numpy.matrix size 4 x 4

    """
    # H0_1
    r0_1 = np.dot(rot_x(90), rot_y(joint_rotations[0]))
    d0_1 = transl(0, 0, a1)
    h0_1 = htm(r0_1, d0_1)

    # H1_2
    r1_2 = rot_z(joint_rotations[1])
    x1_2 = a2*np.cos(np.radians(joint_rotations[1]))
    y1_2 = a2*np.sin(np.radians(joint_rotations[1]))
    z1_2 = 0
    d1_2 = transl(x1_2, y1_2, z1_2)
    h1_2 = htm(r1_2, d1_2)

    # H2_3
    r2_3 = rot_z(joint_rotations[2])
    x2_3 = a3*np.cos(np.radians(joint_rotations[2]))
    y2_3 = a3*np.sin(np.radians(joint_rotations[2]))
    z2_3 = 0
    d2_3 = transl(x2_3, y2_3, z2_3)
    h2_3 = htm(r2_3, d2_3)

    # H0_3
    h0_2 = np.dot(h0_1, h1_2)
    h0_3 = np.dot(h0_2, h2_3)
    return h0_3


def htm4(joint_rotations):
    """ Returns homogeneous transformation matrix (HTM) for given 'joint_rotations' 
    from Base, Shoulder, Elbow, and wristPitch Joint respectively.

    Parameters
    ----------
    joint_rotations : numpy.matrix of size 1x4

    Returns 
    -------
    HTM : numpy.matrix size 4 x 4

    """
    # H0_3
    h0_3 = htm0_3(joint_rotations)

    # H3_4
    r3_4 = rot_z(joint_rotations[3])
    x3_4 = a4 * np.cos(np.radians(joint_rotations[3]))
    y3_4 = a4 * np.sin(np.radians(joint_rotations[3]))
    z3_4 = 0
    d3_4 = transl(x3_4, y3_4, z3_4)
    h3_4 = htm(r3_4, d3_4)
    h0_4 = np.dot(h0_3, h3_4)
    return h0_4


def fk3(joint_rotations):
    """ Returns x,y,z position of end effector given 'joint_rotations'
    from Base, Shoulder, and Elbow Joint respectively.

    Parameters
    ----------
    joint_rotations : list of len 3

    Returns 
    -------
    x,y,z position : list of len 3

    """
    h0_3 = htm0_3(joint_rotations)
    x0_3 = h0_3[0, 3]
    y0_3 = h0_3[1, 3]
    z0_3 = h0_3[2, 3]
    d0_3 = [x0_3, y0_3, z0_3]
    return d0_3


def fk4(joint_rotations):
    """ Returns x,y,z position of end effector given 'joint_rotations'
    from Base, Shoulder,Elbow, and wristPitch Joint respectively.

    Parameters
    ----------
    joint_rotations : list of len 4

    Returns 
    -------
    x,y,z position : list of len 3

    """
    h0_4 = htm4(joint_rotations)
    x0_4 = h0_4[0, 3]
    y0_4 = h0_4[1, 3]
    z0_4 = h0_4[2, 3]
    d0_4 = [x0_4, y0_4, z0_4]
    return d0_4


# Inverse Kinematics #
def ik3(xyz_array):
    """ Returns array of joint_rotations required for end effector 
    to be at position 'xyz_array'.

    Parameters
    ----------
    xyz_array : list of len 3

    Returns 
    -------
    joint_rotations : numpy.ndarray of len 3

    """
    # Eqn 1
    theta_1 = np.arctan2(xyz_array[1], xyz_array[0])
    # Eqn 2
    r1 = np.hypot(xyz_array[0], xyz_array[1])
    # Eqn 3
    r2 = xyz_array[2] - link_lengths[0]
    # Eqn 4
    phi2 = np.arctan2(r2, r1)
    # Eqn 5
    r3 = np.hypot(r1, r2)
    # Eqn 6
    num6 = np.power(link_lengths[2], 2) - \
        np.power(link_lengths[1], 2) - np.power(r3, 2)
    den6 = -2 * link_lengths[1] * r3
    phi1 = np.arccos(num6 / den6)
    # Eqn 7
    # theta_2 = phi2 - phi1  # elbow down
    theta_2 = phi2 + phi1
    # Eqn 8
    num8 = np.power(r3, 2) - \
        np.power(link_lengths[1], 2) - np.power(link_lengths[2], 2)
    den8 = -2 * link_lengths[1] * link_lengths[2]
    phi3 = np.arccos(num8 / den8)
    # Eqn 9
    # theta_3 = pi - phi3 # elbow down
    theta_3 = -(np.pi - phi3)
    # Output Joint Angles
    theta_1 = np.rad2deg(theta_1)
    theta_2 = np.rad2deg(theta_2)
    theta_3 = np.rad2deg(theta_3)
    joint_rotations = np.array([theta_1, theta_2, theta_3])
    return joint_rotations


def calculate_theta_4(joint_rotations, theta0_4):
    """ Returns angle required for wristPitch Joint to have respective angle 'theta0_4'
    given 'joint_rotations' made by first 3 joints.

    Parameters
    ----------
    joint_rotations : list of len 3

    Returns 
    -------
    theta_4 : float

    """
    # R0_3
    theta_1 = joint_rotations[0]
    theta_2 = joint_rotations[1]
    theta_3 = joint_rotations[2]
    # R0_4
    R0_4a = np.dot(rot_z(theta_1), rot_x(90))
    R0_4 = np.dot(R0_4a, rot_z(theta0_4))
    R0_1 = np.dot(rot_x(90), rot_y(theta_1))
    R1_2 = rot_z(theta_2)
    R2_3 = rot_z(theta_3)
    R0_2 = np.dot(R0_1, R1_2)
    R0_3 = np.dot(R0_2, R2_3)
    # R3_4
    R3_4 = np.dot(np.transpose(R0_3), R0_4)
    # theta_4
    theta_4 = np.degrees(np.arcsin(R3_4[1, 0]))
    return theta_4
