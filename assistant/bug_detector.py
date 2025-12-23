from .llm_client import LLMClient
import ast

class BugDetector:
    def __init__(self, llm_client: LLMClient):
        self.llm = llm_client
    
    def detect_bugs(self, code: str) -> str:
        syntax_errors = self._check_syntax(code)
        
        system_prompt = """Tu es un expert en détection de bugs Python.
Analyse le code pour trouver:
- Erreurs logiques
- Problèmes de sécurité
- Fuites de mémoire potentielles
- Erreurs de gestion d'exceptions
- Problèmes de concurrence"""
        
        prompt = f"""Analyse ce code Python pour détecter des bugs potentiels:

```python
{code}
```

Erreurs de syntaxe détectées: {syntax_errors}

Fournis une liste détaillée des bugs potentiels avec leur gravité et des solutions."""
        
        return self.llm.send_message(prompt, system_prompt)
    
    def _check_syntax(self, code: str) -> str:
        try:
            ast.parse(code)
            return "Aucune erreur de syntaxe détectée"
        except SyntaxError as e:
            return f"Erreur de syntaxe ligne {e.lineno}: {e.msg}"
