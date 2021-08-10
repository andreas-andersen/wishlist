import numpy as np
from collections import Counter

def get_unassigned_users(array):
    return array[:, array[3] == 0]

def get_not_received_assignment_users(array):
    return array[:, array[4] == 0]

def get_most_common_responsible(array):
    return Counter(array[1]).most_common()[0][0]

def get_responsible_of_user(array, responsible_user):
    return array[:, array[1] == responsible_user]

def get_assignment_pool(array, responsible_user):
    temp_array = array[:, (array[1] != responsible_user) * (array[3] == 0)]
    largest_unassigned = Counter(temp_array[1]).most_common()[0][0]
    return temp_array[:, temp_array[1] == largest_unassigned]

def make_random_assignment(array):
    random_idx = np.random.choice(np.arange(array.shape[1]))
    return array[0, random_idx]

def get_excluded_unassigned_users(array, responsible_user):
    return array[:, (array[3] == 0) * (array[0] != responsible_user)]


def userwise_assignment(array):
    if array[3].any() == 1 or array[4].any() == 1:
        array[3:5, :] = 0
        array[2, :] = 0

    if get_most_common_responsible(array) > array.shape[1] / 2:
        return random_assignment(array)

    for i in range(array.shape[1]):
        unassigned_users = get_unassigned_users(array)
        not_received_assignment_users = get_not_received_assignment_users(array)

        if i == array.shape[1] - 2:
            if all(user in not_received_assignment_users[1] for user in unassigned_users[1]):
                largest_not_received_group = not_received_assignment_users[1][0]
            elif any(user in not_received_assignment_users[1] for user in unassigned_users[1]):
                not_received_assignment_user_index = [user in not_received_assignment_users[1] for
                    user in unassigned_users[1]]
                largest_not_received_group = unassigned_users[1, not_received_assignment_user_index]
            else:
                largest_not_received_group = get_most_common_responsible(not_received_assignment_users)
        else:
            largest_not_received_group = get_most_common_responsible(not_received_assignment_users)

        user_pool = get_responsible_of_user(not_received_assignment_users, largest_not_received_group)
        assignment_pool = get_assignment_pool(unassigned_users, largest_not_received_group)
        user = user_pool[0, 0]
        assignment = make_random_assignment(assignment_pool)

        array[4, array[0]==user] = 1
        array[3, array[0]==assignment] = 1
        array[2, array[0]==user] = assignment

    return array

def random_assignment(array):
    if array[3].any() == 1 or array[4].any() == 1:
        array[3:5, :] = 0
        array[2, :] = 0

    for i in range(array.shape[1]):

        user = array[0, i]
        assignment_pool = get_excluded_unassigned_users(array, user)

        if i == array.shape[1] - 2:
            if assignment_pool[3, assignment_pool.shape[1]-1] + assignment_pool[4, assignment_pool.shape[1]-1] == 0:
                assignment = assignment_pool[0, assignment_pool.shape[1]-1]
            else:
                assignment = make_random_assignment(assignment_pool)
        else:
            assignment = make_random_assignment(assignment_pool)


        array[4, array[0]==user] = 1
        array[3, array[0]==assignment] = 1
        array[2, array[0]==user] = assignment
    
    return array