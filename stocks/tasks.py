from celery import Celery, shared_task
from celery.schedules import crontab
from stocks.utils import search_stock_price


app = Celery(
    main="tasks",
    broker="pyamqp://guest@localhost//",
    backend="db+sqlite:///celery.sqlite",
)

app.conf.beat_schedule = {
    "get-stock-price-every-minute": {
        "task": "tasks.get_stock_price",
        "schedule": crontab("*/30 * * * *"),
        "args": (
            "PETR4",
            "BBDC4",
            "ITUB4",
            "ITSA4",
            "MGLU3",
        ),
    },
}

app.conf.timezone = "America/Sao_Paulo"


@shared_task
def get_stock_price(*args: str) -> None:
    for stock_name in args:
        search_stock_price(stock_name)
        
    print(f"Your stock {stock_name} price was saved successfully")

# @shared_task
# def get_stock_price(stock_name: str) -> None:
#     search_stock_price(stock_name)
