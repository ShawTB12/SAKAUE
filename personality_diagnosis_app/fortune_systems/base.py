from abc import ABC, abstractmethod
import datetime
import json
import os
from typing import Dict, Any, List

class FortuneSystem(ABC):
    """
    占いシステムの基底クラス
    全ての占いシステムはこのクラスを継承する
    """
    
    def __init__(self, data_file: str):
        """
        初期化メソッド
        
        Args:
            data_file: データファイルのパス
        """
        self.data_file = data_file
        self.data = self._load_data()
    
    def _load_data(self) -> Dict[str, Any]:
        """
        データファイルを読み込む
        
        Returns:
            データをDict形式で返す
        """
        try:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            file_path = os.path.join(base_dir, 'data', self.data_file)
            
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading data file: {e}")
            return {}
    
    @abstractmethod
    def diagnose(self, birth_date: datetime.date) -> Dict[str, Any]:
        """
        誕生日から性格診断を行う抽象メソッド
        継承クラスで実装する必要がある
        
        Args:
            birth_date: 生年月日
            
        Returns:
            診断結果をDict形式で返す
        """
        pass
    
    def get_personality_traits(self, key: str) -> Dict[str, Any]:
        """
        指定されたキーに対応する性格特性を取得する
        
        Args:
            key: 性格特性を取得するためのキー
            
        Returns:
            性格特性をDict形式で返す
        """
        if 'personality_traits' in self.data and key in self.data['personality_traits']:
            return self.data['personality_traits'][key]
        return {}
    
    def get_strengths_and_weaknesses(self, key: str) -> Dict[str, List[str]]:
        """
        指定されたキーに対応する強みと弱みを取得する
        
        Args:
            key: 強みと弱みを取得するためのキー
            
        Returns:
            強みと弱みをDict形式で返す
        """
        result = {'strengths': [], 'weaknesses': []}
        
        if 'strengths' in self.data and key in self.data['strengths']:
            result['strengths'] = self.data['strengths'][key]
        
        if 'weaknesses' in self.data and key in self.data['weaknesses']:
            result['weaknesses'] = self.data['weaknesses'][key]
        
        return result
    
    def get_compatibility(self, key: str) -> Dict[str, List[str]]:
        """
        指定されたキーに対応する相性を取得する
        
        Args:
            key: 相性を取得するためのキー
            
        Returns:
            相性をDict形式で返す
        """
        result = {'good': [], 'bad': []}
        
        if 'compatibility' in self.data and key in self.data['compatibility']:
            if 'good' in self.data['compatibility'][key]:
                result['good'] = self.data['compatibility'][key]['good']
            if 'bad' in self.data['compatibility'][key]:
                result['bad'] = self.data['compatibility'][key]['bad']
        
        return result 