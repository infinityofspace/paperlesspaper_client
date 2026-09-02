from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    from paperlesspaper_client.client import Client


class Users:
    def __init__(self, client: "Client") -> None:
        """
        Initialize the Users API client.

        :param client: The main API client instance used for making requests.
        """

        self.client = client

    def get_user(self, user_id: str) -> dict:
        """
        Get a user by ID.

        :param user_id: The ID of the user to retrieve.
        :return: User data as a dictionary.
        """

        response = self.client.get(f"users/{user_id}")

        return response.json()

    def list_users(
        self,
        organization: str,
        name: str | None = None,
        role: Literal["user", "admin", "patient", "onlyself"] | None = None,
        sort_by: Literal["name", "email", "role"] | None = None,
        search: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
        page: int | None = None,
    ) -> list[dict]:
        """
        List all users.

        :param organization: The organization to filter users by.
        :param name: Optional name filter.
        :param role: Optional role filter.
        :param sort_by: Optional sorting field.
        :param search: Optional search term.
        :param limit: Optional limit for pagination.
        :param offset: Optional offset for pagination.
        :param page: Optional page number for pagination.
        :return: List of users as dictionaries.
        """

        response = self.client.get(
            "users",
            params={
                "organization": organization,
                "name": name,
                "role": role,
                "sort_by": sort_by,
                "search": search,
                "limit": limit,
                "offset": offset,
                "page": page,
            },
        )

        return response.json()

    def create_user(
        self,
        organization: str,
        email: str | None = None,
        timezone: str | None = None,
        role: Literal["user", "admin", "patient", "onlyself"] | None = None,
        meta: dict | None = None,
    ) -> dict:
        """
        Create a new user.

        :param organization: The organization the user belongs to.
        :param email: The email of the user.
        :param timezone: The timezone of the user.
        :param role: The role of the user.
        :param meta: Additional metadata for the user.
        :return: The created user data as a dictionary.
        """

        json = {
            "organization": organization,
        }
        if role:
            json["role"] = role
        if email:
            json["email"] = email
        if timezone:
            json["timezone"] = timezone
        if meta:
            json["meta"] = meta

        response = self.client.post("users", json=json)

        return response.json()

    def delete_user(self, user_id: str) -> dict:
        """
        Delete a user by ID.

        :param user_id: The ID of the user to delete.
        :return: Response data as a dictionary.
        """

        response = self.client.delete(f"users/{user_id}")

        return response.json()

    def update_user(
        self,
        user_id: str,
        name: str | None = None,
        timezone: str | None = None,
        avatar: str | None = None,
        apps: dict | None = None,
        email: str | None = None,
        role: Literal["user", "admin", "patient", "onlyself"] | None = None,
        inviteCode: str | None = None,
        organization: str | None = None,
        meta: dict | None = None,
    ) -> dict:
        """
        Update a user's information.

        :param user_id: The ID of the user to update.
        :param name: The new name of the user.
        :param timezone: The new timezone of the user.
        :param avatar: The new avatar URL of the user.
        :param apps: The new application-specific user fields.
        :param email: The new email of the user.
        :param role: The new role of the user.
        :param inviteCode: The new invite code of the user.
        :param organization: The new organization of the user.
        :param meta: Additional metadata for the user.
        :return: The updated user data as a dictionary.
        """

        json = {}
        if role:
            json["role"] = role
        if email:
            json["email"] = email
        if timezone:
            json["timezone"] = timezone
        if meta:
            json["meta"] = meta
        if name:
            json["name"] = name
        if avatar:
            json["avatar"] = avatar
        if apps:
            json["apps"] = apps
        if inviteCode:
            json["inviteCode"] = inviteCode
        if organization:
            json["organization"] = organization

        response = self.client.patch(f"users/{user_id}", json=json)

        return response.json()
