filename = "22.sample"
filename = "22.input"

lines = File.readlines(filename, chomp:true).map(&:to_i)
pp lines

def mix(n, v)
  n ^ v
end

def prune(n)
  n % 16777216
end

def process(n)
  n1 = n * 64
  n = mix(n1, n)
  n = prune(n)

  n2 = n / 32
  n = mix(n2, n)
  n = prune(n)

  n3 = n * 2048
  n = mix(n3, n)
  n = prune(n)
end

def n_times(n)
  last = Array.new()
  last << n % 10
  (0..1999).each do |i|
    n = process(n)
    last << n % 10
  end
  last
end
# pp lines.map { |line| n_times(line) }.sum

def sequence(n)
  x = n_times(n)
  y = x.each_cons(2).map do |prev, curr|
    curr - prev
  end
  map = {}
  y.each_cons(4).with_index.map do |tuple, idx|
    map[tuple] ||= x[idx+4]
  end
  map
end

def query(map, k)
  map.fetch(k, 0)
end

all = lines.map { |line| sequence(line) }
keys = all.map { |each| each.keys }.flatten(1).to_set.to_a

maximum = 0
freq = Hash.new(0)
keys.each do |key|
 freq[key] = all.map{ |map| query(map, key) }.sum
end

p freq.max_by { |key, val| val }