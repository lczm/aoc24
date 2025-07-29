filename = "23.sample"
filename = "23.input"

class Graph
  def initialize
    @adj = Hash.new { |h, node| h[node] = [] }
  end

  def add_edge(u, v)
    @adj[u] << v
    @adj[v] << u
  end

  def neighbours(node)
    @adj[node]
  end

  def nodes
    @adj.keys
  end
end

graph = Graph.new
lines = File.readlines(filename, chomp:true)
connections = lines.map { |line| a, b = line.split('-', 2) }
connections.each do |connection| 
  graph.add_edge(connection[0], connection[1])
end

triplets = graph.nodes.flat_map do |node|
  graph.neighbours(node)
       .combination(2)
       .select { |u, v| graph.neighbours(u).include?(v) }
       .map { |u, v| [node, u, v].sort }
       .select { |arr| arr.any? { |elem| elem.start_with?("t")} }
end.uniq

pp triplets 
pp triplets.length

# https://en.wikipedia.org/wiki/Bron%E2%80%93Kerbosch_algorithm
def bron_kerbosch_pivot(r, p, x, graph, cliques)
  if p.empty? && x.empty?
    cliques << r.dup
  else
    ux = (p + x).to_set
    u  = ux.max_by { |node| (graph.neighbours(node).to_set & p).size }
    (p - graph.neighbours(u).to_set).each do |v|
      nbrs_v = graph.neighbours(v).to_set
      bron_kerbosch_pivot(
        r + [v],   
        p & nbrs_v,
        x & nbrs_v,
        graph,
        cliques
      )
      p.delete(v)
      x.add(v)
    end
  end
end

def max_clique(graph)
  cliques = []
  bron_kerbosch_pivot([], graph.nodes.to_set, Set.new, graph, cliques)
  cliques.max_by(&:size)
end

p max_clique(graph).sort.join(",")