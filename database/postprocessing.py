import json
import pandas as pd
from numbers import Number
from decimal import Decimal
from datetime import date, datetime


def convert_for_json(obj):

    if isinstance(obj, Decimal):
        return float(obj)

    if isinstance(obj, (date, datetime)):
        return obj.isoformat()

    if isinstance(obj, list):
        return [convert_for_json(x) for x in obj]

    if isinstance(obj, tuple):
        return [convert_for_json(x) for x in obj]

    if isinstance(obj, dict):
        return {k: convert_for_json(v) for k, v in obj.items()}

    try:
        json.dumps(obj)
        return obj
    except TypeError:
        print("UNSUPPORTED TYPE:", type(obj), repr(obj))
        return str(obj)


def format_sql_result(results):
    """
    Returns:
      - numeric value if result is a single number
      - tabular string otherwise
    """

    results = convert_for_json(results)

    # Case 1: single numeric value
    if (
        isinstance(results, list)
        and len(results) == 1
    ):
        row = results[0]

        if isinstance(row, (list, tuple)) and len(row) == 1:
            if isinstance(row[0], Number):
                return row[0]

        if isinstance(row, dict) and len(row) == 1:
            value = next(iter(row.values()))
            if isinstance(value, Number):
                return value

    # Case 2: rows -> table string
    if isinstance(results, list) and len(results) > 0:

        if isinstance(results[0], dict):
            df = pd.DataFrame(results)

        elif isinstance(results[0], (list, tuple)):
            df = pd.DataFrame(results)

        else:
            return str(results)

        return df.to_string(index=False)

    return results




