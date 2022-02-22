from dataclasses import dataclass


@dataclass
class UserIdentity:
    email: str
    first_name: str
    last_name: str


def get_user_identity() -> UserIdentity:
    """
    This function should usually fetch User identity from DB.
    But as an example we return an inmemory object.
    """
    return UserIdentity(
        email='ex.ample@your-company.com',
        first_name='Ex',
        last_name='Ample',
    )
