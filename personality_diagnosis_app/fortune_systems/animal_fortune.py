import datetime
from typing import Dict, Any, List

from .base import FortuneSystem
from utils.date_utils import get_chinese_zodiac

class AnimalFortune(FortuneSystem):
    """
    動物占いによる性格診断システム
    """
    
    def __init__(self):
        """
        初期化メソッド
        """
        super().__init__("animal_fortune_data.json")
    
    def diagnose(self, birth_date: datetime.date) -> Dict[str, Any]:
        """
        誕生日から動物占いによる性格診断を行う
        
        Args:
            birth_date: 生年月日
            
        Returns:
            診断結果をDict形式で返す
        """
        # 動物を算出
        animal = self._calculate_animal(birth_date)
        
        # タイプを算出
        animal_type = self._calculate_type(birth_date)
        
        # 完全な動物タイプの組み合わせ
        full_animal_type = f"{animal}（{animal_type}タイプ）"
        
        # 性格特性を取得
        personality_traits = self.get_personality_traits(full_animal_type)
        
        # 相性を取得
        compatibility = self._get_compatibility(animal)
        
        # 適職を取得
        career = self._get_career(full_animal_type)
        
        # 結果を返す
        result = {
            "animal": animal,
            "type": animal_type,
            "full_type": full_animal_type,
            "personality_traits": personality_traits,
            "compatibility": compatibility,
            "career": career
        }
        
        return result
    
    def _calculate_animal(self, birth_date: datetime.date) -> str:
        """
        生年月日から動物を算出する
        
        Args:
            birth_date: 生年月日
            
        Returns:
            動物
        """
        # 干支を取得
        chinese_zodiac = get_chinese_zodiac(birth_date.year)
        
        # 干支から動物部分のみを抽出
        animal = chinese_zodiac.split("（")[1].replace("）", "")
        
        return animal
    
    def _calculate_type(self, birth_date: datetime.date) -> str:
        """
        生年月日からタイプを算出する
        
        Args:
            birth_date: 生年月日
            
        Returns:
            タイプ
        """
        # 日付から60干支の通し番号を計算
        # 実際には複雑な計算が必要ですが、ここでは簡略化
        day_of_year = (birth_date.month - 1) * 30 + birth_date.day
        
        # 動物占いの4タイプに分類
        if day_of_year % 4 == 0:
            return "チャーミング"
        elif day_of_year % 4 == 1:
            return "ワイルド"
        elif day_of_year % 4 == 2:
            return "ピュア"
        else:
            return "クール"
    
    def _get_compatibility(self, animal: str) -> Dict[str, List[str]]:
        """
        動物から相性を取得する
        
        Args:
            animal: 動物
            
        Returns:
            相性
        """
        # データファイルから相性情報を取得
        if "compatibility" in self.data and animal in self.data["compatibility"]:
            return self.data["compatibility"][animal]
        
        # データがない場合はデフォルト値
        default_compatibility = {
            "good": [],
            "bad": []
        }
        
        # 動物の基本的な相性（簡略化した例）
        if animal == "ねずみ":
            default_compatibility["good"] = ["うし", "りゅう", "さる"]
            default_compatibility["bad"] = ["うま", "うさぎ", "とり"]
        elif animal == "うし":
            default_compatibility["good"] = ["ねずみ", "へび", "とり"]
            default_compatibility["bad"] = ["ひつじ", "うま", "いぬ"]
        elif animal == "とら":
            default_compatibility["good"] = ["うま", "いぬ", "ぶた"]
            default_compatibility["bad"] = ["さる", "へび", "とり"]
        elif animal == "うさぎ":
            default_compatibility["good"] = ["ひつじ", "いぬ", "ぶた"]
            default_compatibility["bad"] = ["ねずみ", "とり", "うま"]
        elif animal == "りゅう":
            default_compatibility["good"] = ["ねずみ", "さる", "とり"]
            default_compatibility["bad"] = ["いぬ", "うし", "りゅう"]
        elif animal == "へび":
            default_compatibility["good"] = ["うし", "とり", "さる"]
            default_compatibility["bad"] = ["とら", "いのしし", "いぬ"]
        elif animal == "うま":
            default_compatibility["good"] = ["とら", "ひつじ", "いぬ"]
            default_compatibility["bad"] = ["ねずみ", "うし", "うさぎ"]
        elif animal == "ひつじ":
            default_compatibility["good"] = ["うさぎ", "うま", "ぶた"]
            default_compatibility["bad"] = ["うし", "りゅう", "いぬ"]
        elif animal == "さる":
            default_compatibility["good"] = ["ねずみ", "りゅう", "へび"]
            default_compatibility["bad"] = ["とら", "へび", "ぶた"]
        elif animal == "とり":
            default_compatibility["good"] = ["うし", "へび", "りゅう"]
            default_compatibility["bad"] = ["ねずみ", "うさぎ", "とら"]
        elif animal == "いぬ":
            default_compatibility["good"] = ["とら", "うさぎ", "うま"]
            default_compatibility["bad"] = ["りゅう", "ひつじ", "へび"]
        else:  # いのしし（ぶた）
            default_compatibility["good"] = ["ひつじ", "うさぎ", "とら"]
            default_compatibility["bad"] = ["へび", "さる", "いのしし"]
        
        return default_compatibility
    
    def _get_career(self, full_animal_type: str) -> List[str]:
        """
        動物とタイプから適職を取得する
        
        Args:
            full_animal_type: 動物とタイプの組み合わせ
            
        Returns:
            適職リスト
        """
        # データファイルから適職情報を取得
        if "career" in self.data and full_animal_type in self.data["career"]:
            return self.data["career"][full_animal_type]
        
        # データがない場合は動物のみで一般的な適職を返す
        animal = full_animal_type.split("（")[0]
        
        if "career_by_animal" in self.data and animal in self.data["career_by_animal"]:
            return self.data["career_by_animal"][animal]
        
        # 全くデータがない場合はデフォルト値
        return ["あなたの特性を活かせる職業が向いています。"]


# シングルトンインスタンスを作成
_instance = None

def diagnose(birth_date: datetime.date) -> Dict[str, Any]:
    """
    動物占いによる診断を行うファサードメソッド
    
    Args:
        birth_date: 生年月日
        
    Returns:
        診断結果をDict形式で返す
    """
    global _instance
    
    if _instance is None:
        _instance = AnimalFortune()
    
    return _instance.diagnose(birth_date) 