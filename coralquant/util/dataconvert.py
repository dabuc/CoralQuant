import decimal
from datetime import datetime

def get_decimal_from_str(str):
    """
    字符串转Decimal
    """
    r = 0 if str == "" else decimal.Decimal(str)
    return r


def get_int_from_str(str):
    """
    字符串转int
    """
    r = 0 if str == "" else int(str)
    return r


def get_float_from_str(str):
    """
    字符串转float
    """
    r = 0 if str == "" else float(str)
    return r


def convert_to_date(date: str,format: str):
    """
    把字符串转化成日期，如果date为空，则返回空
    """
    result=None

    if date:
        result=datetime.strptime(date, format).date()
 
    return result