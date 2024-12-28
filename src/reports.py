import datetime
import typing
from functools import wraps
from pathlib import Path

import pandas as pd


def report_to_file(*, filename: str | typing.Any = "") -> typing.Any:
    def wrapper(any_func: typing.Callable) -> typing.Callable:
        @wraps(any_func)
        def inner(*args: typing.Any, **kwargs: typing.Any) -> typing.Any:
            result = any_func(*args, **kwargs)
            if filename:
                saving_place = filename
            else:
                date = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                saving_place = Path(
                    Path(__file__).parent.parent.joinpath("data", "reports", f"{date}_{any_func.__name__}_report.csv")
                )
                saving_place.parent.mkdir(exist_ok=True, parents=True)
            result.to_csv(saving_place, index=False, encoding="utf-8")

            return result

        return inner

    return wrapper


@report_to_file()
def spending_by_category(transactions: pd.DataFrame, category: str, date: str = "") -> pd.DataFrame:
    """фильтрует траты в объекте pd.DataFrame по категории и дате"""
    try:
        if date == "":
            date_obj = datetime.datetime.now()
        else:
            date_obj = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        start_date = (date_obj - datetime.timedelta(days=90)).strftime("%Y.%m.%d")
        end_date = date_obj.strftime("%Y.%m.%d")
        transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"], dayfirst=True)
        df_by_category = transactions.loc[
            (transactions["Статус"] == "OK")
            & (transactions["Дата операции"] >= start_date)
            & (transactions["Дата операции"] <= end_date)
            & (transactions["Категория"] == category)
        ]
        return df_by_category
    except ValueError as error:
        raise error
    except KeyError as error:
        raise error
    except TypeError as error:
        raise error
