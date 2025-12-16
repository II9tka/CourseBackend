class UserIsExist(Exception):
    def __init__(self, field: str, value: str):
        super().__init__(f'User with {field} "{value}" already exists.')
