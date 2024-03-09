def get_settings(current_app, setting_name):
    """
    This will return settings variable
    :param setting_name:
    :param current_app:
    :return:
    """
    cp = current_app.config
    db_prefix = cp["DB_PREFIX"]

    settings_value = {
        "APIKEY_COLLECTION": db_prefix + "api_keys",
        "INTEGRATION_COLLECTION": db_prefix + "integrations",
        "SANDBOX_INTEGRATION_COLLECTION": db_prefix + "sandbox_integrations",
        "CREDENTIALS_COLLECTION": db_prefix + "credentials",
        "USERS_COLLECTION": db_prefix + "users",
        "ENVIRONMENT": cp["ENVIRONMENT"],
        "LOG_DATABASE_NAME": cp["LOG_DATABASE_NAME"],
        "LOG_COLLECTION_NAME": db_prefix + "audit_logs",
        "GROUPS_COLLECTION": db_prefix + "groups",
        "SECRET_KEY": cp["SECRET_KEY"],
        "UPLOAD_COLLECTION": db_prefix + "upload",
        "KAFKA_SERVERS": cp["KAFKA_SERVERS"],
        "BASE_HOST": cp["BASE_HOST"],
    }
    return settings_value[setting_name]
