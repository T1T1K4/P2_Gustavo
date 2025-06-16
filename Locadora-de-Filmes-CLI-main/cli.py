def exibir_menu_principal():
    print("\n=========== LOCADORA DE FILMES CLI ===========")
    print("--- Gerenciar Filmes ---")
    print("1. Adicionar novo filme ao catálogo")
    print("2. Listar todos os filmes do catálogo")
    print("3. Listar filmes disponíveis")
    print("4. Listar filmes alugados")
    print("5. Buscar filmes por gênero")
    print("6. Buscar filme por ID")
    print("7. Remover filme do catálogo (por ID)")
    print("--- Gerenciar Clientes ---")
    print("10. Adicionar novo cliente")
    print("11. Listar todos os clientes")
    print("12. Ver histórico de aluguéis de um cliente")
    print("13. Remover cliente (por ID)")
    print("--- Operações de Aluguel ---")
    print("20. Alugar filme")
    print("21. Devolver filme")
    print("--- Sistema ---")
    print("40. Ver últimas ações realizadas")
    print("0. Sair do programa")
    print("===============================================")

def obter_escolha_usuario() -> int:
    while True:
        try:
            escolha = int(input("Digite sua opção: "))
            return escolha
        except ValueError:
            print("Entrada inválida. Por favor, digite um número.")

def obter_detalhes_filme_usuario() -> dict | None:
    print("\n--- Adicionar Novo Filme ao Catálogo ---")
    titulo = input("Título do filme: ").strip()
    if not titulo: print("O título é obrigatório."); return None
    
    try:
        ano = int(input("Ano de lançamento: "))
        if not (1888 < ano < 2050):
            print("Ano inválido. O primeiro filme foi lançado em 1888.")
            return None
    except ValueError: 
        print("Ano inválido. Digite um número entre 1888 e 2050.")
        return None

    diretor = input("Diretor: ").strip()
    generos_str = input("Gêneros (separados por vírgula): ").strip()
    generos = set(g.strip().capitalize() for g in generos_str.split(',') if g.strip()) if generos_str else set()
    if not generos:
        print("AVISO: Nenhum gênero informado. Será registrado como 'Não informado'.")
        generos = {"Não informado"}

    atores_str = input("Atores principais (separados por vírgula): ").strip()
    atores = [a.strip() for a in atores_str.split(',') if a.strip()] if atores_str else []
    if not atores:
        print("AVISO: Nenhum ator informado. Será registrado como 'Não informado'.")
        atores = ["Não informado"]

    return {"titulo": titulo, "ano": ano, "diretor": diretor, "generos": generos, "atores": atores}

def obter_detalhes_cliente_usuario() -> dict | None:
    print("\n--- Adicionar Novo Cliente ---")
    nome = input("Nome do cliente: ").strip()
    if not nome: print("Nome é obrigatório."); return None
    contato = input("Contato (telefone/email): ").strip()
    return {"nome": nome, "contato": contato}

def iniciar_interface(gerenciador):
    historico_comandos_menu = [] 
    while True:
        exibir_menu_principal()
        escolha = obter_escolha_usuario()
        historico_comandos_menu.append(escolha)

        if escolha == 1:
            detalhes = obter_detalhes_filme_usuario()
            if detalhes:
                gerenciador.adicionar_filme_catalogo(
                    detalhes["titulo"], detalhes["ano"], detalhes["diretor"],
                    detalhes["generos"], detalhes["atores"]
                )
        elif escolha == 2:
            gerenciador.listar_todos_os_filmes()
        elif escolha == 3:
            gerenciador.listar_filmes_por_status('disponivel')
        elif escolha == 4:
            gerenciador.listar_filmes_por_status('alugado')
        elif escolha == 5:
            print("\n--- Buscar Filmes por Gênero ---")
            gerenciador.listar_generos_disponiveis()
            genero = input("\nDigite o gênero desejado: ").strip()
            gerenciador.buscar_por_genero(genero)
        elif escolha == 6:
            id_filme = input("Digite o ID do filme para buscar: ").strip()
            filme = gerenciador.buscar_filme_por_id(id_filme)
            if filme:
                print(f"\nDetalhes do filme:")
                print(f"Título: {filme['titulo']}")
                print(f"Ano: {filme['ano']}")
                print(f"ID: {filme['id']}")
                print(f"Diretor: {filme.get('diretor', 'N/A')}")
                print(f"Gêneros: {', '.join(filme.get('generos', ['N/A']))}")
                print(f"Atores: {', '.join(filme.get('atores', ['N/A']))}")
                print(f"Status: {filme['status'].upper()}")
                if filme['status'] == 'alugado':
                    cliente_alugou = gerenciador.buscar_cliente_por_id(filme.get('id_cliente_alugou', ''))
                    nome_cliente = cliente_alugou['nome'] if cliente_alugou else "Desconhecido"
                    print(f"Alugado por: {nome_cliente} (ID Cliente: {filme.get('id_cliente_alugou', 'N/A')}) em {filme.get('data_aluguel', 'N/A')}")
        elif escolha == 7:
            id_filme = input("Digite o ID do filme para remover do catálogo: ").strip()
            gerenciador.remover_filme_catalogo(id_filme)
        elif escolha == 10:
            detalhes_cliente = obter_detalhes_cliente_usuario()
            if detalhes_cliente:
                gerenciador.adicionar_cliente(detalhes_cliente['nome'], detalhes_cliente['contato'])
        elif escolha == 11:
            gerenciador.listar_clientes()
        elif escolha == 12:
            id_cliente = input("Digite o ID do cliente para ver o histórico: ").strip()
            gerenciador.ver_historico_cliente(id_cliente)
        elif escolha == 13:
            id_cliente = input("Digite o ID do cliente para remover: ").strip()
            gerenciador.remover_cliente(id_cliente)
        elif escolha == 20:
            id_filme = input("Digite o ID do filme a ser alugado: ").strip()
            id_cliente = input("Digite o ID do cliente que está alugando: ").strip()
            gerenciador.alugar_filme(id_filme, id_cliente)
        elif escolha == 21:
            id_filme = input("Digite o ID do filme a ser devolvido: ").strip()
            gerenciador.devolver_filme(id_filme)
        elif escolha == 40:
            quantidade = input("Quantas últimas ações deseja ver? (padrão: 10): ").strip()
            try:
                quantidade = int(quantidade) if quantidade else 10
                gerenciador.ver_ultimas_acoes(quantidade)
            except ValueError:
                print("Quantidade inválida. Usando o valor padrão de 10.")
                gerenciador.ver_ultimas_acoes()
        elif escolha == 0:
            print("\nObrigado por usar a Locadora de Filmes CLI!")
            if len(historico_comandos_menu) > 1:
                print("Últimas opções de menu selecionadas (da mais recente para a mais antiga):")
                for cmd in reversed(historico_comandos_menu[-6:-1]): 
                    print(f" -> Opção {cmd}")
            break
        else:
            print("Opção desconhecida. Por favor, tente novamente.")
        if escolha != 0:
            input("\nPressione Enter para continuar...")