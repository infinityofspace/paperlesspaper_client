from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from paperlesspaper_client.client import Client


class Accounts:
    def __init__(self, client: "Client") -> None:
        """
        Initialize the Accounts API client.

        :param client: The main API client instance used for making requests.
        """

        self.client = client

    def get_account(self, account_id: str):
        """
        Get account details by account ID.

        :param account_id: The ID of the account to retrieve.
        :return: Account details as a dictionary.
        """

        response = self.client.get(f"accounts/{account_id}")

        return response.json()

    def update_account(
        self,
        account_id: str,
        language: str | None = None,
        gender: str | None = None,
        email: str | None = None,
        given_name: str | None = None,
        family_name: str | None = None,
        debug: bool | None = None,
        demo: bool | None = None,
        notifications: bool | None = None,
    ):
        """
        Update account details by account ID.

        :param account_id: The ID of the account to update.
        :param language: The new language setting.
        :param gender: The new gender setting.
        :param email: The new email address.
        :param given_name: The new given name.
        :param family_name: The new family name.
        :param debug: The new debug setting.
        :param demo: The new demo setting.
        :param notifications: The new notifications setting.
        :return: Updated account details as a dictionary.
        """

        json = {}
        if language is not None:
            json["language"] = language
        if gender is not None:
            json["gender"] = gender
        if email is not None:
            json["email"] = email
        if given_name is not None:
            json["given_name"] = given_name
        if family_name is not None:
            json["family_name"] = family_name
        if debug is not None:
            json["debug"] = debug
        if demo is not None:
            json["demo"] = demo
        if notifications is not None:
            json["notifications"] = notifications

        response = self.client.put(f"accounts/{account_id}", json=json)

        return response.json()

    def get_current_account(self):
        """
        Get the current account details.

        :return: Current account details as a dictionary.
        """

        response = self.client.get("accounts/current")

        return response.json()

    def delete_current_account(self):
        """
        Delete the current account.

        :return: The deleted account details as a dictionary.
        """

        response = self.client.delete("accounts/current")

        return response.json()
