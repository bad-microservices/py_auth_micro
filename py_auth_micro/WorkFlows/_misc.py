from jwt_helper import JWTValidator

from ..Config import AppConfig


def _get_info_from_token(
    jwt_validator: JWTValidator, app_cfg: AppConfig, access_token: str
) -> tuple[str, bool]:
    """This Function gets Information from an Access-Token.

    It will Return a Tuple with the username and if he is an administrator.

    Args:
        jwt_validator (JWTValidator): JWTValidator used to verify the Access Token.
        app_cfg (AppConfig): AppConfig containing the Admin Group name.
        access_token (str): The Access Token to validate.
    Raises:
        ValueError: The Token could not be verified.

    Returns:
        tuple[str, bool]: username, is_admin
    """

    jwt_content = jwt_validator.get_jwt_as_dict(access_token)

    header: dict = jwt_content["headers"]
    user = jwt_content["payload"]["user"]

    is_admin = app_cfg.admin_group in header.get("aud", None)

    return user, is_admin
