import json
import os
from datetime import datetime
from typing import List, Dict

class StateManager:
    def __init__(self, state_file: str = "assistant_state.json"):
        self.state_file = state_file
        self.state = self._load_state()
    
    def _load_state(self) -> Dict:
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                return self._get_default_state()
        return self._get_default_state()
    
    def _get_default_state(self) -> Dict:
        return {
            "conversation_history": [],
            "generated_code": [],
            "analyzed_code": [],
            "session_start": datetime.now().isoformat(),
            "preferences": {}
        }
    
    def save_state(self):
        try:
            with open(self.state_file, 'w', encoding='utf-8') as f:
                json.dump(self.state, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Erreur lors de la sauvegarde: {str(e)}")
    
    def add_conversation(self, role: str, content: str):
        self.state["conversation_history"].append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
        self.save_state()
    
    def add_generated_code(self, code_type: str, description: str, code: str):
        self.state["generated_code"].append({
            "type": code_type,
            "description": description,
            "code": code,
            "timestamp": datetime.now().isoformat()
        })
        self.save_state()
    
    def add_analyzed_code(self, code: str, analysis: str):
        self.state["analyzed_code"].append({
            "code": code,
            "analysis": analysis,
            "timestamp": datetime.now().isoformat()
        })
        self.save_state()
    
    def get_conversation_history(self) -> List[Dict]:
        return self.state["conversation_history"]
    
    def clear_state(self):
        self.state = self._get_default_state()
        self.save_state()
    
    def set_preference(self, key: str, value):
        self.state["preferences"][key] = value
        self.save_state()
    
    def get_preference(self, key: str, default=None):
        return self.state["preferences"].get(key, default)
