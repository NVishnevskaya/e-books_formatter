MIN_LENGTH, MAX_LENGTH = 8, 40


def is_number(user_password):
    try:
        int(user_password)
    except (ValueError, TypeError):
        return False
    return True


def are_there_all_alphas(user_password):
    alphas_checker = map(lambda x: x.isalpha(), user_password)
    return all(alphas_checker)


def is_correct_password(user_password):
    if is_number(user_password):
        return False
    if are_there_all_alphas(user_password):
        return False
    return MIN_LENGTH <= len(user_password) <= MAX_LENGTH

def is_the_same_with_hash(user_password, hashed_password):
    return hash(user_password) == hashed_password


if __name__ == "__main__":
    pass
