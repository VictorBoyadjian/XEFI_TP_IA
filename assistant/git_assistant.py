from .llm_client import LLMClient
import subprocess

class GitAssistant:
    def __init__(self, llm_client: LLMClient):
        self.llm = llm_client
    
    def generate_commit_message(self, diff: str = None) -> str:
        if not diff:
            diff = self._get_git_diff()
        
        system_prompt = """Tu es un expert Git. Génère des messages de commit suivant les conventions:
- Type: feat, fix, docs, style, refactor, test, chore
- Format: type(scope): description courte
- Corps optionnel pour détails
- Format conventionnel commits"""
        
        prompt = f"""Génère un message de commit pour ces changements:

```diff
{diff}
```

Fournis un message de commit clair et professionnel."""
        
        return self.llm.send_message(prompt, system_prompt)
    
    def _get_git_diff(self) -> str:
        try:
            result = subprocess.run(
                ['git', 'diff', '--cached'],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.stdout:
                return result.stdout
            
            result = subprocess.run(
                ['git', 'diff'],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.stdout or "Aucun changement détecté"
        except Exception as e:
            return f"Erreur: {str(e)}"
