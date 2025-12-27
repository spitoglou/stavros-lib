"""
Miscellaneous Operations
"""

from typing import Any

import requests
from requests.models import Response


def get_country_data(country: str) -> list[dict[str, Any]]:
    """Country Data

    Arguments:
        country {str} -- Country Name

    Returns:
        list -- Country Data
    """
    url = "https://restcountries.com/v2/name/" + country
    data: Response = requests.get(url)
    return data.json()  # type: ignore[no-any-return]


def sys_not(
    title: str = "Title",
    message: str = "Message",
    timeout: int = 7,
    toast: bool = True,
    app_icon: str = "",
) -> None:
    """Generate System Notifications (multi-platform)

    Keyword Arguments:
        title {str} -- Main Title (default: {'Title'})
        message {str} -- Message to be displayed (default: {'Message'})
        timeout {int} -- Timeout in seconds (default: {7})
        toast {bool} -- Appear as "toast" (default: {True})
        app_icon {str} -- Icon file(can be ignored completely) (default: {''})
    """

    from plyer import notification  # pyright: ignore[reportMissingTypeStubs]

    notification.notify(  # pyright: ignore[reportOptionalCall]
        title=title,
        message=message,
        timeout=timeout,
        toast=toast,
        app_icon=app_icon,
    )
