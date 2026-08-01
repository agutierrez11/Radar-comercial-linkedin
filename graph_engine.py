import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

try:
    import networkx as nx
except ImportError:
    print("Instalando networkx...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "networkx"])
    import networkx as nx

def build_relationship_graph(connections_file="enriched_connections.json"):
    if not os.path.exists(connections_file):
        print(f"Error: {connections_file} no encontrado.")
        return None, []
        
    with open(connections_file, "r", encoding="utf-8") as f:
        contacts = json.load(f)
        
    G = nx.Graph()
    user_node = "Usuario (Tú)"
    G.add_node(user_node, type="User", label=user_node)
    
    for c in contacts:
        name = c.get("full_name") or c.get("name")
        company = c.get("company", "Empresa No Especificada")
        position = c.get("position", "Cargo No Especificado")
        country = c.get("country", "Desconocido")
        hierarchy = c.get("hierarchy", "Otros")
        
        if not name:
            continue
            
        # Nodos
        G.add_node(name, type="Contact", company=company, position=position, country=country, hierarchy=hierarchy)
        if company != "Empresa No Especificada":
            G.add_node(company, type="Company")
            G.add_edge(name, company, relation="works_at")
            
        if country != "Desconocido":
            G.add_node(country, type="Country")
            G.add_edge(name, country, relation="located_in")
            
        # Conexión directa de 1er grado con el usuario
        weight = 1.0
        if hierarchy == "C-Level":
            weight = 0.5 # Menor distancia matemática (mayor valor)
        elif hierarchy == "Director":
            weight = 0.7
            
        G.add_edge(user_node, name, relation="connected_to", weight=weight)
        
    return G, contacts

def analyze_graph_intelligence(G):
    if not G:
        return {}
        
    total_nodes = G.number_of_nodes()
    total_edges = G.number_of_edges()
    
    # Centralidad de intermediación (Super-Conectores)
    betweenness = nx.betweenness_centrality(G)
    top_connectors = sorted(
        [(node, score) for node, score in betweenness.items() if G.nodes[node].get("type") == "Contact"],
        key=lambda x: x[1],
        reverse=True
    )[:10]
    
    # Empresas con mayor densidad de contactos
    companies = [n for n, d in G.nodes(data=True) if d.get("type") == "Company"]
    company_density = sorted(
        [(comp, G.degree(comp)) for comp in companies],
        key=lambda x: x[1],
        reverse=True
    )[:10]
    
    results = {
        "total_nodes": total_nodes,
        "total_edges": total_edges,
        "top_super_connectors": top_connectors,
        "top_companies_density": company_density
    }
    
    print("=== ANÁLISIS DE TEORÍA DE GRAFOS DE TU RED ===")
    print(f" Total Nodos en el Grafo: {total_nodes}")
    print(f"🔗 Total Aristas / Relaciones: {total_edges}")
    print("\n Top 5 Súper-Conectores en tu Red (Betweenness Centrality):")
    for name, score in top_connectors[:5]:
        comp = G.nodes[name].get('company', '')
        pos = G.nodes[name].get('position', '')
        print(f"  • {name} ({pos} @ {comp}) - Centralidad: {score:.4f}")
        
    print("\n Top 5 Empresas con Mayor Densidad de Contactos:")
    for comp, count in company_density[:5]:
        print(f"  • {comp}: {count} conexiones de 1er grado")
        
    return results

if __name__ == "__main__":
    G, contacts = build_relationship_graph()
    analyze_graph_intelligence(G)
