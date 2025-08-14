from fastapi import Request


def set_user_context(request: Request, user_id: str | None, org_id: str | None) -> None:
    request.state.user_id = user_id
    request.state.org_id = org_id
