import tempfile
from pathlib import Path

import responses


@responses.activate
def test_get_paper(client, base_url):
    responses.add(responses.GET, f"{base_url}papers/p1", json={"id": "p1"}, status=200)
    assert client.papers.get_paper("p1") == {"id": "p1"}


@responses.activate
def test_list_papers(client, base_url):
    responses.add(responses.GET, f"{base_url}papers", json=[{"id": "p1"}], status=200)
    assert client.papers.list_papers(organization="org-1") == [{"id": "p1"}]


@responses.activate
def test_create_paper(client, base_url):
    responses.add(responses.POST, f"{base_url}papers", json={"id": "p1"}, status=200)
    assert client.papers.create_paper("org-1", "d1", "image") == {"id": "p1"}


@responses.activate
def test_update_paper(client, base_url):
    responses.add(
        responses.PATCH,
        f"{base_url}papers/p1",
        json={"id": "p1", "kind": "image"},
        status=200,
    )
    assert client.papers.update_paper("org-1", "p1", "d1", "image") == {
        "id": "p1",
        "kind": "image",
    }


@responses.activate
def test_create_paper_image(client, base_url):
    responses.add(
        responses.POST, f"{base_url}papers/image/p1", json={"url": "signed"}, status=200
    )
    assert client.papers.create_paper_image("p1") == {"url": "signed"}


@responses.activate
def test_get_google_calendar_data(client, base_url):
    responses.add(
        responses.GET,
        f"{base_url}papers/p1/google-calendar",
        json={"events": []},
        status=200,
    )
    assert client.papers.get_google_calendar_data("p1") == {"events": []}


@responses.activate
def test_upload_single_paper_image(client, base_url):
    responses.add(
        responses.POST, f"{base_url}papers/image/p1", json={"ok": True}, status=200
    )
    with tempfile.NamedTemporaryFile() as tmp:
        Path(tmp.name).write_bytes(b"img")
        assert client.papers.upload_single_image("p1", tmp.name) == {"ok": True}
