def test_provider():
    return {
        "username": "serviceprovider",
        "email": "provider@example.com",
        "password": "providerpass",
        "role": "service provider"
    }

def test_user():
    return {
        "username": "accountuser",
        "email": "accountuser@example.com",
        "password": "accountpass",
        "role": "account user"
    }

def test_admin():
    return {
        "username": "adminuser",
        "email": "admin@example.com",
        "password": "adminpass",
        "role": "admin"
    }

def test_guest():
    return {
        "username": "guestuser",
        "email": "guest@example.com",
        "password": "guestpass",
        "role": "guest"
    }
