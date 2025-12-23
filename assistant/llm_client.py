import ollama
from typing import List, Dict

class LLMClient:
    def __init__(self, model: str = "codellama:7b"):
        self.model = model
        self.conversation_history: List[Dict[str, str]] = []
    
    def send_message(self, message: str, system_prompt: str = None) -> str:
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.extend(self.conversation_history)
        messages.append({"role": "user", "content": message})
        
        try:
            response = ollama.chat(model=self.model, messages=messages)
            assistant_message = response['message']['content']
            
            self.conversation_history.append({"role": "user", "content": message})
            self.conversation_history.append({"role": "assistant", "content": assistant_message})
            
            return assistant_message
        except Exception as e:
            return f"Erreur de communication avec le modèle: {str(e)}"
    
    def clear_history(self):
        self.conversation_history = []
    
    def get_history(self) -> List[Dict[str, str]]:
        return self.conversation_history
