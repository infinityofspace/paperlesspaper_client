import tempfile
from pathlib import Path

import responses


@responses.activate
def test_list_devices(client, base_url):
    responses.add(responses.GET, f"{base_url}devices/", json=[{"id": "d1"}], status=200)
    assert client.devices.list_devices() == [{"id": "d1"}]


@responses.activate
def test_create_device(client, base_url):
    responses.add(responses.POST, f"{base_url}devices/", json={"id": "d1"}, status=200)
    assert client.devices.create_device("paper-display", "org-1") == {"id": "d1"}


@responses.activate
def test_get_device(client, base_url):
    responses.add(responses.GET, f"{base_url}devices/d1", json={"id": "d1"}, status=200)
    assert client.devices.get_device("d1") == {"id": "d1"}


@responses.activate
def test_update_device(client, base_url):
    responses.add(
        responses.PATCH,
        f"{base_url}devices/d1",
        json={"id": "d1", "kind": "paper-display"},
        status=200,
    )
    assert client.devices.update_device("d1", kind="paper-display") == {
        "id": "d1",
        "kind": "paper-display",
    }


@responses.activate
def test_delete_device(client, base_url):
    responses.add(
        responses.DELETE, f"{base_url}devices/d1", json={"deleted": True}, status=200
    )
    assert client.devices.delete_device("d1") == {"deleted": True}


@responses.activate
def test_get_device_events(client, base_url):
    responses.add(
        responses.GET, f"{base_url}devices/events/d1", json={"events": []}, status=200
    )
    assert client.devices.get_device_events("d1") == {"events": []}


@responses.activate
def test_get_device_image(client, base_url):
    responses.add(
        responses.GET,
        f"{base_url}devices/image/d1/u1",
        json={"image": "ok"},
        status=200,
    )
    assert client.devices.get_device_image("d1", "u1") == {"image": "ok"}


@responses.activate
def test_ping_device(client, base_url):
    responses.add(
        responses.GET, f"{base_url}devices/ping/d1", json={"ok": True}, status=200
    )
    assert client.devices.ping_device("d1") == {"ok": True}


@responses.activate
def test_reboot_device(client, base_url):
    responses.add(
        responses.POST, f"{base_url}devices/reboot/d1", json={"ok": True}, status=200
    )
    assert client.devices.reboot_device("d1") == {"ok": True}


@responses.activate
def test_register_device(client, base_url):
    responses.add(
        responses.POST,
        f"{base_url}devices/registerdevice/d1",
        json={"registered": True},
        status=200,
    )
    assert client.devices.register_device("d1", True, "org-1") == {"registered": True}


@responses.activate
def test_reset_device(client, base_url):
    responses.add(
        responses.POST, f"{base_url}devices/reset/d1", json={"reset": True}, status=200
    )
    assert client.devices.reset_device("d1") == {"reset": True}


@responses.activate
def test_update_single_image_from_website(client, base_url):
    responses.add(
        responses.POST,
        f"{base_url}devices/updateSingleImageFromWebsite/d1",
        json={"ok": True},
        status=200,
    )
    assert client.devices.update_single_image_from_website("d1") == {"ok": True}


@responses.activate
def test_update_single_image_meta(client, base_url):
    responses.add(
        responses.POST,
        f"{base_url}devices/updateSingleImageMeta/d1",
        json={"ok": True},
        status=200,
    )
    assert client.devices.update_single_image_meta("d1", {"title": "X"}) == {"ok": True}


@responses.activate
def test_upload_logs(client, base_url):
    responses.add(
        responses.GET,
        f"{base_url}devices/upload-logs/d1",
        json={"url": "logs"},
        status=200,
    )
    assert client.devices.upload_logs("d1") == {"url": "logs"}


@responses.activate
def test_upload_single_image(client, base_url):
    responses.add(
        responses.POST,
        f"{base_url}devices/uploadSingleImage/d1",
        json={"ok": True},
        status=200,
    )
    with tempfile.NamedTemporaryFile() as tmp:
        Path(tmp.name).write_bytes(b"img")
        assert client.devices.upload_single_image("d1", "uuid-1", tmp.name) == {
            "ok": True
        }
