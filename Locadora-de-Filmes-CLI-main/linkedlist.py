class Node:
    def __init__(self, data, prev = None, next = None):
        """
        Inicializa um nó da lista encadeada.

        Args:
            data: O dado que será armazenado no nó.
        """
        self.data = data
        self.next = next
        self.prev = prev

    def __repr__(self):
        """
        Retorna uma representação em string do nó.

        Returns:
            str: O dado armazenado no nó como string.
        """
        return str(self.data)

    def __eq__(self, other):
        """
        Compara dois nós para verificar se são iguais.

        Args:
            other (Node): O nó a ser comparado.

        Returns:
            bool: True se os dados dos nós forem iguais, False caso contrário.
        """
        if not isinstance(other, Node):
            return False

        return self.data == other.data


class DoublyLinkedList:
    def __init__(self, nodes: list = None):
        """
        Inicializa uma lista encadeada, opcionalmente com uma lista de dados.

        Args:
            nodes (list, opcional): Uma lista de dados para inicializar os nós da lista encadeada.
                                   Se fornecida, os nós serão criados e encadeados automaticamente.
        """
        self.head = None
        self.tail = None
        self.length = 0

        # Se a lista de nós for fornecida, cria os nós e os encadeia.
        if nodes:
            # Cria uma cópia da lista para não modificar a original
            nodes_copy = nodes.copy()
            # Cria o primeiro nó com o primeiro elemento da lista.
            node = Node(data=nodes_copy.pop(0))

            # Atribui o primeiro nó como head da lista.
            self.head = node
            self.length = 1

            # Cria os nós restantes e os encadeia.
            for element in nodes_copy:
                node.next = Node(data=element, prev=node)
                node = node.next
                self.length += 1
            
            self.tail = node

    def __iter__(self):
        """
        Permite a iteração sobre os nós da lista encadeada.

        Yields:
            Node: O nó atual da iteração.
        """
        node = self.head

        while node is not None:
            yield node
            node = node.next

    def __reversed__(self):
        node = self.tail

        while node is not None:
            yield node
            node = node.prev

    def __repr__(self):
        """
        Retorna uma representação em string da lista encadeada.

        Returns:
            str: Uma string que representa os elementos da lista encadeada
                 no formato 'dado1 -> dado2 -> ... -> None'.
        """
        node = self.head
        nodes = ["None"]

        while node is not None:
            nodes.append(node.data)
            node = node.next

        nodes.append("None")

        return " <-> ".join(nodes)

    def __contains__(self, target):
        for curr in self:
            if curr.data == target.data:
                return True
        return False
    
    def __len__(self):
        """Retorna o número de nós na lista."""
        return self.length
    
    def empty(self):
        """Verifica se a lista está vazia."""
        return self.length == 0
    
    def add_first(self, node: Node):
        node.prev = None
        node.next = self.head
        
        if self.head:
            self.head.prev = node
        
        self.head = node

        if not self.tail:
            self.tail = node

        self.length += 1

    def add_last(self, node: Node):
        # Se a lista estiver vazia, o nó se torna o head e tail.
        if self.head is None and self.tail is None:
            self.head = self.tail = node
            self.length = 1
            return

        node.prev = self.tail
        self.tail.next = node
        self.tail = node
        self.length += 1

    def add_after(self, node: Node, new_node: Node):
        """
        Adiciona um nó após um nó específico na lista encadeada.

        Args:
            node (Node): O nó após o qual o novo nó será adicionado.
            new_node (Node): O novo nó a ser adicionado.
        """
        # Se o head da lista for None, não há onde adicionar o novo nó.
        if self.head is None:
            raise Exception("A lista está vazia.")

        # Se o nó atual for None, não há onde adicionar o novo nó.
        if node is None:
            return
        
        if self.tail == node:
            return self.add_last(new_node)
        
        for current_node in self:
            if current_node == node:
                new_node.prev = current_node
                new_node.next = current_node.next

                current_node.next.prev = new_node
                current_node.next = new_node

                self.length += 1
                return

        # Se o nó não for encontrado na lista, levanta uma exceção.
        raise Exception(f"O nó {node} não foi encontrado na lista.")

    def add_before(self, node: Node, new_node: Node):
        """
        Adiciona um nó antes de um nó específico na lista encadeada.

        Args:
            node (Node): O nó antes do qual o novo nó será adicionado.
            new_node (Node): O novo nó a ser adicionado.
        """
        # Se o head da lista for None, não há onde adicionar o novo nó.
        if self.head is None:
            raise Exception("A lista está vazia.")

        # Se o nó atual for None, não há onde adicionar o novo nó.
        if node is None:
            return

        # Se o nó a ser adicionado for o head, adiciona-o no início da lista.
        if self.head == node:
            return self.add_first(new_node)
        
        # Percorre a lista encadeada para encontrar o nó antes do qual queremos adicionar o novo nó.
        for current_node in reversed(self):
            if current_node == node:
                new_node.next = current_node
                new_node.prev = current_node.prev

                current_node.prev.next = new_node
                current_node.prev = new_node
                self.length += 1
                return

        # Se o nó não for encontrado na lista, levanta uma exceção.
        raise Exception(f"O nó {node} não foi encontrado na lista.")

    def remove(self, node: Node):
        """
        Remove um nó específico da lista encadeada.

        Args:
            node (Node): O nó a ser removido.
        """
        # Se o head da lista for None, não há onde remover o nó.
        if self.head is None:
            raise Exception("A lista está vazia.")
        
        removido = False
        
        if self.head == node:
            if self.head == self.tail:
                self.head = None
                self.tail = None
            else:
                self.head = self.head.next
                self.head.prev = None
            removido = True
        elif self.tail == node:
            new_tail = self.tail.prev
            new_tail.next = None
            self.tail = new_tail
            removido = True
        else:
            for current_node in self:
                if current_node.next == node:
                    node_remove = current_node.next
                    current_node.next = node_remove.next

                    if node_remove.next is not None:
                        node_remove.next.prev = current_node
                    else:
                        self.tail = current_node
                    
                    removido = True
                    break

        if removido:
            # Limpa as referências do nó removido
            node.prev = None
            node.next = None
            self.length -= 1
        else:
            raise ValueError(f"O nó {node} não foi encontrado na lista.")

    def popleft(self):
        if self.head is None:
            raise Exception("A lista está vazia.")
        data = self.head.data
        self.remove(self.head)
        return data
    
    def pop(self):
        if self.tail is None:
            raise Exception("A lista está vazia.")

        data = self.tail.data
        self.remove(self.tail)
        return data