import base64

def test_create_post(client):
    # Register user
    client.post("/register", json={
        "username": "testuser",
        "email": "test@test.com",
        "password": "secret123"
    })

    # Login
    login = client.post("/login", json={
        "username_or_email": "testuser",
        "password": "secret123"
    })
    token = login.json()["access_token"]

    # Create post
    res = client.post(
        "/post/",
        data={"text": "Hello test"},
        headers={"Authorization": f"Bearer {token}"}
    )

    assert res.status_code == 200
    assert res.json()["text"] == "Hello test"


def test_create_post_with_media(client):
    client.post("/register", json={
        "username": "mediauser",
        "email": "media@test.com",
        "password": "secret123"
    })
    login = client.post("/login", json={
        "username_or_email": "mediauser",
        "password": "secret123"
    })
    token = login.json()["access_token"]

    image_bytes = b"fake_image_data"
    res = client.post(
        "/post/",
        data={"text": "Post with media"},
        files={"media": ("image.png", image_bytes, "image/png")},
        headers={"Authorization": f"Bearer {token}"}
    )

    assert res.status_code == 200
    assert res.json()["text"] == "Post with media"


def test_post_like_and_unlike(client):
    client.post("/register", json={
        "username": "likeuser",
        "email": "like@test.com",
        "password": "secret123"
    })
    login = client.post("/login", json={
        "username_or_email": "likeuser",
        "password": "secret123"
    })
    token = login.json()["access_token"]

    post_res = client.post(
        "/post/",
        data={"text": "Like test"},
        headers={"Authorization": f"Bearer {token}"}
    )
    post_id = post_res.json()["id"]

    # Like post
    like_res = client.post(
        f"/post/{post_id}/like",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert like_res.status_code == 200

    # Unlike post
    unlike_res = client.post(
        f"/post/{post_id}/like",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert unlike_res.status_code == 200


def test_comment_crud(client):
    client.post("/register", json={
        "username": "commentuser",
        "email": "comment@test.com",
        "password": "secret123"
    })
    login = client.post("/login", json={
        "username_or_email": "commentuser",
        "password": "secret123"
    })
    token = login.json()["access_token"]

    post_res = client.post(
        "/post/",
        data={"text": "Comment test"},
        headers={"Authorization": f"Bearer {token}"}
    )
    post_id = post_res.json()["id"]

    comment_res = client.post(
        f"/post/{post_id}/comment",
        json={"text": "My comment"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert comment_res.status_code == 200

    # Delete comment
    del_res = client.delete(
        f"/post/comments/{1}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert del_res.status_code == 200


def test_delete_post(client):
    # Register & login
    client.post("/register", json={"username": "deleteuser", "email": "delete@test.com", "password": "secret123"})
    login = client.post("/login", json={"username_or_email": "deleteuser", "password": "secret123"})
    token = login.json()["access_token"]

    # Create post
    post_res = client.post("/post/", data={"text": "Delete me"}, headers={"Authorization": f"Bearer {token}"})
    post_id = post_res.json()["id"]

    get_res = client.get(f"/post/{post_id}", headers={"Authorization": f"Bearer {token}"})
    assert get_res.status_code == 200 

    # Delete post
    del_res = client.delete(f"/post/{post_id}", headers={"Authorization": f"Bearer {token}"})
    assert del_res.status_code == 200
    assert del_res.json()["success"] is True

    # Ensure post is gone
    get_res = client.get(f"/post/{post_id}", headers={"Authorization": f"Bearer {token}"})
    assert get_res.status_code == 404