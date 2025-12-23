from .llm_client import LLMClient
import autopep8
import subprocess
import tempfile
import os

class CodeAnalyzer:
    def __init__(self, llm_client: LLMClient):
        self.llm = llm_client
    
    def analyze_code(self, code: str) -> str:
        system_prompt = """Tu es un expert Python spécialisé dans l'analyse de code.
Analyse le code et fournis des suggestions d'amélioration concernant:
- Performance
- Lisibilité
- Sécurité
- Bonnes pratiques Python
- Respect de PEP 8"""
        
        prompt = f"""Analyse ce code Python et fournis des suggestions d'amélioration:

```python
{code}
```

Fournis une analyse détaillée avec des suggestions concrètes."""
        
        return self.llm.send_message(prompt, system_prompt)
    
    def suggest_improvements(self, code: str) -> str:
        return self.analyze_code(code)
    
    def format_code(self, code: str) -> str:
        try:
            formatted = autopep8.fix_code(code)
            return formatted
        except Exception as e:
            return f"Erreur lors du formatage: {str(e)}\n\nCode original:\n{code}"
    
    def check_pylint(self, code: str) -> str:
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(code)
                temp_file = f.name
            
            result = subprocess.run(
                ['pylint', temp_file],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            os.unlink(temp_file)
            return result.stdout
        except FileNotFoundError:
            return "Pylint n'est pas installé ou accessible"
        except Exception as e:
            return f"Erreur lors de l'analyse pylint: {str(e)}"
