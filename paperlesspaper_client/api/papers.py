from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from paperlesspaper_client.client import Client


class Papers:
    def __init__(self, client: "Client") -> None:
        """
        Initialize the Papers API client.

        :param client: The main API client instance used for making requests.
        """

        self.client = client

    def get_paper(
        self, paper_id: str, kind: str | None = None, _return: str | None = None
    ) -> dict:
        """
        Get a specific paper by its ID.

        :param paper_id: The ID of the paper to retrieve.
        :param kind: The kind of image to retrieve (e.g., "thumbnail", "full").
        :param _return: Optional return type for the response.
        :return: Paper details as a dictionary.
        """

        params = {}
        if kind is not None:
            params["kind"] = kind
        if _return is not None:
            params["_return"] = _return

        response = self.client.get(f"papers/{paper_id}", params=params)

        return response.json()

    def list_papers(
        self,
        name: str | None = None,
        role: str | None = None,
        sort_by: str | None = None,
        search: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
        page: int | None = None,
        device_id: str | None = None,
        organization: str | None = None,
    ) -> list[dict]:
        """
        List all papers with optional query parameters.

        :param params: Optional query parameters for filtering or pagination.
        :return: Response object containing the list of papers.
        """

        params = {}
        if name is not None:
            params["name"] = name
        if role is not None:
            params["role"] = role
        if sort_by is not None:
            params["sortBy"] = sort_by
        if search is not None:
            params["search"] = search
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        if page is not None:
            params["page"] = page
        if device_id is not None:
            params["deviceId"] = device_id
        if organization is not None:
            params["organization"] = organization

        response = self.client.get("papers", params=params)

        return response.json()

    def create_paper(
        self,
        organization: str,
        device_id: str,
        kind: str,
        device_paper_id: str | None = None,
        meta: dict | None = None,
    ) -> dict:
        """
        Creates a new screen (paper) to be displayed on the ePaper device.

        :param organization: The organization ID to which the paper belongs.
        :param device_id: The device ID associated with the paper.
        :param kind: The kind of paper to create (e.g., "plugin", "image", "plugin").
        :param device_paper_id: Optional device-specific paper ID.
        :param meta: Optional metadata for the paper.
        :return: Details of the created paper as a dictionary.
        """

        json = {"organization": organization, "deviceId": device_id, "kind": kind}
        if device_paper_id is not None:
            json["devicePaperId"] = device_paper_id
        if meta is not None:
            json["meta"] = meta

        response = self.client.post("papers", json=json)

        return response.json()

    def update_paper(
        self,
        organization: str,
        paper_id: str,
        device_id: str,
        kind: str,
        device_paper_id: str | None = None,
        meta: dict | None = None,
    ) -> dict:
        """
        Updates the content or settings of an existing paper (screen).

        :param organization: The organization ID to which the paper belongs.
        :param paper_id: The ID of the paper to update.
        :param device_id: The device ID associated with the paper.
        :param kind: The kind of paper to update (e.g., "plugin", "image", "weather").
        :param device_paper_id: Optional device-specific paper ID.
        :param meta: Optional metadata for the paper.
        :return: Details of the updated paper as a dictionary.
        """

        json = {"organization": organization, "deviceId": device_id, "kind": kind}
        if device_paper_id is not None:
            json["devicePaperId"] = device_paper_id
        if meta is not None:
            json["meta"] = meta

        response = self.client.patch(f"papers/{paper_id}", json=json)

        return response.json()

    def create_paper_image(
        self, paper_id: str, kind: str | None = None, _return: str | None = None
    ) -> dict:
        """
        Creates a temporary signed URL for getting an image from storage.

        :param paper_id: The ID of the paper.
        :param kind: The kind of image (e.g., "thumbnail", "full").
        :param _return: Optional return type for the response.
        :return: A temporary signed URL for the image.
        """

        json = {}
        if kind is not None:
            json["kind"] = kind
        if _return is not None:
            json["_return"] = _return

        response = self.client.post(f"papers/image/{paper_id}", json=json)

        return response.json()

    def get_google_calendar_data(
        self,
        paper_id: str,
        selected_calendars: dict | None = None,
        day_range: int | None = None,
        max_events: int | None = None,
        code: str | None = None,
        google_calendar: dict | None = None,
    ) -> dict:
        """
        Fetches the latest Google Calendar events for the specified paper without persisting any other paper changes.

        :param paper_id: The ID of the paper.
        :param selected_calendars: Optional dictionary of selected calendars.
        :param day_range: Optional range of days to fetch events for.
        :param max_events: Optional maximum number of events to fetch.
        :param code: Optional authorization code.
        :param google_calendar: Optional Google Calendar data.
        :return: Google Calendar data as a dictionary.
        """

        params = {}
        if selected_calendars is not None:
            params["selectedCalendars"] = selected_calendars
        if day_range is not None:
            if 1 <= day_range <= 100:
                params["dayRange"] = day_range
            else:
                raise ValueError("day_range must be between 1 and 100.")
        if max_events is not None:
            if 1 <= max_events <= 200:
                params["maxEvents"] = max_events
            else:
                raise ValueError("max_events must be between 1 and 200.")
        if code is not None:
            params["code"] = code
        if google_calendar is not None:
            params["googleCalendar"] = google_calendar

        response = self.client.get(f"papers/{paper_id}/google-calendar", params=params)

        return response.json()

    def upload_single_image(
        self, paper_id: str, image_path: str, kind: str | None = None
    ) -> dict:
        """
        Uploads a single image to the specified paper.

        :param paper_id: The ID of the paper.
        :param image_path: The local path to the image file to upload.
        :param kind: Optional kind of image (e.g., "thumbnail", "full").
        :return: Response data as a dictionary.
        """

        with open(image_path, "rb") as image_file:
            files = {"image": image_file}
            params = {}
            if kind is not None:
                params["kind"] = kind

            response = self.client.post(
                f"papers/image/{paper_id}", files=files, params=params
            )

            return response.json()
