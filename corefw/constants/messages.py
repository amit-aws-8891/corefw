UNKNOWN_ERROR = ("E000001", "Unknown Error: {0}")
INVALID_PAYLOAD = ("E000002", "Invalid payload: {0}")
INVALID_EMAIL = ("E000003", "Invalid email address")
INVALID_URL = ("E000004", "Invalid Url")
INVALID_IP_ADDRESS = ("E000005", "Invalid Ip address")
FAILED_TO_GET_RESPONSE = ("E0000006", "Failed to get the response from url: {0}")
FORBIDDEN = ("E000007", "forbidden")
BAD_REQUEST = ("E000008", "Bad request")
BAD_GATEWAY = ("E0000009", "Bad Gateway")
REQUEST_TIMEOUT = ("E0000010", "Request timeout from url: {0}")
EMPTY_API_KEY = ("E0000011", "Please provide api key")
INVALID_API_KEY = ("E0000012", "Invalid api key")
FORBIDDEN_ACCESS = ("E0000013", "Forbidden access")
INVALID_EMAIL_ADDRESS = ("E0000014", "Invalid email address")
INVALID_TARGET_URL = ("E0000015", "Invalid target URL")
INVALID_TARGET_IP_ADDRESS = ("E0000016", "Invalid target IP address")
ONLY_JSON_SUPPORTED = ("E0000017", "Only JSON data is accepted")
FAILED_TO_UPDATE_API_KEY = ("E0000018", "Failed to update api key")
FAILED_TO_GET_APIKEY_DETAILS = ("E0000019", "Failed to get api key details")
FAILED_TO_GET_ASSOCIATED_APPS = ("E0000020", "Failed to update api key")
DUPLICATE_GROUP_NAME = ("E0000021", "Group already exists")
FAILED_TO_CREATE_GROUP = ("E0000022", "Failed to create group")
DUPLICATE_APIKEY_NAME = ("E0000023", "Api key name already exists")
FAILED_TO_CREATE_API_KEY = ("E0000024", "Failed to create API key")
INVALID_DATA_OBJECT = ("E0000025", "Data cannot be empty")
FAILED_TO_CREATE_INTEGRATION = ("E0000026", "Failed to create Integration")
INTEGRATION_NOT_FOUND = ("E0000027", "Integration not found")
PROVIDER_NOT_FOUND = ("E0000027", "provider not found")
JWT_TOKEN_EXPIRED = ("E0000028", "JWT token expired")
INVALID_JWT_TOKEN_EXPIRED = ("E0000029", "Invalid JWT token")
FAILED_TO_UPLOAD_DOCUMENTS = ("E0000030", "Failed to upload documents")
INVALID_VLS_CLIENT_CODE = ("E10001", "Invalid VLS API key")
FAILED_TO_CREATE_SERVICE_REQUEST = ("E0000031", "Failed to create service request")
FAILED_TO_CREATE_TASK_REQUEST = ("E0000032", "Failed to create service task request")
FAILED_TO_CREATE_ITEMID_REQUEST = (
    "E0000034",
    "Failed to create itemId service request",
)
FAILED_TO_CREATE_GET_REQUEST = ("E0000035", "Failed to create Get request")
FAILED_TO_PUSH_DATA = ("E000003", "Failed to push data to Kafka")

SUCCESS = "Success"

# success
API_KEY_CREATED = ("S000001", "API key created successfully.")
GROUP_CREATED = ("S000002", "Group created successfully.")
DATA_PUSH_SUCCESS = ("S000003", "Data pushed successfully.")
