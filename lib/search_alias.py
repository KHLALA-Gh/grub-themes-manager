def check_alias_existence(file_path, alias_to_check):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    for line in lines:
        if f'alias {alias_to_check}=' in line and not line.strip().startswith("#"):
            return True

    return False