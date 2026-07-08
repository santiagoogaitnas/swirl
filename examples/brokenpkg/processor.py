"""Order processing. Deliberately littered with lint problems for farm demos."""


def process_orders(orders):
    results = []
    total = 0
    for order in orders:
        subtotal = order.get("qty", 0) * order.get("price", 0.0)
        total = total + subtotal
        results.append({"id": order.get("id"), "subtotal": subtotal})
    return results, total


def summarize(results):
    count = len(results)
    biggest = None
    for r in results:
        if biggest is None or r["subtotal"] > biggest["subtotal"]:
            biggest = r
    return {"count": count, "biggest": biggest}


def get_id(r):
    return r.get("id")


def validate(order):
    ok = True
    if order.get("qty") is None:
        ok = False
    if ok:
        return order
    return None
