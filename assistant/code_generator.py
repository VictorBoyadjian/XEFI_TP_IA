from .llm_client import LLMClient

class CodeGenerator:
    def __init__(self, llm_client: LLMClient):
        self.llm = llm_client
    
    def generate_function(self, description: str) -> str:
        system_prompt = """Tu es un expert Python. Génère uniquement du code Python sans explications.
Respecte PEP 8. Inclus des docstrings et des type hints."""
        
        prompt = f"""Génère une fonction Python complète basée sur cette description:
{description}

Réponds UNIQUEMENT avec le code Python, sans markdown ni explications."""
        
        return self.llm.send_message(prompt, system_prompt)
    
    def generate_class(self, description: str) -> str:
        system_prompt = """Tu es un expert Python. Génère uniquement du code Python sans explications.
Respecte PEP 8. Inclus des docstrings et des type hints."""
        
        prompt = f"""Génère une classe Python complète basée sur cette description:
{description}

Réponds UNIQUEMENT avec le code Python, sans markdown ni explications."""
        
        return self.llm.send_message(prompt, system_prompt)
    
    def generate_module(self, description: str) -> str:
        system_prompt = """Tu es un expert Python. Génère uniquement du code Python sans explications.
Respecte PEP 8. Inclus des docstrings et des type hints."""
        
        prompt = f"""Génère un module Python complet basé sur cette description:
{description}

Réponds UNIQUEMENT avec le code Python, sans markdown ni explications."""
        
        return self.llm.send_message(prompt, system_prompt)
