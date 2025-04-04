from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model

User = get_user_model()


@database_sync_to_async
def get_user(user_id):
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return None  # Return None, not False


class QueryAuthMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        query_string = scope.get("query_string", b"").decode("utf-8")
        query_parameters = dict(param.split("=") for param in query_string.split("&"))
        user_id = query_parameters.get("user_id", None)

        if user_id:
            user = await get_user(user_id)
            if user:
                scope["user"] = user
            else:
                scope["user"] = None  # In case user does not exist
        else:
            scope["user"] = None  # No user_id in the query string, assign None

        return await self.app(scope, receive, send)
