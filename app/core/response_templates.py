def detail_with_msg(msg: str, field: str = "detail") -> dict:
    msg = str(msg)
    field = str(field)

    return {
        "content": {
            "application/json": {
                "example": {f"{field}": f"{msg}"},
            }
        }
    }
