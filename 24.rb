filename = "24.sample"
filename = "24.input"

def and_func(x, y)
    (x == 1 && y == 1) ? 1 : 0
end

def or_func(x, y)
    (x == 1 || y == 1) ? 1 : 0
end

def xor_func(x, y)
    (x != y) ? 1 : 0
end

lines = File.readlines(filename, chomp:true).slice_before(&:empty?).to_a
setup, graph = lines[0], lines[1]
graph.shift

instructions = setup.map { |item| item.split(": ") }.to_h

compute_graph = {}
graph.each do |line|
    operation, key = line.split(" -> ")
    ops = operation.split(" ")
    compute_graph[key] = {
        "op" => ops[1],
        "x" => ops[0],
        "y" => ops[2]
    }
end

def compute(graph, cache, instructions, wire)
    return cache[wire] if cache.key?(wire)

    if instructions.key?(wire)
        val = instructions[wire].to_i
        cache[wire] = val
        return val
    end

    ops = graph[wire]
    op, x, y = ops["op"], ops["x"], ops["y"]

    x_val = compute(graph, cache, instructions, x)
    y_val = compute(graph, cache, instructions, y)

    case op
    when "AND"
        result = and_func(x_val, y_val)
    when "OR"
        result = or_func(x_val, y_val)
    when "XOR"
        result = xor_func(x_val, y_val)
    end

    cache[wire] = result
    return result
end

cache, zs = {}, {}
compute_graph.each do |k, v|
    if k.start_with?("z")
        zs[k] = compute(compute_graph, cache, instructions, k)
    end
end

bin = zs.sort_by { |k, v| k }.map { |k, v| v }.join("").reverse
pp bin.to_i(2)

def generate_dot_file(compute_graph, instructions, filename = "graph.dot")
  File.open(filename, "w") do |file|
    file.puts "digraph LogicGates {"
    file.puts "  rankdir=LR;"
    file.puts "  node [shape=box];"
    file.puts ""
    
    instructions.each do |wire, value|
      color = value.to_i == 1 ? "lightgreen" : "lightcoral"
      file.puts "  #{wire} [label=\"#{wire}\\n#{value}\", style=filled, fillcolor=#{color}];"
    end
    file.puts ""
    
    compute_graph.each do |output_wire, gate_info|
      op = gate_info["op"]
      x_wire = gate_info["x"]
      y_wire = gate_info["y"]
      gate_id = "gate_#{output_wire}"
      gate_color = case op
                   when "AND" then "lightblue"
                   when "OR" then "lightyellow"
                   when "XOR" then "lightpink"
                   else "white"
                   end
      file.puts "  #{gate_id} [label=\"#{op}\", shape=ellipse, style=filled, fillcolor=#{gate_color}];"
      file.puts "  #{x_wire} -> #{gate_id};"
      file.puts "  #{y_wire} -> #{gate_id};"
      output_color = output_wire.start_with?("z") ? "gold" : "white"
      file.puts "  #{output_wire} [style=filled, fillcolor=#{output_color}];"
      file.puts "  #{gate_id} -> #{output_wire};"
      file.puts ""
    end
    file.puts "}"
  end
end

# can generate by `dot -Tpng logic_circuit.dot -o test.png`
generate_dot_file(compute_graph, instructions, "logic_circuit.dot")