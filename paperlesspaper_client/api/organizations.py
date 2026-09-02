from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from paperlesspaper_client.client import Client


class Organizations:
    def __init__(self, client: "Client") -> None:
        """
        Initialize the Organizations API client.

        :param client: The main API client instance used for making requests.
        """

        self.client = client

    def list_organizations(self) -> list[dict]:
        """
        Get a list of organizations associated with the authenticated user.

        :return: List of organizations as dictionaries.
        """

        response = self.client.get("organizations")

        return response.json()

    def get_organization(self, organization_id: str) -> dict:
        """
        Get details of a specific organization by its ID.

        :param organization_id: The ID of the organization to retrieve.
        :return: Organization details as a dictionary.
        """

        response = self.client.get(f"organizations/{organization_id}")

        return response.json()

    def create_organization(self, kind: str) -> dict:
        """
        Create a new organization.

        :param kind: The kind of organization to create (e.g., "private").
        :return: Details of the created organization as a dictionary.
        """

        data = {"kind": kind}
        response = self.client.post("organizations", data=data)

        return response.json()

    def delete_organization(self, organization_id: str) -> dict:
        """
        Delete an organization by its ID.

        :param organization_id: The ID of the organization to delete.
        :return: The deleted organization details as a dictionary.
        """

        response = self.client.delete(f"organizations/{organization_id}")

        return response.json()

    def update_organization(
        self,
        organization_id: str,
        name: str | None = None,
        kind: str | None = None,
        meta: dict | None = None,
    ) -> dict:
        """
        Update an organization's details.

        :param organization_id: The ID of the organization to update.
        :param name: The new name of the organization.
        :param kind: The new kind of the organization.
        :param meta: The new metadata for the organization.
        :return: The updated organization details as a dictionary.
        """

        params = {}
        if name is not None:
            params["name"] = name
        if kind is not None:
            params["kind"] = kind
        if meta is not None:
            params["meta"] = meta

        response = self.client.patch(f"organizations/{organization_id}", data=params)

        return response.json()
