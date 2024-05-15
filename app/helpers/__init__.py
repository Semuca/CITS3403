"""Contains a variety of helper functions"""

from .authenticate_token import (redirect_wrapper, get_user_by_auth_header,
                                 get_user_by_token, unauthenticated_endpoint_wrapper,
                                 authenticated_endpoint_wrapper)
from .dictionary_filtering import remove_none_from_dictionary
from .json_schema_validation import validate_request_schema, RequestSchemaDefinition
from .loot_drops import calculate_next_level_requirements, single_loot_drop
