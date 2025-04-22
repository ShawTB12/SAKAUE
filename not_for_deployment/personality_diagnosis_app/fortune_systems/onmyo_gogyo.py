import datetime
from typing import Dict, Any, List

from .base import FortuneSystem
from utils.date_utils import get_ten_kan

class OnmyoGogyo(FortuneSystem):
    """
    陰陽五行による性格診断システム
    """
    
    def __init__(self):
        """
        初期化メソッド
        """
        super().__init__("onmyo_gogyo_data.json")
    
    def diagnose(self, birth_date: datetime.date) -> Dict[str, Any]:
        """
        誕生日から陰陽五行による性格診断を行う
        
        Args:
            birth_date: 生年月日
            
        Returns:
            診断結果をDict形式で返す
        """
        # 天干から陰陽を取得
        ten_kan = get_ten_kan(birth_date.year)
        inyo = self._calculate_inyo(ten_kan)
        
        # 五行を算出
        gogyo = self._calculate_gogyo(birth_date)
        
        # 相性の良い五行と悪い五行を算出
        compatible_gogyo = self._calculate_compatible_gogyo(gogyo)
        incompatible_gogyo = self._calculate_incompatible_gogyo(gogyo)
        
        # 性格特性を取得
        personality_traits = self.get_personality_traits(gogyo)
        
        # 強みと弱みを取得
        strengths_weaknesses = self.get_strengths_and_weaknesses(gogyo)
        
        # 結果を返す
        result = {
            "inyo": inyo,
            "gogyo": gogyo,
            "compatible_gogyo": compatible_gogyo,
            "incompatible_gogyo": incompatible_gogyo,
            "personality_traits": personality_traits,
            "strengths": strengths_weaknesses["strengths"],
            "weaknesses": strengths_weaknesses["weaknesses"]
        }
        
        return result
    
    def _calculate_inyo(self, ten_kan: str) -> str:
        """
        天干から陰陽を算出する
        
        Args:
            ten_kan: 天干
            
        Returns:
            陰陽
        """
        inyo_map = {
            "甲": "陽",
            "乙": "陰",
            "丙": "陽",
            "丁": "陰",
            "戊": "陽",
            "己": "陰",
            "庚": "陽",
            "辛": "陰",
            "壬": "陽",
            "癸": "陰"
        }
        
        return inyo_map.get(ten_kan, "")
    
    def _calculate_gogyo(self, birth_date: datetime.date) -> str:
        """
        生年月日から五行を算出する
        
        Args:
            birth_date: 生年月日
            
        Returns:
            五行
        """
        # 生年月日から算出した値に基づいて五行を決定する
        # 実際には複雑な計算が必要ですが、ここでは簡略化して生まれた月から算出
        month_gogyo = {
            1: "水", 2: "水",
            3: "木", 4: "木",
            5: "火", 6: "火",
            7: "土", 8: "土",
            9: "金", 10: "金",
            11: "水", 12: "水"
        }
        
        # 日付による微調整（簡略化）
        day = birth_date.day
        if day % 5 == 1:
            return "木"
        elif day % 5 == 2:
            return "火"
        elif day % 5 == 3:
            return "土"
        elif day % 5 == 4:
            return "金"
        else:
            return month_gogyo.get(birth_date.month, "水")
    
    def _calculate_compatible_gogyo(self, gogyo: str) -> str:
        """
        五行から相性の良い五行を算出する
        
        Args:
            gogyo: 五行
            
        Returns:
            相性の良い五行
        """
        # 五行の相生関係: 木→火→土→金→水→木
        compatibility = {
            "木": "火",
            "火": "土",
            "土": "金",
            "金": "水",
            "水": "木"
        }
        
        return compatibility.get(gogyo, "")
    
    def _calculate_incompatible_gogyo(self, gogyo: str) -> str:
        """
        五行から相性の悪い五行を算出する
        
        Args:
            gogyo: 五行
            
        Returns:
            相性の悪い五行
        """
        # 五行の相剋関係: 木→土→水→火→金→木
        incompatibility = {
            "木": "土",
            "土": "水",
            "水": "火",
            "火": "金",
            "金": "木"
        }
        
        return incompatibility.get(gogyo, "")


# シングルトンインスタンスを作成
_instance = None

def diagnose(birth_date: datetime.date) -> Dict[str, Any]:
    """
    陰陽五行による診断を行うファサードメソッド
    
    Args:
        birth_date: 生年月日
        
    Returns:
        診断結果をDict形式で返す
    """
    global _instance
    
    if _instance is None:
        _instance = OnmyoGogyo()
    
    return _instance.diagnose(birth_date) 