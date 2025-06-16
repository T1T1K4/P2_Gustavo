import uuid
import datetime
from linkedlist import DoublyLinkedList, Node

def gerar_id_unico():
    return str(uuid.uuid4().hex)[:4]

def criar_payload_filme(titulo: str, ano: int, diretor: str, generos: set, atores: list) -> dict:
    if not isinstance(titulo, str) or not titulo.strip():
        raise ValueError("O título do filme não pode ser vazio.")
    if not isinstance(ano, int) or not (1888 < ano < 2050):
        raise ValueError("Ano de lançamento inválido. O primeiro filme foi lançado em 1888.")
    if not isinstance(diretor, str) or not diretor.strip():
        diretor = "Desconhecido"
    if not isinstance(generos, set): generos = set(generos)
    if not isinstance(atores, list): atores = list(atores)
    return {
        'id': gerar_id_unico(), 'titulo': titulo, 'ano': ano, 'diretor': diretor,
        'generos': generos, 'atores': atores, 'status': 'disponivel',
        'id_cliente_alugou': None, 'data_aluguel': None
    }

def criar_payload_cliente(nome: str, contato: str) -> dict:
    if not isinstance(nome, str) or not nome.strip():
        raise ValueError("O nome do cliente não pode ser vazio.")
    if not isinstance(contato, str) or not contato.strip():
        contato = "Não informado"
    return {
        'id_cliente': "cliente_" + gerar_id_unico(), 'nome': nome,
        'contato': contato, 'historico_alugueis': []
    }

