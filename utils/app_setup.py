from database import (
	setup_admin,
	load_admin
)
from models.admin_model import Admin

def get_admin():
    row = load_admin()
    if row is None:
        return None
    else:
        return Admin(
            id=row["ID"],
            name=row["name"],
            password=row["password"],
        )
