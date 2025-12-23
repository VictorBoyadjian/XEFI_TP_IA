from .llm_client import LLMClient

class TestGenerator:
    def __init__(self, llm_client: LLMClient):
        self.llm = llm_client
    
    def generate_tests(self, code: str, framework: str = "pytest") -> str:
        system_prompt = f"""Tu es un expert en tests Python avec {framework}.
Génère des tests unitaires complets."""
        
        prompt = f"""Génère des tests unitaires {framework} pour ce code:

```python
{code}
```

Inclus des tests pour:
- Cas normaux
- Cas limites
- Gestion d'erreurs

Réponds UNIQUEMENT avec le code des tests, sans explications."""
        
        return self.llm.send_message(prompt, system_prompt)
