from enum import Enum


class Status(str, Enum):
    ACTIVE, INACTIVE = ("ACTIVE", "INACTIVE")

    @classmethod
    def values(cls) -> list:
        """
        Values of providers
        """
        values = list()
        values.append(Status.ACTIVE.value)
        values.append(Status.INACTIVE.value)
        return values
