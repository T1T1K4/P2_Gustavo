from gerenciador_locadora import GerenciadorLocadora
from cli import iniciar_interface
import sys

def popular_dados_exemplo_locadora(gerenciador: GerenciadorLocadora):
    print("Populando dados iniciais para a locadora...")
    f1_data = gerenciador.adicionar_filme_catalogo("Matrix Reloaded", 2003, "Wachowskis", {"Ação", "Ficção Científica"}, ["Keanu Reeves"])
    f2_data = gerenciador.adicionar_filme_catalogo("O Senhor dos Anéis: A Sociedade do Anel", 2001, "Peter Jackson", {"Fantasia", "Aventura"}, ["Elijah Wood"])
    f3_data = gerenciador.adicionar_filme_catalogo("A Viagem de Chihiro", 2001, "Hayao Miyazaki", {"Animação", "Fantasia"}, ["Não informado"])
    
    c1_data = gerenciador.adicionar_cliente("Ana Silva", "ana.silva@email.com")
    c2_data = gerenciador.adicionar_cliente("Bruno Costa", "99999-8888")

    if f1_data and c1_data:
        gerenciador.alugar_filme(f1_data['id'], c1_data['id_cliente'])
    
    print("-" * 30)
    print("Dados de exemplo da locadora populados.")
    print("-" * 30)

def iniciar_sistema():
    meu_gerenciador_locadora = GerenciadorLocadora()
    
    # Verifica se foi passado o argumento --sem-dados
    if len(sys.argv) > 1 and sys.argv[1] == "--sem-dados":
        print("Iniciando sistema sem dados de exemplo...")
    else:
        popular_dados_exemplo_locadora(meu_gerenciador_locadora)

    try:
        iniciar_interface(meu_gerenciador_locadora)
    except Exception as e:
        print(f"\nERRO CRÍTICO NO PROGRAMA: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("\nPrograma da locadora finalizado.")

if __name__ == "__main__":
    iniciar_sistema()