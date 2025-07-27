filename = "21.input"
filename = "21.sample"

lines = File.readlines(filename, chomp:true)
p lines

numeric_keypad =   
  ['7','8','9'],
  ['4','5','6'],
  ['1','2','3'],
  [' ','0','A']

directional_keypad =
  [' ','^','A'],
  ['<','v','>']

NUMERIC_POSITIONS = {}
numeric_keypad.each_with_index do |row, i|
  row.each_with_index do |val, j|
    NUMERIC_POSITIONS[val] = [i, j] unless val == ' '
  end
end

DIRECTIONAL_POSITIONS = {}
directional_keypad.each_with_index do |row, i|
  row.each_with_index do |val, j|
    DIRECTIONAL_POSITIONS[val] = [i, j] unless val == ' '
  end
end

DELTAS = {
  [-1,  0] => '^',
  [ 1,  0] => 'v',
  [ 0, -1] => '<',
  [ 0,  1] => '>' 
}

BFS_CACHE = {}
def bfs(start_val, dest_val, start_positions, dest_positions, grid)
  cache_key = [start_val, dest_val, start_positions.object_id, dest_positions.object_id, grid.object_id]
  return BFS_CACHE[cache_key] if BFS_CACHE.key?(cache_key)

  start = start_positions[start_val]
  dest = dest_positions[dest_val]

  result = if start == dest
    ["A"]
  else
    queue = [start]
    parent = { start => [] }
    distance = { start => 0 }

    head = 0
    until queue.empty?
      current = queue.shift

      if distance.key?(dest) && distance[current] >= distance[dest]
        next
      end

      DELTAS.each do |(di, dj), action|
        ni, nj = current[0] + di, current[1] + dj
        next unless ni.between?(0, grid.size - 1) && nj.between?(0, grid[0].size-1)
        next if grid[ni][nj] == ' '

        neighbour = [ni, nj]
        new_dist = distance[current] + 1

        if !distance.key?(neighbour)
          distance[neighbour] = new_dist
          parent[neighbour] = [[current, action]]
          queue << neighbour
        elsif distance[neighbour] == new_dist
          parent[neighbour] << [current, action]
        end
      end
    end

    if !parent.key?(dest)
      []
    else
      # Reconstruct all shortest paths
      paths = []
      q = [[dest, ""]] # [[node, path_str]]

      until q.empty?
        curr_node, curr_path_str = q.shift

        if curr_node == start
          paths << curr_path_str.reverse
          next
        end

        if parent.key?(curr_node)
          parent[curr_node].each do |prev, action|
            q << [prev, curr_path_str + action]
          end
        end
      end

      paths.map { |p| p + 'A' }
    end
  end

  BFS_CACHE[cache_key] = result
  result
end

def apply(steps, pos_x, pos_y, grid)
  steps.prepend("A")
  pos = steps
    .chars
    .each_cons(2)
    .map(&:join)  

  all = []
  pos.each do |p|
    all.push(bfs(p[0], p[1], pos_x, pos_y, grid))
  end

  first, *rest = all
  first.product(*rest).map(&:join)
end

sum = 0
lines.each do |line|
  result = apply(line, NUMERIC_POSITIONS, NUMERIC_POSITIONS, numeric_keypad)
  2.times do
    result = result.map do |each|
      apply(each, DIRECTIONAL_POSITIONS, DIRECTIONAL_POSITIONS, directional_keypad)
    end.flatten
  end

  shortest = result.min_by(&:length)
  sum += (shortest.length * line[1..-2].to_i)
end

pp sum

# pp bfs("A", "A", NUMERIC_POSITIONS, NUMERIC_POSITIONS, numeric_keypad)
# pp bfs(">", ">", DIRECTIONAL_POSITIONS, DIRECTIONAL_POSITIONS, directional_keypad)
# pp bfs(">", ">", DIRECTIONAL_POSITIONS, DIRECTIONAL_POSITIONS, directional_keypad)
# pp bfs("A", "^", DIRECTIONAL_POSITIONS, DIRECTIONAL_POSITIONS, directional_keypad)
# pp bfs("2", "9", NUMERIC_POSITIONS, NUMERIC_POSITIONS, numeric_keypad)