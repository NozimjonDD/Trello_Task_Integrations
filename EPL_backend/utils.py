from rest_framework.exceptions import ErrorDetail
from rest_framework.serializers import as_serializer_error
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    handlers = {
        "AuthenticationFailed": _handle_auth_failed_error,
        "InvalidToken": _handle_invalid_token_error,
        "ValidationError": _handle_validation_error,
    }
    response = exception_handler(exc, context)

    exception_class = exc.__class__.__name__
    if exception_class in handlers:
        return handlers[exception_class](exc, context)
    return response


def _handle_auth_failed_error(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        response.data = {
            "status_code": response.status_code,
            "errors": [
                {"error": "no_account_found",
                 "error_field": None,
                 "message": str(exc)}
            ]
        }
    return response


def _handle_invalid_token_error(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        response.data = {
            "status_code": response.status_code,
            "errors": [
                {"error": "token_not_valid",
                 "error_field": None,
                 "message": str(exc.detail["messages"][0]["message"])}
            ]
        }
    return response


def _handle_validation_error(exc, context):
    response = exception_handler(exc, context)
    errors = as_serializer_error(exc)

    if response is not None:
        response.data = {"status_code": response.status_code, "errors": []}
        make_pretty_error(response.data, errors)
    return response


def make_pretty_error(data, errors):
    for error in errors:
        if isinstance(errors[error], dict) and len(errors[error]) >= 1:
            for er in errors[error]:
                make_pretty_error(data, {er: errors[error][er]})
        elif isinstance(errors[error], list) and isinstance(errors[error][0], ErrorDetail) and len(errors[error]) == 1:
            data["errors"].append(
                {
                    "error": f"{error}_{errors[error][0].code}",
                    "error_field": f"{error}",
                    "message": errors[error][0]
                }
            )
        elif isinstance(errors[error][0], dict) and len(errors[error]) >= 1:
            for er in errors[error]:
                make_pretty_error(data, er)
        else:
            data["errors"].append(
                {
                    "error": f"{error}_{errors[error].code}",
                    "error_field": f"{error}",
                    "message": errors[error]
                }
            )