class GerenciadorLocadora:
    def __init__(self):
        self.catalogo_filmes_dll = DoublyLinkedList()
        self.filmes_por_id_idx = {}
        self.generos_para_filmes_idx = {}
        self.atores_para_filmes_idx = {}
        self.diretores_para_filmes_idx = {}
        self.clientes_cadastrados = {}
        self.pilha_acoes = [] 

    def registrar_acao(self, acao: str):
        """Registra uma ação na pilha de ações."""
        data_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.pilha_acoes.append(f"[{data_hora}] {acao}")

    def ver_ultimas_acoes(self, quantidade: int = 10):
        """Exibe as últimas ações realizadas no sistema."""
        if not self.pilha_acoes:
            print("Nenhuma ação registrada no sistema.")
            return

        print("\n--- Últimas Ações Realizadas ---")
        ultimas_acoes = self.pilha_acoes[-quantidade:]
        for i, acao in enumerate(reversed(ultimas_acoes), 1):
            print(f"{i}. {acao}")
        print("-" * 40)

    def _adicionar_filme_aos_indices(self, dados_filme: dict):
        id_filme = dados_filme['id']
        for genero in dados_filme.get('generos', set()):
            self.generos_para_filmes_idx.setdefault(genero.lower(), set()).add(id_filme)
        for ator in dados_filme.get('atores', []):
            self.atores_para_filmes_idx.setdefault(ator.lower(), set()).add(id_filme)
        diretor = dados_filme.get('diretor')
        if diretor:
            self.diretores_para_filmes_idx.setdefault(diretor.lower(), set()).add(id_filme)

    def _remover_filme_dos_indices(self, dados_filme: dict):
        id_filme = dados_filme['id']
        for genero in dados_filme.get('generos', set()):
            chave_genero = genero.lower()
            if chave_genero in self.generos_para_filmes_idx and id_filme in self.generos_para_filmes_idx[chave_genero]:
                self.generos_para_filmes_idx[chave_genero].remove(id_filme)
                if not self.generos_para_filmes_idx[chave_genero]:
                    del self.generos_para_filmes_idx[chave_genero]
        for ator in dados_filme.get('atores', []):
            chave_ator = ator.lower()
            if chave_ator in self.atores_para_filmes_idx and id_filme in self.atores_para_filmes_idx[chave_ator]:
                self.atores_para_filmes_idx[chave_ator].remove(id_filme)
                if not self.atores_para_filmes_idx[chave_ator]: del self.atores_para_filmes_idx[chave_ator]
        diretor = dados_filme.get('diretor')
        if diretor:
            chave_diretor = diretor.lower()
            if chave_diretor in self.diretores_para_filmes_idx and id_filme in self.diretores_para_filmes_idx[chave_diretor]:
                self.diretores_para_filmes_idx[chave_diretor].remove(id_filme)
                if not self.diretores_para_filmes_idx[chave_diretor]: del self.diretores_para_filmes_idx[chave_diretor]

    def adicionar_filme_catalogo(self, titulo: str, ano: int, diretor: str, generos: set, atores: list) -> dict | None:
        try:
            for no_existente in self.catalogo_filmes_dll:
                if no_existente.data['titulo'].lower() == titulo.lower() and no_existente.data['ano'] == ano:
                    print(f"ERRO: Filme '{titulo}' ({ano}) já existe no catálogo.")
                    return None
            dados_filme = criar_payload_filme(titulo, ano, diretor, generos, atores)
        except ValueError as e:
            print(f"ERRO ao validar dados do filme: {e}")
            return None
        
        novo_no_filme_obj = Node(dados_filme)
        self.catalogo_filmes_dll.add_last(novo_no_filme_obj)
        
        no_filme_adicionado_na_dll = self.catalogo_filmes_dll.tail
        self.filmes_por_id_idx[dados_filme['id']] = no_filme_adicionado_na_dll
        
        self._adicionar_filme_aos_indices(dados_filme)
        self.registrar_acao(f"Filme '{dados_filme['titulo']}' adicionado ao catálogo (ID: {dados_filme['id']})")
        print(f"SUCESSO: Filme '{dados_filme['titulo']}' adicionado ao catálogo com ID: {dados_filme['id']}")
        return dados_filme

    def buscar_filme_por_id(self, id_filme: str) -> dict | None:
        no_filme = self.filmes_por_id_idx.get(id_filme)
        return no_filme.data if no_filme else None

    def listar_todos_os_filmes(self):
        if self.catalogo_filmes_dll.empty():
            print("Catálogo de filmes vazio.")
            return
        print("\n--- Catálogo de Filmes ---")
        total_filmes = 0
        for i, no_filme in enumerate(self.catalogo_filmes_dll):
            filme = no_filme.data
            total_filmes += 1
            print(f"\n{total_filmes}. {filme['titulo']} ({filme['ano']})")
            print(f"   ID: {filme['id']}")
            print(f"   Diretor: {filme.get('diretor', 'N/A')}")
            print(f"   Gêneros: {', '.join(filme.get('generos', ['N/A']))}")
            print(f"   Atores: {', '.join(filme.get('atores', ['N/A']))}")
            status_str = f"Status: {filme['status'].upper()}"
            if filme['status'] == 'alugado':
                cliente_alugou = self.clientes_cadastrados.get(filme['id_cliente_alugou'], {})
                cliente_nome = cliente_alugou.get('nome', 'Desconhecido')
                status_str += f" (Alugado por: {cliente_nome} em {filme['data_aluguel']})"
            print(f"   {status_str}")
            print("-" * 40)
        print(f"\nTotal de filmes no catálogo: {total_filmes}")

    def listar_filmes_por_status(self, status_desejado: str):
        if self.catalogo_filmes_dll.empty():
            print(f"Nenhum filme no catálogo para listar como '{status_desejado}'.")
            return
        print(f"\n--- Filmes com Status: {status_desejado.upper()} ---")
        encontrados = 0
        for i, no_filme in enumerate(self.catalogo_filmes_dll):
            filme = no_filme.data
            if filme['status'] == status_desejado:
                encontrados += 1
                print(f"\n{encontrados}. {filme['titulo']} ({filme['ano']})")
                print(f"   ID: {filme['id']}")
                print(f"   Diretor: {filme.get('diretor', 'N/A')}")
                print(f"   Gêneros: {', '.join(filme.get('generos', ['N/A']))}")
                print(f"   Atores: {', '.join(filme.get('atores', ['N/A']))}")
                info_aluguel = ""
                if status_desejado == 'alugado' and filme['id_cliente_alugou']:
                    cliente_alugou = self.clientes_cadastrados.get(filme['id_cliente_alugou'], {})
                    cliente_nome = cliente_alugou.get('nome', 'Cliente Desconhecido')
                    info_aluguel = f" (Alugado por: {cliente_nome} em {filme['data_aluguel']})"
                print(f"   Status: {filme['status'].upper()}{info_aluguel}")
                print("-" * 40)
        if encontrados == 0:
            print(f"Nenhum filme encontrado com status '{status_desejado}'.")
        else:
            print(f"\nTotal de filmes encontrados: {encontrados}")

    def remover_filme_catalogo(self, id_filme: str) -> bool:
        no_a_remover_ref = self.filmes_por_id_idx.get(id_filme)
        if not no_a_remover_ref:
            print(f"ERRO: Filme com ID '{id_filme}' não encontrado.")
            return False
        if no_a_remover_ref.data['status'] == 'alugado':
            print(f"ERRO: Filme '{no_a_remover_ref.data['titulo']}' está atualmente alugado e não pode ser removido.")
            return False

        dados_filme_removido = no_a_remover_ref.data
        try:
            self.catalogo_filmes_dll.remove(no_a_remover_ref)
            del self.filmes_por_id_idx[id_filme]
            self._remover_filme_dos_indices(dados_filme_removido)
            self.registrar_acao(f"Filme '{dados_filme_removido['titulo']}' removido do catálogo (ID: {id_filme})")
            print(f"SUCESSO: Filme '{dados_filme_removido['titulo']}' removido do catálogo.")
            return True
        except ValueError as e:
            print(f"ERRO: Filme não encontrado na lista. {str(e)}")
            return False
        except Exception as e:
            print(f"ERRO: Ocorreu um problema ao tentar remover o filme. {str(e)}")
            return False

    def adicionar_cliente(self, nome: str, contato: str) -> dict | None:
        try:
            for cliente_existente in self.clientes_cadastrados.values():
                if cliente_existente['nome'].lower() == nome.lower():
                    print(f"ERRO: Cliente '{nome}' já cadastrado com ID {cliente_existente['id_cliente']}.")
                    return None
            payload_cliente = criar_payload_cliente(nome, contato)
        except ValueError as e:
            print(f"ERRO ao validar dados do cliente: {e}")
            return None
        self.clientes_cadastrados[payload_cliente['id_cliente']] = payload_cliente
        self.registrar_acao(f"Cliente '{payload_cliente['nome']}' adicionado (ID: {payload_cliente['id_cliente']})")
        print(f"SUCESSO: Cliente '{payload_cliente['nome']}' adicionado com ID: {payload_cliente['id_cliente']}")
        return payload_cliente

    def buscar_cliente_por_id(self, id_cliente: str) -> dict | None:
        cliente = self.clientes_cadastrados.get(id_cliente)
        if not cliente:
            print(f"AVISO: Cliente com ID '{id_cliente}' não encontrado.")
        return cliente
        
    def listar_clientes(self):
        if not self.clientes_cadastrados:
            print("Nenhum cliente cadastrado.")
            return
        print("\n--- Lista de Clientes Cadastrados ---")
        for i, (id_cliente, cliente) in enumerate(self.clientes_cadastrados.items()):
            print(f"{i+1}. Nome: {cliente['nome']} (ID: {id_cliente}, Contato: {cliente['contato']})")
            if cliente['historico_alugueis']:
                print(f"   Histórico: {len(cliente['historico_alugueis'])} aluguel(éis)")
            else:
                print("   Histórico: Nenhum aluguel registrado.")

    def alugar_filme(self, id_filme: str, id_cliente: str) -> bool:
        no_filme = self.filmes_por_id_idx.get(id_filme)
        cliente = self.clientes_cadastrados.get(id_cliente)

        if not no_filme:
            print(f"ERRO: Filme com ID '{id_filme}' não encontrado.")
            return False
        if not cliente:
            print(f"ERRO: Cliente com ID '{id_cliente}' não encontrado.")
            return False

        dados_filme = no_filme.data
        if dados_filme['status'] == 'alugado':
            print(f"ERRO: Filme '{dados_filme['titulo']}' já está alugado.")
            return False

        dados_filme['status'] = 'alugado'
        dados_filme['id_cliente_alugou'] = id_cliente
        dados_filme['data_aluguel'] = datetime.date.today().strftime("%Y-%m-%d")
        
        registro_aluguel = (
            id_filme, dados_filme['titulo'],
            dados_filme['data_aluguel'], None
        )

        cliente['historico_alugueis'].append(registro_aluguel)
        self.registrar_acao(f"Filme '{dados_filme['titulo']}' alugado para '{cliente['nome']}' (ID Cliente: {id_cliente})")
        print(f"SUCESSO: Filme '{dados_filme['titulo']}' alugado para '{cliente['nome']}' em {dados_filme['data_aluguel']}.")
        return True

    def devolver_filme(self, id_filme: str) -> bool:
        no_filme = self.filmes_por_id_idx.get(id_filme)
        if not no_filme:
            print(f"ERRO: Filme com ID '{id_filme}' não encontrado.")
            return False

        dados_filme = no_filme.data
        if dados_filme['status'] != 'alugado':
            print(f"ERRO: Filme '{dados_filme['titulo']}' não está alugado.")
            return False

        id_cliente = dados_filme['id_cliente_alugou']
        cliente = self.clientes_cadastrados.get(id_cliente)
        if not cliente:
            print(f"ERRO: Cliente que alugou o filme não encontrado.")
            return False

        data_devolucao = datetime.date.today().strftime("%Y-%m-%d")
        
        # Atualizar o registro de aluguel no histórico do cliente
        for i, aluguel in enumerate(cliente['historico_alugueis']):
            if aluguel[0] == id_filme and not aluguel[3]:  # Se é o filme e não tem data de devolução
                cliente['historico_alugueis'][i] = (aluguel[0], aluguel[1], aluguel[2], data_devolucao)
                break

        # Resetar os dados do filme
        dados_filme['status'] = 'disponivel'
        dados_filme['id_cliente_alugou'] = None
        dados_filme['data_aluguel'] = None

        self.registrar_acao(f"Filme '{dados_filme['titulo']}' devolvido por '{cliente['nome']}' (ID Cliente: {id_cliente})")
        print(f"SUCESSO: Filme '{dados_filme['titulo']}' devolvido com sucesso.")
        return True

    def ver_historico_cliente(self, id_cliente: str):
        cliente = self.buscar_cliente_por_id(id_cliente)
        if not cliente: return
        print(f"\n--- Histórico de Aluguéis do Cliente: {cliente['nome']} (ID: {id_cliente}) ---")
        if not cliente['historico_alugueis']:
            print("Nenhum aluguel registrado para este cliente.")
            return
        
        for aluguel_tupla in cliente['historico_alugueis']:
            id_filme, titulo_filme, data_aluguel, data_devolucao = aluguel_tupla
            devolucao_str = data_devolucao if data_devolucao else "Pendente"
            print(f"- Filme: {titulo_filme} (ID: {id_filme})")
            print(f"  Alugado em: {data_aluguel}, Devolvido em: {devolucao_str}")
            print("-" * 15)

    def remover_cliente(self, id_cliente: str) -> bool:
        cliente = self.clientes_cadastrados.get(id_cliente)
        if not cliente:
            print(f"ERRO: Cliente com ID '{id_cliente}' não encontrado.")
            return False

        # Verificar se o cliente tem filmes alugados
        for no_filme in self.catalogo_filmes_dll:
            if no_filme.data['id_cliente_alugou'] == id_cliente:
                print(f"ERRO: Cliente '{cliente['nome']}' tem filmes alugados e não pode ser removido.")
                return False

        # Remover o cliente
        nome_cliente = cliente['nome']
        del self.clientes_cadastrados[id_cliente]
        self.registrar_acao(f"Cliente '{nome_cliente}' removido do sistema (ID: {id_cliente})")
        print(f"SUCESSO: Cliente '{nome_cliente}' removido do sistema.")
        return True

    def listar_generos_disponiveis(self):
        if not self.generos_para_filmes_idx:
            print("Nenhum gênero cadastrado no sistema.")
            return
        
        print("\nGêneros disponíveis:")
        generos_ordenados = sorted(self.generos_para_filmes_idx.keys())
        for genero in generos_ordenados:
            print(f"- {genero.capitalize()}")

    def buscar_por_genero(self, genero: str) -> bool:
        if not genero or not genero.strip():
            print("ERRO: Gênero não pode ser vazio.")
            return False

        genero_normalizado = genero.strip().lower()
        ids_filmes = self.generos_para_filmes_idx.get(genero_normalizado)

        if not ids_filmes:
            print(f"Nenhum filme encontrado para o gênero '{genero.capitalize()}'.")
            return False

        print(f"\n--- Filmes do gênero: {genero.capitalize()} ---")
        total_encontrados = 0
        for id_filme in ids_filmes:
            no_filme = self.filmes_por_id_idx.get(id_filme)
            if no_filme:
                filme = no_filme.data
                total_encontrados += 1
                print(f"\n{total_encontrados}. {filme['titulo']} ({filme['ano']})")
                print(f"   ID: {filme['id']}")
                print(f"   Diretor: {filme.get('diretor', 'N/A')}")
                print(f"   Status: {filme['status'].upper()}")
                if filme['status'] == 'alugado':
                    cliente = self.clientes_cadastrados.get(filme['id_cliente_alugou'], {})
                    print(f"   Alugado por: {cliente.get('nome', 'Desconhecido')} em {filme['data_aluguel']}")
                print("-" * 40)

        print(f"\nTotal de filmes encontrados: {total_encontrados}")
        return True