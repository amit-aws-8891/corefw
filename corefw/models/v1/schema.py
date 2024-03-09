import base64
from datetime import datetime

from cryptography.fernet import Fernet
from src.specs.constants.constants import (
    ACTIVE,
    API_KEY,
    ASSOCIATED_APPS,
    ASSOCIATED_GROUPS,
    CLIENT,
    CLIENT_CODE,
    CONFIG_DATA,
    CREDENTIALS,
    LAST_USED,
    NAME,
    PROVIDER_CODE,
    PROVIDER_NAME,
    STATUS,
    VALUE,
)
from src.specs.enums.status import Status


class ApiKeySchema(dict):
    __setattr__ = dict.__setitem__
    __getattr__ = dict.__getitem__

    def __init__(self, **kwargs):
        self.name = kwargs.get(NAME)
        self.api_key = kwargs.get(API_KEY)
        self.associated_groups = kwargs.get(ASSOCIATED_GROUPS)
        self.created_at = datetime.utcnow().timestamp()
        self.status = ACTIVE
        self.last_used = ""
        dict.__init__(self)


class VLSApiKeySchema(dict):
    __setattr__ = dict.__setitem__
    __getattr__ = dict.__getitem__

    def __init__(self, **kwargs):
        self.api_key = kwargs.get(API_KEY)
        self.client_code = kwargs.get(CLIENT_CODE)
        self.client = kwargs.get(CLIENT)
        self.created_at = int(datetime.utcnow().timestamp())
        self.status = Status.ACTIVE.value
        self.last_used = ""
        dict.__init__(self)


class ApiKeyUpdateSchema(dict):
    __setattr__ = dict.__setitem__
    __getattr__ = dict.__getitem__

    def __init__(self, **kwargs):
        if kwargs.get(NAME):
            self.name = kwargs.get(NAME)
        if kwargs.get(ASSOCIATED_GROUPS):
            self.associated_groups = kwargs.get(ASSOCIATED_GROUPS)
        if kwargs.get(STATUS):
            self.status = kwargs.get(STATUS)
        if kwargs.get(LAST_USED):
            self.last_used = str(datetime.utcnow())
        dict.__init__(self)


class APIGroupSchema(dict):
    __setattr__ = dict.__setitem__
    __getattr__ = dict.__getitem__

    def __init__(self, **kwargs):
        self.name = kwargs.get(NAME)
        self.associated_apps = kwargs.get(ASSOCIATED_APPS)
        self.created_at = int(datetime.utcnow().timestamp())
        self.status = Status.ACTIVE.value
        dict.__init__(self)


class IntegrationSchema(dict):
    __setattr__ = dict.__setitem__
    __getattr__ = dict.__getitem__

    def __init__(self, **kwargs):
        credentials = []
        f_key = Fernet.generate_key()
        fernet = Fernet(f_key)
        self.provider_code = kwargs.get(PROVIDER_CODE)
        self.provider_name = kwargs.get(PROVIDER_NAME)
        self.created_at = int(datetime.utcnow().timestamp())
        self.updated_at = int(datetime.utcnow().timestamp())
        self.status = Status.ACTIVE.value
        self.config_data = kwargs.get(CONFIG_DATA)
        for row in kwargs.get(CREDENTIALS):
            credentials.append(
                {NAME: row.get(NAME), VALUE: fernet.encrypt(row.get(VALUE).encode())}
            )
        self.credentials = credentials
        self.salt_key = base64.b64encode(f_key)
        dict.__init__(self)


class UpdateIntegrationSchema(dict):
    __setattr__ = dict.__setitem__
    __getattr__ = dict.__getitem__

    def __init__(self, **kwargs):

        if kwargs.get(STATUS):
            self.status = kwargs.get(STATUS)
        if kwargs.get(CONFIG_DATA):
            self.config_data = kwargs.get(CONFIG_DATA)
        if kwargs.get(CREDENTIALS):
            credentials = []
            f_key = Fernet.generate_key()
            fernet = Fernet(f_key)
            for row in kwargs.get(CREDENTIALS):
                credentials.append(
                    {
                        NAME: row.get(NAME),
                        VALUE: fernet.encrypt(row.get(VALUE).encode()),
                    }
                )
            self.credentials = credentials
            self.salt_key = base64.b64encode(f_key)
        self.updated_at = int(datetime.utcnow().timestamp())
        dict.__init__(self)


class CredentialSchema(dict):
    __setattr__ = dict.__setitem__
    __getattr__ = dict.__getitem__

    def __init__(self, fernet, **kwargs):
        credentials = []
        for row in kwargs.get(CREDENTIALS):
            credentials.append(
                {NAME: row.get(NAME), VALUE: fernet.encrypt(row.get(VALUE).encode())}
            )
        self.credentials = credentials
        dict.__init__(self)
