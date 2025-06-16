# Sistema de Locadora de Filmes CLI

Um sistema de gerenciamento de locadora de filmes desenvolvido em Python com interface de linha de comando (CLI).

## 📋 Descrição

Este sistema permite gerenciar uma locadora de filmes, oferecendo funcionalidades para:
- Cadastro e gerenciamento de filmes
- Cadastro e gerenciamento de clientes
- Aluguel e devolução de filmes
- Busca de filmes por diversos critérios
- Histórico de aluguéis
- Registro de ações do sistema

## 🚀 Funcionalidades

### Gerenciamento de Filmes
- Adicionar filmes ao catálogo
- Remover filmes do catálogo
- Listar todos os filmes
- Buscar filmes por ID
- Listar filmes por status (disponível/alugado)
- Buscar filmes por gênero
- Visualizar gêneros disponíveis

### Gerenciamento de Clientes
- Cadastrar novos clientes
- Remover clientes
- Listar todos os clientes
- Buscar cliente por ID
- Visualizar histórico de aluguéis do cliente

### Operações de Aluguel
- Alugar filmes
- Devolver filmes
- Verificar status de disponibilidade

### Sistema
- Registro de ações realizadas
- Visualização das últimas ações do sistema
- Dados de exemplo para teste

## 🛠️ Tecnologias Utilizadas

- Python 3.x
- Estrutura de dados: Lista Duplamente Encadeada (DoublyLinkedList)
- Sistema de índices para busca eficiente
- Interface de linha de comando (CLI)

## 📦 Estrutura do Projeto

```
.
├── main.py                 # Ponto de entrada do programa
├── gerenciador_locadora.py # Classe principal de gerenciamento
├── linkedlist.py          # Implementação da lista duplamente encadeada
└── cli.py                 # Interface de linha de comando
```

## 🚀 Como Executar

1. Clone o repositório
2. Certifique-se de ter o Python 3.x instalado
3. Execute o programa principal:

```bash
python main.py
```

Para iniciar o sistema sem dados de exemplo:
```bash
python main.py --sem-dados
```

## 📝 Exemplo de Uso

O sistema inclui dados de exemplo que são carregados automaticamente ao iniciar, incluindo:
- Filmes como "Matrix Reloaded", "O Senhor dos Anéis" e "A Viagem de Chihiro"
- Clientes de exemplo
- Um aluguel de exemplo

## 🔍 Funcionalidades de Busca

O sistema oferece múltiplas formas de busca:
- Por ID do filme
- Por gênero
- Por status (disponível/alugado)
- Por cliente
- Por histórico de aluguéis

## ⚠️ Validações

O sistema inclui validações para:
- Dados de entrada de filmes e clientes
- Operações de aluguel e devolução
- Remoção de filmes e clientes
- Duplicidade de registros

## 📊 Registro de Ações

Todas as ações importantes são registradas no sistema, incluindo:
- Adição/remoção de filmes
- Cadastro/remoção de clientes
- Aluguéis e devoluções
- Data e hora de cada operação

## 🤝 Contribuindo

Contribuições são bem-vindas! Para contribuir:
1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request
