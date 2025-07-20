require "set"

filename = "20.sample"
filename = "20.input"

lines = File.foreach(filename, chomp: true)
grid = lines.map { |line| line.chars }

height, width = grid.size, grid[0].size
start = dest = nil
grid.each_with_index do |row, y|
  row.each_with_index do |cell, x|
    start = [y, x] if cell == "S"
    dest = [y, x] if cell == "E"
  end
end

seen = Set.new([start])
next_point = ->(point)do
  [[1,0],[-1,0],[0,1],[0,-1]].each do |dx, dy|
    y, x = point
    ny, nx = y + dy, x + dx
    next if ny < 0 || ny >= height || nx < 0 || nx >= width
    candidate = [ny, nx]
    next if seen.include?(candidate)

    if grid[ny][nx] == "." || grid[ny][nx] == "E"
      seen << candidate
      return candidate
    end
  end
  nil
end

current = start
points = [start]
while (np = next_point.call(current))
  points << np
  current = np
end

values = points
  .each_with_index
  .map { |pt, idx| [pt, idx] }
  .to_h
values[start] = 0

def flower(point, height, width)
  y, x = point
  coords = (-20..20).flat_map do |dy|
    dx_range = (-(20 - dy.abs)..(20 - dy.abs))
    dx_range.map { |dx| [y + dy, x + dx] }
  end
  coords.select { |y, x| y.between?(0, height - 1) && x.between?(0, width-1) }
end

cheats = Array.new()
# next_point_cheat = ->(point)do
#   y, x = point
#   return nil if point == dest
#   [[1,0],[-1,0],[0,1],[0,-1]].each do |dx, dy|
#     wy, wx = y + dy, x + dx
#     next if wy < 0 || wy >= height  || wx < 0 || wx >= width
#     next unless grid[wy][wx] == "#"     # must be a wall
#
#     ty, tx = wy + dy, wx + dx
#     next if ty < 0 || ty >= height  || tx < 0 || tx >= width
#     next unless grid[ty][tx] == "." || grid[ty][tx] == "E"
#
#     diff  = values[[ty,tx]] - values[[y,x]]
#     saved = diff - 2
#     cheats << saved if saved > 0
#   end
#   nil
# end

next_point_cheat = ->(point)do
  y, x = point
  return nil if point == dest
  reachable = flower(point, height, width)
  reachable.each do |ry, rx|
    next unless grid[ry][rx] == "." || grid[ry][rx] == "E"
    diff = values[[ry, rx]] - values[[y, x]]
    cost = (ry - y).abs + (rx - x).abs
    saved = diff - cost
    cheats << saved if saved > 0
  end
  nil
end

points.each do |p|
  next_point_cheat.call(p) 
end

# pp cheats.tally
freq = cheats.tally.filter {
  |k, v| k >= 100
}
pp freq
p freq.values.sum
