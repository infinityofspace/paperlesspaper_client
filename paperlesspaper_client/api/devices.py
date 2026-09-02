from contextlib import ExitStack
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from paperlesspaper_client.client import Client


class Devices:
    def __init__(self, client: "Client") -> None:
        """
        Initialize the Devices API client.

        :param client: The main API client instance used for making requests.
        """

        self.client = client

    def list_devices(self, **params) -> list[dict]:
        """
        List devices visible to the authenticated user.

        :param params: Optional query parameters forwarded to the API.
        :return: List of devices as dictionaries.
        """

        response = self.client.get("devices/", params=params)

        return response.json()

    def create_device(
        self,
        kind: str,
        organization: str,
        patient: str | None = None,
        paper: str | None = None,
    ) -> dict:
        """
        Create a new device for the current organization.

        :param kind: Device kind, such as "paper-display".
        :param organization: The organization ID to associate with the device.
        :param patient: Optional patient ID.
        :param paper: Optional paper ID.
        :return: Created device data as a dictionary.
        """

        json = {
            "kind": kind,
            "organization": organization,
            "patient": patient,
            "paper": paper,
        }
        response = self.client.post(
            "devices/", json={k: v for k, v in json.items() if v is not None}
        )

        return response.json()

    def get_device(self, device_id: str) -> dict:
        """
        Get a device by ID.

        :param device_id: The ID of the device to retrieve.
        :return: Device data as a dictionary.
        """

        response = self.client.get(f"devices/{device_id}")
        return response.json()

    def update_device(self, device_id: str, **payload) -> dict:
        """
        Update a device by ID.

        :param device_id: The ID of the device to update.
        :param payload: Fields to update on the device.
        :return: Updated device data as a dictionary.
        """

        response = self.client.patch(
            f"devices/{device_id}",
            json={k: v for k, v in payload.items() if v is not None},
        )

        return response.json()

    def delete_device(self, device_id: str) -> dict:
        """
        Delete a device by ID.

        :param device_id: The ID of the device to delete.
        :return: Response data as a dictionary.
        """

        response = self.client.delete(f"devices/{device_id}")

        return response.json()

    def get_device_events(self, device_id: str) -> dict:
        """
        Get the event history for a device.

        :param device_id: The ID of the device.
        :return: Device events as a dictionary.
        """

        response = self.client.get(f"devices/events/{device_id}")

        return response.json()

    def get_device_image(self, device_id: str, uuid: str) -> dict:
        """
        Get a device image by device ID and image UUID.

        :param device_id: The ID of the device.
        :param uuid: The UUID of the image.
        :return: Image data as a dictionary.
        """

        response = self.client.get(f"devices/image/{device_id}/{uuid}")

        return response.json()

    def ping_device(self, device_id: str) -> dict:
        """
        Ping a device.

        :param device_id: The ID of the device to ping.
        :return: Ping response data as a dictionary.
        """

        response = self.client.get(f"devices/ping/{device_id}")

        return response.json()

    def reboot_device(self, device_id: str) -> dict:
        """
        Reboot a device remotely.

        :param device_id: The ID of the device to reboot.
        :return: Reboot response data as a dictionary.
        """

        response = self.client.post(f"devices/reboot/{device_id}")

        return response.json()

    def register_device(
        self,
        device_id: str,
        enable: bool,
        organization: str,
        patient: str | None = None,
        paper: str | None = None,
    ) -> dict:
        """
        Register an existing device with the authenticated organization.

        :param device_id: The ID of the device to register.
        :param enable: Whether the device should be enabled.
        :param organization: The organization ID to associate with the device.
        :param patient: Optional patient ID.
        :param paper: Optional paper ID.
        :return: Registration response data as a dictionary.
        """

        json = {
            "enable": enable,
            "organization": organization,
            "patient": patient,
            "paper": paper,
        }
        response = self.client.post(
            f"devices/registerdevice/{device_id}",
            json={k: v for k, v in json.items() if v is not None},
        )

        return response.json()

    def reset_device(self, device_id: str) -> dict:
        """
        Reset a device.

        :param device_id: The ID of the device to reset.
        :return: Reset response data as a dictionary.
        """

        response = self.client.post(f"devices/reset/{device_id}")

        return response.json()

    def update_single_image_from_website(self, device_id: str) -> dict:
        """
        Trigger a single-image update from the website for a device.

        :param device_id: The ID of the device.
        :return: Update response data as a dictionary.
        """

        response = self.client.post(f"devices/updateSingleImageFromWebsite/{device_id}")

        return response.json()

    def update_single_image_meta(
        self, device_id: str, payload: dict | None = None
    ) -> dict:
        """
        Update metadata for a device image.

        :param device_id: The ID of the device.
        :param payload: Metadata payload to send to the API.
        :return: Update response data as a dictionary.
        """

        response = self.client.post(
            f"devices/updateSingleImageMeta/{device_id}", json=payload or {}
        )

        return response.json()

    def upload_logs(self, device_id: str) -> dict:
        """
        Request upload logs for a device.

        :param device_id: The ID of the device.
        :return: Log upload response data as a dictionary.
        """

        response = self.client.get(f"devices/upload-logs/{device_id}")

        return response.json()

    def upload_single_image(
        self,
        device_id: str,
        uuid: str,
        image_path: str | None = None,
        image_path_2: str | None = None,
    ) -> dict:
        """
        Upload one or two images for a device.

        :param device_id: The ID of the device.
        :param uuid: The image UUID supplied by the API.
        :param image_path: Optional path to the first image file.
        :param image_path_2: Optional path to the second image file.
        :return: Upload response data as a dictionary.
        """

        with ExitStack() as stack:
            files = {}
            if image_path is not None:
                files["image"] = stack.enter_context(open(image_path, "rb"))
            if image_path_2 is not None:
                files["image2"] = stack.enter_context(open(image_path_2, "rb"))
            response = self.client.post(
                f"devices/uploadSingleImage/{device_id}",
                json={"uuid": uuid},
                files=files or None,
            )

            return response.json()
