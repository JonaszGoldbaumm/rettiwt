def test_follow_unfollow(client):
    # Register two users
    res1 = client.post("/register", json={"username": "f1", "email": "f1@test.com", "password": "pass"})
    user1_id = res1.json()["id"]
    res2 = client.post("/register", json={"username": "f2", "email": "f2@test.com", "password": "pass"})
    user2_id = res2.json()["id"]

    # Login first user
    login1 = client.post("/login", json={"username_or_email": "f1", "password": "pass"})
    token1 = login1.json()["access_token"]

    # Follow user2
    follow_res = client.post(f"/profile/{user2_id}/follow", headers={"Authorization": f"Bearer {token1}"})
    assert follow_res.status_code == 200
    assert follow_res.json()["following"] is True

    # Check is_following
    check_res = client.get(f"/profile/{user2_id}/isfollow", headers={"Authorization": f"Bearer {token1}"})
    assert check_res.status_code == 200
    assert check_res.json()["following"] is True

    # Unfollow user2 (toggle)
    unfollow_res = client.post(f"/profile/{user2_id}/follow", headers={"Authorization": f"Bearer {token1}"})
    assert unfollow_res.status_code == 200
    assert unfollow_res.json()["following"] is False