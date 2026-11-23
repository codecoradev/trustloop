from db import query


def list_orders(limit=50, offset=0):
    rows = query("SELECT id, created_at, total FROM orders ORDER BY created_at DESC LIMIT ? OFFSET ?", (limit, offset))
    return {"orders": rows, "next_offset": offset + len(rows)}
