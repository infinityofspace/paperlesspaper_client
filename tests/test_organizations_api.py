import responses


@responses.activate
def test_list_organizations(client, base_url):
    responses.add(
        responses.GET, f"{base_url}organizations", json=[{"id": "org-1"}], status=200
    )
    assert client.organizations.list_organizations() == [{"id": "org-1"}]


@responses.activate
def test_create_organization(client, base_url):
    responses.add(
        responses.POST, f"{base_url}organizations", json={"id": "org-1"}, status=200
    )
    assert client.organizations.create_organization("private") == {"id": "org-1"}


@responses.activate
def test_update_organization(client, base_url):
    responses.add(
        responses.PATCH,
        f"{base_url}organizations/org-1",
        json={"id": "org-1", "name": "Org"},
        status=200,
    )
    assert client.organizations.update_organization("org-1", name="Org") == {
        "id": "org-1",
        "name": "Org",
    }


@responses.activate
def test_delete_organization(client, base_url):
    responses.add(
        responses.DELETE,
        f"{base_url}organizations/org-1",
        json={"deleted": True},
        status=200,
    )
    assert client.organizations.delete_organization("org-1") == {"deleted": True}
