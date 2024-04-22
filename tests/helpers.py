def get_api_headers():
    """Gets basic headers for testing api requests"""
    return {
        'Authorization': 'Bearer ' + "authtest",
        'Accept': '*/*',
        'Content-Type': 'application/json'
    }