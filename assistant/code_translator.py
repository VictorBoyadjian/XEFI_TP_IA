from .llm_client import LLMClient

class CodeTranslator:
    def __init__(self, llm_client: LLMClient):
        self.llm = llm_client
    
    def translate_code(self, code: str, source_lang: str, target_lang: str) -> str:
        system_prompt = f"""Tu es un expert en programmation multilangage.
Traduis du code {source_lang} vers {target_lang} en conservant la logique et les bonnes pratiques."""
        
        prompt = f"""Traduis ce code {source_lang} en {target_lang}:

```{source_lang}
{code}
```

Réponds UNIQUEMENT avec le code traduit en {target_lang}, sans explications."""
        
        return self.llm.send_message(prompt, system_prompt)
