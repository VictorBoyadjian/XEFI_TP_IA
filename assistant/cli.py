from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.prompt import Prompt
from rich.table import Table
from rich.syntax import Syntax
from .llm_client import LLMClient
from .code_generator import CodeGenerator
from .code_analyzer import CodeAnalyzer
from .test_generator import TestGenerator
from .code_translator import CodeTranslator
from .bug_detector import BugDetector
from .git_assistant import GitAssistant
from .state_manager import StateManager

class CLI:
    def __init__(self):
        self.console = Console()
        self.llm = LLMClient()
        self.code_gen = CodeGenerator(self.llm)
        self.code_analyzer = CodeAnalyzer(self.llm)
        self.test_gen = TestGenerator(self.llm)
        self.translator = CodeTranslator(self.llm)
        self.bug_detector = BugDetector(self.llm)
        self.git_assistant = GitAssistant(self.llm)
        self.state_manager = StateManager()
    
    def run(self):
        self.console.clear()
        self.show_welcome()
        
        while True:
            try:
                choice = self.show_menu()
                
                if choice == "0":
                    self.console.print("[yellow]Au revoir ![/yellow]")
                    break
                
                self.handle_choice(choice)
                
            except KeyboardInterrupt:
                self.console.print("\n[yellow]Interruption détectée. Au revoir ![/yellow]")
                break
            except Exception as e:
                self.console.print(f"[red]Erreur: {str(e)}[/red]")
    
    def show_welcome(self):
        welcome_text = """
# 🚀 Assistant Python Personnalisé

Votre assistant de développement Python intelligent propulsé par Llama 3.2
        """
        self.console.print(Panel(Markdown(welcome_text), style="bold blue"))
    
    def show_menu(self) -> str:
        table = Table(title="Menu Principal", show_header=True, header_style="bold magenta")
        table.add_column("N°", style="cyan", width=6)
        table.add_column("Fonctionnalité", style="green")
        
        table.add_row("1", "Génération de code (fonction/classe/module)")
        table.add_row("2", "Analyse de code")
        table.add_row("3", "Générateur de tests")
        table.add_row("4", "Traducteur de code")
        table.add_row("5", "Détecteur de bugs")
        table.add_row("6", "Assistant Git")
        table.add_row("7", "Formater le code (PEP 8)")
        table.add_row("8", "Historique de conversation")
        table.add_row("9", "Sauvegarder le code généré")
        table.add_row("0", "Quitter")
        
        self.console.print(table)
        return Prompt.ask("\n[bold cyan]Choisissez une option[/bold cyan]", choices=["0","1","2","3","4","5","6","7","8","9"])
    
    def handle_choice(self, choice: str):
        if choice == "1":
            self.generate_code_menu()
        elif choice == "2":
            self.analyze_code_menu()
        elif choice == "3":
            self.generate_tests_menu()
        elif choice == "4":
            self.translate_code_menu()
        elif choice == "5":
            self.detect_bugs_menu()
        elif choice == "6":
            self.git_assistant_menu()
        elif choice == "7":
            self.format_code_menu()
        elif choice == "8":
            self.show_history()
        elif choice == "9":
            self.save_code_menu()
    
    def generate_code_menu(self):
        self.console.print("\n[bold green]Génération de Code[/bold green]")
        code_type = Prompt.ask(
            "Type de code",
            choices=["fonction", "classe", "module"],
            default="fonction"
        )
        
        description = Prompt.ask("Description du code à générer")
        
        self.console.print("[yellow]Génération en cours...[/yellow]")
        
        if code_type == "fonction":
            code = self.code_gen.generate_function(description)
        elif code_type == "classe":
            code = self.code_gen.generate_class(description)
        else:
            code = self.code_gen.generate_module(description)
        
        self.display_code(code, "python")
        self.state_manager.add_generated_code(code_type, description, code)
        
        if Prompt.ask("Sauvegarder ce code ?", choices=["o", "n"], default="n") == "o":
            self.save_code_to_file(code, code_type)
    
    def analyze_code_menu(self):
        self.console.print("\n[bold green]Analyse de Code[/bold green]")
        code = self.get_code_input()
        
        self.console.print("[yellow]Analyse en cours...[/yellow]")
        analysis = self.code_analyzer.analyze_code(code)
        
        self.console.print(Panel(Markdown(analysis), title="Analyse", border_style="green"))
        self.state_manager.add_analyzed_code(code, analysis)
    
    def generate_tests_menu(self):
        self.console.print("\n[bold green]Génération de Tests[/bold green]")
        code = self.get_code_input()
        framework = Prompt.ask("Framework de test", choices=["pytest", "unittest"], default="pytest")
        
        self.console.print("[yellow]Génération des tests...[/yellow]")
        tests = self.test_gen.generate_tests(code, framework)
        
        self.display_code(tests, "python")
        
        if Prompt.ask("Sauvegarder les tests ?", choices=["o", "n"], default="n") == "o":
            self.save_code_to_file(tests, "tests")
    
    def translate_code_menu(self):
        self.console.print("\n[bold green]Traduction de Code[/bold green]")
        code = self.get_code_input()
        source_lang = Prompt.ask("Langage source", default="python")
        target_lang = Prompt.ask("Langage cible", default="javascript")
        
        self.console.print("[yellow]Traduction en cours...[/yellow]")
        translated = self.translator.translate_code(code, source_lang, target_lang)
        
        self.display_code(translated, target_lang)
    
    def detect_bugs_menu(self):
        self.console.print("\n[bold green]Détection de Bugs[/bold green]")
        code = self.get_code_input()
        
        self.console.print("[yellow]Analyse en cours...[/yellow]")
        bugs = self.bug_detector.detect_bugs(code)
        
        self.console.print(Panel(Markdown(bugs), title="Bugs Détectés", border_style="red"))
    
    def git_assistant_menu(self):
        self.console.print("\n[bold green]Assistant Git[/bold green]")
        
        self.console.print("[yellow]Génération du message de commit...[/yellow]")
        commit_msg = self.git_assistant.generate_commit_message()
        
        self.console.print(Panel(commit_msg, title="Message de Commit", border_style="blue"))
    
    def format_code_menu(self):
        self.console.print("\n[bold green]Formatage du Code (PEP 8)[/bold green]")
        code = self.get_code_input()
        
        self.console.print("[yellow]Formatage en cours...[/yellow]")
        formatted = self.code_analyzer.format_code(code)
        
        self.display_code(formatted, "python")
    
    def show_history(self):
        history = self.state_manager.get_conversation_history()
        
        if not history:
            self.console.print("[yellow]Aucun historique disponible[/yellow]")
            return
        
        self.console.print(f"\n[bold cyan]Historique ({len(history)} entrées)[/bold cyan]\n")
        
        for i, entry in enumerate(history[-10:], 1):
            role = entry["role"]
            content = entry["content"][:100] + "..." if len(entry["content"]) > 100 else entry["content"]
            timestamp = entry.get("timestamp", "")
            
            self.console.print(f"[cyan]{i}. [{role}] ({timestamp})[/cyan]")
            self.console.print(f"   {content}\n")
    
    def save_code_menu(self):
        generated = self.state_manager.state.get("generated_code", [])
        
        if not generated:
            self.console.print("[yellow]Aucun code généré à sauvegarder[/yellow]")
            return
        
        self.console.print(f"\n[cyan]Code généré récent ({len(generated)} éléments)[/cyan]\n")
        
        for i, item in enumerate(generated[-5:], 1):
            self.console.print(f"{i}. [{item['type']}] {item['description']}")
        
        choice = Prompt.ask("Numéro du code à sauvegarder (ou 0 pour annuler)")
        
        if choice != "0" and choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(generated[-5:]):
                actual_idx = len(generated) - 5 + idx
                item = generated[actual_idx]
                self.save_code_to_file(item["code"], item["type"])
    
    def get_code_input(self) -> str:
        self.console.print("[cyan]Entrez votre code (tapez 'FIN' sur une ligne vide pour terminer):[/cyan]")
        lines = []
        while True:
            line = input()
            if line.strip() == "FIN":
                break
            lines.append(line)
        return "\n".join(lines)
    
    def display_code(self, code: str, language: str = "python"):
        syntax = Syntax(code, language, theme="monokai", line_numbers=True)
        self.console.print(Panel(syntax, title=f"Code {language}", border_style="green"))
    
    def save_code_to_file(self, code: str, code_type: str):
        filename = Prompt.ask("Nom du fichier", default=f"{code_type}.py")
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(code)
            self.console.print(f"[green]Code sauvegardé dans {filename}[/green]")
        except Exception as e:
            self.console.print(f"[red]Erreur lors de la sauvegarde: {str(e)}[/red]")
