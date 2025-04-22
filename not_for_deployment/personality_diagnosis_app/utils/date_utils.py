import datetime
import calendar
from typing import Tuple, Dict

def get_lunar_date(date: datetime.date) -> Dict:
    """
    西暦日付から旧暦（太陰暦）の日付を取得する
    注: 実際の変換には専用のライブラリが必要です
    """
    # このメソッドは実際には pylunar などのライブラリを使用する
    # ここではダミーの実装を返します
    return {
        "year": date.year,
        "month": date.month,
        "day": date.day,
        "leap_month": False
    }

def get_chinese_zodiac(year: int) -> str:
    """
    年から干支を取得する
    """
    zodiac = ["子（ねずみ）", "丑（うし）", "寅（とら）", "卯（うさぎ）", 
              "辰（たつ）", "巳（へび）", "午（うま）", "未（ひつじ）", 
              "申（さる）", "酉（とり）", "戌（いぬ）", "亥（いのしし）"]
    return zodiac[(year - 4) % 12]

def get_ten_kan(year: int) -> str:
    """
    年から十干を取得する
    """
    kan = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
    return kan[(year - 4) % 10]

def get_juu_ni_shi(year: int) -> str:
    """
    年から十二支を取得する
    """
    shi = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
    return shi[(year - 4) % 12]

def get_western_zodiac(month: int, day: int) -> str:
    """
    月と日から西洋占星術の星座を取得する
    """
    if (month == 3 and day >= 21) or (month == 4 and day <= 19):
        return "牡羊座"
    elif (month == 4 and day >= 20) or (month == 5 and day <= 20):
        return "牡牛座"
    elif (month == 5 and day >= 21) or (month == 6 and day <= 21):
        return "双子座"
    elif (month == 6 and day >= 22) or (month == 7 and day <= 22):
        return "蟹座"
    elif (month == 7 and day >= 23) or (month == 8 and day <= 22):
        return "獅子座"
    elif (month == 8 and day >= 23) or (month == 9 and day <= 22):
        return "乙女座"
    elif (month == 9 and day >= 23) or (month == 10 and day <= 23):
        return "天秤座"
    elif (month == 10 and day >= 24) or (month == 11 and day <= 22):
        return "蠍座"
    elif (month == 11 and day >= 23) or (month == 12 and day <= 21):
        return "射手座"
    elif (month == 12 and day >= 22) or (month == 1 and day <= 19):
        return "山羊座"
    elif (month == 1 and day >= 20) or (month == 2 and day <= 18):
        return "水瓶座"
    else:
        return "魚座"

def get_kyusei(date: datetime.date) -> str:
    """
    日付から九星を取得する
    """
    kyusei = ["一白水星", "二黒土星", "三碧木星", "四緑木星", "五黄土星", 
              "六白金星", "七赤金星", "八白土星", "九紫火星"]
    
    # 計算方法は概算です
    year_num = (date.year + 6) % 9
    return kyusei[year_num - 1 if year_num > 0 else 8]

def is_leap_year(year: int) -> bool:
    """
    閏年かどうかを判定する
    """
    return calendar.isleap(year) 