import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

def find_cycles(G):
    return list(nx.cycle_basis(G))

def save_graph(G, data, file_name):
    plt.figure()
    edge_labels = dict([((u,v),d[data]) for u,v,d in G.edges(data=True)])
    pos=nx.spring_layout(G)
    nx.draw_networkx_edge_labels(G, pos=pos, edge_labels=edge_labels)
    nx.draw(G, pos=pos, with_labels=True)
    plt.savefig(file_name)

def print_graph(G, data):
    edge_labels = dict([((u,v),d[data]) for u,v,d in G.edges(data=True)])
    pos=nx.spring_layout(G)
    nx.draw_networkx_edge_labels(G, pos=pos, edge_labels=edge_labels)
    nx.draw(G, pos=pos, with_labels=True)
    plt.show()

def create_equasions(G, SEM):
    '''
    Creates system of eqasions from Kirhcoff laws
    Returns tuple of arrays representing equasions
    '''
    
    def get_edges_from_cycle(cycle):
        '''Returns list of edges from list of nodes (forming a cycle)'''
        edges = list()
        for i in range(len(cycle) - 1):
            edges.append((cycle[i], cycle[i+1]))
        edges.append((cycle[-1], cycle[0]))
        return edges
        
    def against_current(u,v):
        '''
        Program is assuming that current goes as tuples returned from Graph.edges()
        For example in edge (3,5) current goes 3 --> 5
        This function checks if edge (u,v) is against this current
        '''
        for a,b in G.edges():
            if a == v and b == u:
                return True
        return False
        
    
    cycles = find_cycles(G)
    edge_nums = dict([(frozenset(edge), idx) for idx, edge in enumerate(G.edges)])      # each edge (as frozenset) gets number (starting at 0)
    size = len(edge_nums)

    A = np.zeros((size, size))
    B = np.zeros(size)

    i = 0
    for cycle in cycles:
        for edge in get_edges_from_cycle(cycle):
            A[i][edge_nums[frozenset(edge)]] = G[edge[0]][edge[1]]['R']

            if against_current(edge[0],edge[1]):
                A[i][edge_nums[frozenset(edge)]] = -A[i][edge_nums[frozenset(edge)]]

            for u, v, E in SEM:
                if (u,v) == edge or (v,u) == edge:
                    if against_current(u,v):
                        B[i] += -E
                    else:
                        B[i] += E

        i += 1

    for node in G.nodes():
        edges_from_node = [(node, neighbor) for neighbor in G.neighbors(node)]
        for edge in edges_from_node:
            A[i][edge_nums[frozenset(edge)]] = 1

            if against_current(edge[0],edge[1]):
                A[i][edge_nums[frozenset(edge)]] = -1
        
        i += 1
        if(i == size):
            break

    return((A,B))
        
def produce_output_graph(G, X):
    '''Based on input graph and solution of system of equasions returns graph representing electric current'''
    DG = nx.DiGraph()
    for (u,v),I in zip(G.edges(), X):
        if I > 0:
            DG.add_edge(u, v, I=format(I, '.2f'))
        else:
            DG.add_edge(v, u, I=format(abs(I), '.2f'))
    return DG

def solve_eq(A, B):
    return solve_Gauss(A, B)

def solve_Gauss(A, B):
    size = A.shape[0]
    B.shape = (-1,1)
    AB = np.concatenate((A, B), axis = 1)

    for i in range(size - 1):
        pivot = np.argmax(A[i:,i]) + i
        if pivot != i:
            AB[[i,pivot],:] = AB[[pivot,i],:]
        
        for j in range(i + 1, size):
            AB[j,:] -= AB[i,:] * (AB[j,i] / AB[i,i])


    A = AB[:,:-1]
    B = AB[:,-1]

    X = np.copy(B)

    for i in range(size - 1, -1, -1):
        for j in range(i + 1, size):
            X[i] -= A[i][j] * X[j]
        X[i] /= A[i][i]

    return X

# ------------------------------------------------------------------------------------------------------
def use_Kirchhoff_laws(G, SEM):
    A, B = create_equasions(G, SEM)
    X = solve_eq(A, B)
    G = produce_output_graph(G, X)
    return G

def example_graph():
    G = nx.Graph()
    G.add_edge(1, 2, R=20)
    G.add_edge(1, 4, R=5)
    G.add_edge(1, 3, R=10)
    G.add_edge(4, 2, R=10)
    G.add_edge(2, 3, R=15)
    return G

def main():
    G = example_graph()
    SEM = [(2,4,20)]
    
    save_graph(G, 'R', 'input_circut.png')
    G = use_Kirchhoff_laws(G, SEM)
    save_graph(G, 'I', 'output_circut.png')

if __name__ == "__main__":
    main()
