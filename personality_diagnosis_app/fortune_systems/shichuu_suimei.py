import datetime
import math
from typing import Dict, Any, Tuple

from .base import FortuneSystem
from utils.date_utils import get_ten_kan, get_juu_ni_shi

class ShichuuSuimei(FortuneSystem):
    """
    四柱推命による性格診断システム
    """
    
    def __init__(self):
        """
        初期化メソッド
        """
        super().__init__("shichuu_suimei_data.json")
        
        # 天干配列
        self.ten_kan = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
        
        # 地支配列
        self.juu_ni_shi = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
        
        # 十二運配列
        self.juu_ni_un = ["長生", "沐浴", "冠帯", "建禄", "帝旺", "衰", "病", "死", "墓", "絶", "胎", "養"]
        
        # 各天干に対応する十二運の地支順序（開始地支のインデックス）
        self.juu_ni_un_start_idx = {
            "甲": self.juu_ni_shi.index("亥"),  # 甲の長生は亥から始まる
            "乙": self.juu_ni_shi.index("午"),  # 乙の長生は午から始まる
            "丙": self.juu_ni_shi.index("寅"),  # 丙の長生は寅から始まる
            "丁": self.juu_ni_shi.index("酉"),  # 丁の長生は酉から始まる
            "戊": self.juu_ni_shi.index("寅"),  # 戊の長生は寅から始まる
            "己": self.juu_ni_shi.index("酉"),  # 己の長生は酉から始まる
            "庚": self.juu_ni_shi.index("巳"),  # 庚の長生は巳から始まる
            "辛": self.juu_ni_shi.index("子"),  # 辛の長生は子から始まる
            "壬": self.juu_ni_shi.index("申"),  # 壬の長生は申から始まる
            "癸": self.juu_ni_shi.index("卯")   # 癸の長生は卯から始まる
        }
        
        # 宿命星配列
        self.tsuhen_sei = ["比肩", "劫財", "食神", "傷官", "偏財", "正財", "偏官", "正官", "偏印", "印綬"]
        
        # 各地支に対応する蔵干（本気、中気、余気）
        self.hidden_kan = {
            "子": ["癸", "", ""],         # 子の本気は癸
            "丑": ["己", "癸", "辛"],     # 丑の本気は己、中気は癸、余気は辛
            "寅": ["甲", "丙", "戊"],     # 寅の本気は甲、中気は丙、余気は戊
            "卯": ["乙", "", ""],         # 卯の本気は乙
            "辰": ["戊", "乙", "癸"],     # 辰の本気は戊、中気は乙、余気は癸
            "巳": ["丙", "庚", "戊"],     # 巳の本気は丙、中気は庚、余気は戊
            "午": ["丁", "己", ""],       # 午の本気は丁、中気は己
            "未": ["己", "丁", "乙"],     # 未の本気は己、中気は丁、余気は乙
            "申": ["庚", "壬", "戊"],     # 申の本気は庚、中気は壬、余気は戊
            "酉": ["辛", "", ""],         # 酉の本気は辛
            "戌": ["戊", "辛", "丁"],     # 戌の本気は戊、中気は辛、余気は丁
            "亥": ["壬", "甲", ""]        # 亥の本気は壬、中気は甲
        }
    
    def diagnose(self, birth_date: datetime.date) -> Dict[str, Any]:
        """
        誕生日から四柱推命による性格診断を行う
        
        Args:
            birth_date: 生年月日
            
        Returns:
            診断結果をDict形式で返す
        """
        # 日柱天干を算出
        day_ten_kan = self._calculate_day_ten_kan(birth_date)
        
        # 日柱地支を算出
        day_juu_ni_shi = self._calculate_day_juu_ni_shi(birth_date)
        
        # 日柱十二運を算出
        juu_ni_un = self._calculate_juu_ni_un(day_ten_kan, day_juu_ni_shi)
        
        # 月柱地支を算出
        month_juu_ni_shi = self._get_month_juu_ni_shi(birth_date)
        
        # 月干の蔵干を算出
        zougan = self._get_hidden_kan(month_juu_ni_shi, birth_date.day)
        
        # 宿命星を算出
        tsuhen_sei = self._calculate_tsuhen_sei(day_ten_kan, zougan)
        
        # 五行の算出
        gogyo = self._calculate_gogyo(day_ten_kan)
        
        # 日主の五行の算出
        nishu_gogyo = self._calculate_nishu_gogyo(birth_date)
        
        # 基本的な性格特性を取得
        personality_traits = self.get_personality_traits(day_ten_kan + day_juu_ni_shi)
        
        # 強みと弱みを取得
        strengths_weaknesses = self.get_strengths_and_weaknesses(day_ten_kan + day_juu_ni_shi)
        
        # キャリアアドバイスを取得
        career_advice = self._get_career_advice(day_ten_kan + day_juu_ni_shi)
        
        # 結果を返す
        result = {
            "ten_kan": day_ten_kan,
            "juu_ni_shi": juu_ni_un,  # ユーザーリクエストに応じて十二運を返す
            "tsuhen_sei": tsuhen_sei,
            "gogyo": gogyo,
            "nishu_gogyo": nishu_gogyo,
            "personality_traits": personality_traits,
            "strengths": strengths_weaknesses["strengths"],
            "weaknesses": strengths_weaknesses["weaknesses"],
            "career_advice": career_advice
        }
        
        return result
    
    def _calculate_day_ten_kan(self, birth_date: datetime.date) -> str:
        """
        生年月日から日柱天干を算出する
        
        Args:
            birth_date: 生年月日
            
        Returns:
            日柱天干
        """
        # 基準日（1900年1月1日は「甲」）からの経過日数を計算
        base_date = datetime.date(1900, 1, 31)  # 1900年1月31日は「甲」
        julian_days = (birth_date - base_date).days
        
        # 10干のサイクルで割った余りから天干を決定
        index = (julian_days % 10)
        return self.ten_kan[index]
    
    def _calculate_day_juu_ni_shi(self, birth_date: datetime.date) -> str:
        """
        生年月日から日柱地支を算出する
        
        Args:
            birth_date: 生年月日
            
        Returns:
            日柱地支
        """
        # 基準日（1900年1月1日は「子」）からの経過日数を計算
        base_date = datetime.date(1900, 1, 31)  # 1900年1月31日は「子」
        julian_days = (birth_date - base_date).days
        
        # 12支のサイクルで割った余りから地支を決定
        index = (julian_days % 12)
        return self.juu_ni_shi[index]
    
    def _calculate_juu_ni_un(self, day_ten_kan: str, day_juu_ni_shi: str) -> str:
        """
        日柱天干と日柱地支から十二運を算出する
        
        Args:
            day_ten_kan: 日柱天干
            day_juu_ni_shi: 日柱地支
            
        Returns:
            十二運
        """
        # 日柱天干に対応する十二運の開始地支インデックスを取得
        start_idx = self.juu_ni_un_start_idx.get(day_ten_kan, 0)
        
        # 日柱地支のインデックスを取得
        shi_idx = self.juu_ni_shi.index(day_juu_ni_shi)
        
        # 適切な十二運のインデックスを計算（時計回りまたは反時計回りの順序に応じて）
        # 陽干（甲、丙、戊、庚、壬）は順方向、陰干（乙、丁、己、辛、癸）は逆方向
        if self.ten_kan.index(day_ten_kan) % 2 == 0:  # 陽干
            un_idx = (shi_idx - start_idx) % 12
        else:  # 陰干
            un_idx = (start_idx - shi_idx) % 12
        
        return self.juu_ni_un[un_idx]
    
    def _get_month_juu_ni_shi(self, birth_date: datetime.date) -> str:
        """
        生年月日から月柱地支を算出する
        
        Args:
            birth_date: 生年月日
            
        Returns:
            月柱地支
        """
        # 月と地支のマッピング（節入りを考慮しない簡易版）
        month_to_shi = {
            1: "丑", 2: "寅", 3: "卯", 4: "辰", 5: "巳", 6: "午",
            7: "未", 8: "申", 9: "酉", 10: "戌", 11: "亥", 12: "子"
        }
        
        return month_to_shi.get(birth_date.month, "")
    
    def _get_hidden_kan(self, juu_ni_shi: str, day: int) -> str:
        """
        地支と日から蔵干を取得する
        
        Args:
            juu_ni_shi: 地支
            day: 日
            
        Returns:
            蔵干
        """
        # 地支に対応する蔵干（本気、中気、余気）を取得
        hidden_kans = self.hidden_kan.get(juu_ni_shi, ["", "", ""])
        
        # 日にちに応じて適切な蔵干を選択
        if 1 <= day <= 7:
            return hidden_kans[2] if hidden_kans[2] else hidden_kans[0]  # 余気または本気
        elif 8 <= day <= 14:
            return hidden_kans[1] if hidden_kans[1] else hidden_kans[0]  # 中気または本気
        else:
            return hidden_kans[0]  # 本気
    
    def _calculate_tsuhen_sei(self, day_ten_kan: str, hidden_kan: str) -> str:
        """
        日柱天干と蔵干から宿命星（十神）を算出する
        
        Args:
            day_ten_kan: 日柱天干
            hidden_kan: 蔵干
            
        Returns:
            宿命星（十神）
        """
        if not hidden_kan:
            return "不明"
        
        # 日柱天干のインデックスを取得
        day_kan_idx = self.ten_kan.index(day_ten_kan)
        
        # 蔵干のインデックスを取得
        hidden_kan_idx = self.ten_kan.index(hidden_kan)
        
        # 十神のインデックスを計算
        tsuhen_idx = (hidden_kan_idx - day_kan_idx) % 10
        
        return self.tsuhen_sei[tsuhen_idx]
    
    def _calculate_gogyo(self, ten_kan: str) -> str:
        """
        天干から五行を算出する
        
        Args:
            ten_kan: 天干
            
        Returns:
            五行
        """
        gogyo_map = {
            "甲": "木",
            "乙": "木",
            "丙": "火",
            "丁": "火",
            "戊": "土",
            "己": "土",
            "庚": "金",
            "辛": "金",
            "壬": "水",
            "癸": "水"
        }
        
        return gogyo_map.get(ten_kan, "")
    
    def _calculate_nishu_gogyo(self, birth_date: datetime.date) -> str:
        """
        生年月日から日主の五行を算出する
        
        Args:
            birth_date: 生年月日
            
        Returns:
            日主の五行
        """
        # 日柱天干を取得
        day_ten_kan = self._calculate_day_ten_kan(birth_date)
        
        # 天干から五行を取得
        return self._calculate_gogyo(day_ten_kan)
    
    def _get_career_advice(self, key: str) -> str:
        """
        キーに基づいてキャリアアドバイスを取得する
        
        Args:
            key: キャリアアドバイスを取得するためのキー
            
        Returns:
            キャリアアドバイス
        """
        if "career_advice" in self.data and key in self.data["career_advice"]:
            return self.data["career_advice"][key]
        
        return "あなたの個性を活かせる職業を選ぶことが大切です。"


# シングルトンインスタンスを作成
_instance = None

def diagnose(birth_date: datetime.date) -> Dict[str, Any]:
    """
    四柱推命による診断を行うファサードメソッド
    
    Args:
        birth_date: 生年月日
        
    Returns:
        診断結果をDict形式で返す
    """
    global _instance
    
    if _instance is None:
        _instance = ShichuuSuimei()
    
    return _instance.diagnose(birth_date) 