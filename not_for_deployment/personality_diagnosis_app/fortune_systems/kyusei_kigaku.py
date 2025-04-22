import datetime
from typing import Dict, Any, List

from .base import FortuneSystem
from utils.date_utils import get_kyusei

class KyuseiKigaku(FortuneSystem):
    """
    九星気学による性格診断システム
    """
    
    def __init__(self):
        """
        初期化メソッド
        """
        super().__init__("kyusei_kigaku_data.json")
    
    def diagnose(self, birth_date: datetime.date) -> Dict[str, Any]:
        """
        誕生日から九星気学による性格診断を行う
        
        Args:
            birth_date: 生年月日
            
        Returns:
            診断結果をDict形式で返す
        """
        # 本命星を算出
        honmei_sei = get_kyusei(birth_date)
        
        # 月命星を算出
        getsu_mei_sei = self._calculate_getsu_mei_sei(birth_date)
        
        # 五行を取得
        gogyo = self._get_gogyo(honmei_sei)
        
        # 性格特性を取得
        personality_traits = self.get_personality_traits(honmei_sei)
        
        # 相性を取得
        compatibility = self._get_compatibility(honmei_sei)
        
        # 年運を取得
        yearly_fortune = self._get_yearly_fortune(honmei_sei, datetime.datetime.now().year)
        
        # 結果を返す
        result = {
            "honmei_sei": honmei_sei,
            "getsu_mei_sei": getsu_mei_sei,
            "gogyo": gogyo,
            "personality_traits": personality_traits,
            "compatibility": compatibility,
            "yearly_fortune": yearly_fortune
        }
        
        return result
    
    def _calculate_getsu_mei_sei(self, birth_date: datetime.date) -> str:
        """
        生年月日から月命星を算出する
        
        Args:
            birth_date: 生年月日
            
        Returns:
            月命星
        """
        # 月命星の算出（簡易版）
        kyusei = ["一白水星", "二黒土星", "三碧木星", "四緑木星", "五黄土星", 
                  "六白金星", "七赤金星", "八白土星", "九紫火星"]
        
        # 単純に月から算出（実際にはもっと複雑）
        month_idx = (birth_date.month + 6) % 9
        return kyusei[month_idx if month_idx > 0 else 8]
    
    def _get_gogyo(self, honmei_sei: str) -> str:
        """
        本命星から五行を取得する
        
        Args:
            honmei_sei: 本命星
            
        Returns:
            五行
        """
        # 九星と五行のマッピング
        gogyo_map = {
            "一白水星": "水",
            "二黒土星": "土",
            "三碧木星": "木",
            "四緑木星": "木",
            "五黄土星": "土",
            "六白金星": "金",
            "七赤金星": "金",
            "八白土星": "土",
            "九紫火星": "火"
        }
        
        return gogyo_map.get(honmei_sei, "")
    
    def _get_compatibility(self, honmei_sei: str) -> Dict[str, List[str]]:
        """
        本命星から相性を取得する
        
        Args:
            honmei_sei: 本命星
            
        Returns:
            相性
        """
        # データファイルから相性情報を取得
        if "compatibility" in self.data and honmei_sei in self.data["compatibility"]:
            return self.data["compatibility"][honmei_sei]
        
        # データがない場合はデフォルト値
        # 九星の相性マップ（簡略化した例）
        default_compatibility = {
            "good": [],
            "bad": []
        }
        
        if honmei_sei == "一白水星":
            default_compatibility["good"] = ["六白金星", "八白土星"]
            default_compatibility["bad"] = ["四緑木星", "九紫火星"]
        elif honmei_sei == "二黒土星":
            default_compatibility["good"] = ["三碧木星", "四緑木星"]
            default_compatibility["bad"] = ["七赤金星", "六白金星"]
        elif honmei_sei == "三碧木星":
            default_compatibility["good"] = ["二黒土星", "五黄土星"]
            default_compatibility["bad"] = ["七赤金星", "一白水星"]
        elif honmei_sei == "四緑木星":
            default_compatibility["good"] = ["二黒土星", "五黄土星"]
            default_compatibility["bad"] = ["九紫火星", "一白水星"]
        elif honmei_sei == "五黄土星":
            default_compatibility["good"] = ["三碧木星", "四緑木星"]
            default_compatibility["bad"] = ["六白金星", "七赤金星"]
        elif honmei_sei == "六白金星":
            default_compatibility["good"] = ["一白水星", "九紫火星"]
            default_compatibility["bad"] = ["二黒土星", "五黄土星"]
        elif honmei_sei == "七赤金星":
            default_compatibility["good"] = ["八白土星", "九紫火星"]
            default_compatibility["bad"] = ["二黒土星", "三碧木星"]
        elif honmei_sei == "八白土星":
            default_compatibility["good"] = ["一白水星", "七赤金星"]
            default_compatibility["bad"] = ["二黒土星", "五黄土星"]
        elif honmei_sei == "九紫火星":
            default_compatibility["good"] = ["六白金星", "七赤金星"]
            default_compatibility["bad"] = ["一白水星", "四緑木星"]
        
        return default_compatibility
    
    def _get_yearly_fortune(self, honmei_sei: str, year: int) -> str:
        """
        本命星と年から年運を取得する
        
        Args:
            honmei_sei: 本命星
            year: 年
            
        Returns:
            年運
        """
        # データファイルから年運情報を取得
        if "yearly_fortune" in self.data and honmei_sei in self.data["yearly_fortune"]:
            fortunes = self.data["yearly_fortune"][honmei_sei]
            
            # 年を9で割った余りを使用して年運を取得
            index = (year % 9)
            if index == 0:
                index = 9
            
            if str(index) in fortunes:
                return fortunes[str(index)]
        
        # データがない場合はデフォルト値
        return "今年は新しい挑戦が吉となるでしょう。"


# シングルトンインスタンスを作成
_instance = None

def diagnose(birth_date: datetime.date) -> Dict[str, Any]:
    """
    九星気学による診断を行うファサードメソッド
    
    Args:
        birth_date: 生年月日
        
    Returns:
        診断結果をDict形式で返す
    """
    global _instance
    
    if _instance is None:
        _instance = KyuseiKigaku()
    
    return _instance.diagnose(birth_date) 