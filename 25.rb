filename = "25.sample"
filename = "25.input"

lines = File.readlines(filename, chomp:true)
groups = lines.slice_before("").reject { |g| g == [""] }.map do |group|
  group.reject(&:empty?)
end

locks, keys = [], []

groups.each do |group|
  pp group
  v, w, x, y, z = 0, 0, 0, 0, 0
  (1..5).each do |i|
    v += 1 if group[i][0] == "#"
    w += 1 if group[i][1] == "#"
    x += 1 if group[i][2] == "#"
    y += 1 if group[i][3] == "#"
    z += 1 if group[i][4] == "#"
  end
  if group[0] == "#####"
    locks.push([v, w, x, y, z])
  else
    keys.push([v, w, x, y, z])
  end
end

pp locks
pp keys

count = 0
keys.each do |key|
  locks.each do |lock|
    if key.zip(lock).all? { |a, b| a + b <= 5 }
      count += 1
    end
  end
end
pp count