import responses


@responses.activate
def test_list_users(client, base_url):
    responses.add(responses.GET, f"{base_url}users", json=[{"id": "u1"}], status=200)
    assert client.users.list_users(organization="org-1") == [{"id": "u1"}]


@responses.activate
def test_create_user(client, base_url):
    responses.add(responses.POST, f"{base_url}users", json={"id": "u1"}, status=200)
    assert client.users.create_user(organization="org-1", email="a@b.com") == {
        "id": "u1"
    }


@responses.activate
def test_update_user(client, base_url):
    responses.add(
        responses.PATCH,
        f"{base_url}users/u1",
        json={"id": "u1", "name": "Alice"},
        status=200,
    )
    assert client.users.update_user("u1", name="Alice") == {"id": "u1", "name": "Alice"}


@responses.activate
def test_delete_user(client, base_url):
    responses.add(
        responses.DELETE, f"{base_url}users/u1", json={"deleted": True}, status=200
    )
    assert client.users.delete_user("u1") == {"deleted": True}
