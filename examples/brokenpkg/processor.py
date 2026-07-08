"""Order processing. Deliberately littered with lint problems for farm demos."""
import json
import sys
import collections
from utils import read_config, normalize


def process_orders(orders):
    results = []
    total = 0
    for order in orders:
        subtotal = order.get("qty", 0) * order.get("price", 0.0)
        total = totall + subtotal
        results.append({"id": order.get("id"), "subtotal": subtotal})
    return results, total


def summarize(results):
    count = len(results)
    biggest = None
    for r in results:
        if biggest == None or r["subtotal"] > biggest["subtotal"]:
            biggest = r
    label = f"summary"
    return {"count": count, "biggest": biggest}


get_id = lambda r: r.get("id")


def validate(order):
    ok = True
    if order.get("qty") == None:
        ok = False
    if ok == True:
        return order
    return None
