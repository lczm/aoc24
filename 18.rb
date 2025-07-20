filename = "18.sample"
filename = "18.input"

gx, gy = filename == "18.input" ? [70, 70] : [6, 6]

coordinates = Array.new
File.foreach(filename, chomp: true) do |line|
  xs, ys = line.split(",")
  x = xs.to_i
  y = ys.to_i
  coordinates.push([x, y])
end

grid = Array.new(gy + 1) { Array.new(gx + 1, 0) }
coordinates.first(1024).each do |x, y|
  grid[y][x] = 1
end

def print_grid(grid)
  grid.each do |row|
    line = row.map { |cell| cell == 0 ? "." : "#"}.join
    puts line
  end
end

def dijkstra(grid)
  rows = grid.size
  cols = grid[0].size

  distances = Array.new(rows) { Array.new(cols, Float::INFINITY) }
  visited = Array.new(rows) { Array.new(cols, false) }
  # starting position
  distances[0][0] = 0
  
  loop do 
    # pick unvisited node with smallest distance
    min_dist = Float::INFINITY
    min_node = nil
    rows.times do |y|
      cols.times do |x|
        if !visited[y][x] && distances[y][x] < min_dist
          min_dist = distances[y][x]
          min_node = [x, y]
        end
      end
    end
    
    # no more nodes
    break if min_node.nil?

    x, y = min_node
    break if x == cols - 1 && y == rows - 1
    visited[y][x] = true

    [[1,0],[-1,0],[0,1],[0,-1]].each do |dx, dy|
      nx, ny = x + dx, y + dy
      next if nx < 0 || nx >= cols || ny < 0 || ny >= rows
      next if visited[ny][nx]
      next if grid[ny][nx] == 1

      alt = distances[y][x] + 1
      if alt < distances[ny][nx]
        distances[ny][nx] = alt
      end
    end
  end

  result = distances[rows-1][cols-1]
  result.infinite? ? nil : result
end

# part 1
p dijkstra(grid)

# part 2
low = 1024
high = coordinates.size
answer = nil
while low <= high
  mid = (low + high) / 2
  p mid

  grid = Array.new(gy + 1) { Array.new(gx + 1, 0) }
  coordinates.first(mid).each do |x, y|
    grid[y][x] = 1
  end

  steps = dijkstra(grid)
  if steps
    low = mid + 1
  else
    answer = mid
    high = mid - 1
  end
end
p answer
p coordinates[answer - 1]

