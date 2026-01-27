def test_post_like_and_unlike(client):
    # Register & login
    res = client.post("/register", json={"username": "likeuser", "email": "like@test.com", "password": "secret123"})
    login = client.post("/login", json={"username_or_email": "likeuser", "password": "secret123"})
    token = login.json()["access_token"]

    # Create post
    post_res = client.post("/post/", data={"text": "Like test"}, headers={"Authorization": f"Bearer {token}"})
    post_id = post_res.json()["id"]

    # Like
    like_res = client.post(f"/post/{post_id}/like", headers={"Authorization": f"Bearer {token}"})
    assert like_res.status_code == 200
    assert like_res.json()["success"] is True

    # Unlike (toggle again)
    unlike_res = client.post(f"/post/{post_id}/like", headers={"Authorization": f"Bearer {token}"})
    assert unlike_res.status_code == 200
    assert unlike_res.json()["success"] is True
