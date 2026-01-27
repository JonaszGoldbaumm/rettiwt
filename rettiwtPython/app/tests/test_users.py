def test_user_registration_and_login(client):
    # Register
    res = client.post("/register", json={
        "username": "user1",
        "email": "user1@test.com",
        "password": "pass1234"
    })
    assert res.status_code == 200
    assert res.json()["username"] == "user1"

    # Duplicate username
    res2 = client.post("/register", json={
        "username": "user1",
        "email": "user2@test.com",
        "password": "pass1234"
    })
    assert res2.status_code == 400 or res2.status_code == 422

    # Login
    login = client.post("/login", json={
        "username_or_email": "user1",
        "password": "pass1234"
    })
    assert login.status_code == 200
    assert "access_token" in login.json()


def test_user_profile_update(client):
    client.post("/register", json={
        "username": "updateuser",
        "email": "update@test.com",
        "password": "pass1234"
    })
    login = client.post("/login", json={
        "username_or_email": "updateuser",
        "password": "pass1234"
    })
    token = login.json()["access_token"]


    res = client.patch("/profile/me/username", json={"new_username": "newname"}, headers={"Authorization": f"Bearer {token}"})
    res2 = client.patch("/profile/me/password", json={"old_password": "pass1234", "new_password": "newpass"}, headers={"Authorization": f"Bearer {token}"})
    res3 = client.patch("/profile/me/description", json={"description": "Hello world"}, headers={"Authorization": f"Bearer {token}"})

    assert res3.status_code == 200
    assert res3.json()["message"] == "Description updated"

