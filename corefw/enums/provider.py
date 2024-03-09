from enum import Enum


class Providers(str, Enum):

    CAPRI, CAMS, LOS, TEAL, VLS_INTERNAL = (
        "CAPRI",
        "CAMS",
        "LOS",
        "TEAL",
        "VLS_INTERNAL",
    )

    @classmethod
    def values(cls) -> list:
        """
        Values of providers
        """
        values = list()

        values.append(Providers.VLS_INTERNAL.value)
        values.append(Providers.CAMS.value)
        values.append(Providers.LOS.value)
        values.append(Providers.TEAL.value)

        values.append(Providers.CAPRI.value)

        return values
