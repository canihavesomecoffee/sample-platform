#!/usr/bin/python

import sys
from os import path

# Need to append server root path to ensure we can import the necessary files.
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

if len(sys.argv) != 5:
    print(f'Invalid number of arguments. Expected 5 arguments, got {len(sys.argv)}')
    exit()


def run():
    from database import create_session
    from mod_auth.models import Role, User

    db = create_session(sys.argv[1])
    # Check if there's at least one admin user
    admin = User.query.filter(User.role == Role.admin).first()
    if admin is not None:
        print(f"Admin already exists: {admin.name}")
        return

    user = User(sys.argv[2], Role.admin, sys.argv[3], User.generate_hash(sys.argv[4]))
    db.add(user)
    db.commit()
    print(f"Admin user created with name: {user.name}")


run()
