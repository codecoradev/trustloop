def void_order(order_id, orders):
    """Mark an order as voided so it is not shipped."""
    orders[order_id]["status"] = "voided"
    return orders[order_id]


def abort_checkout(order_id, orders):
    """Stop a checkout that the customer abandoned."""
    orders[order_id]["status"] = "aborted"
    return orders[order_id]
