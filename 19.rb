filename = "19.sample"
filename = "19.input"

patterns, designs = File.read(filename).split(/\n\s*\n/, 2)
patterns = patterns.split(",").map(&:strip)
designs = designs.lines.map(&:chomp)

def form(patterns, design)
  n = design.length
  dp = Array.new(n+1, 0)
  dp[0] = 1

  (0..n).each do |i|
    next unless dp[i]
    patterns.each do |p|
      if design[i, p.length] == p
        dp[i + p.length] += dp[i]
      end
    end
  end

  dp[n]
end

# part 1
p designs
  .map { |d| form(patterns, d) > 0 ? 1 : 0 }
  .reduce(0, :+)
# part 2
p designs
  .map { |d| form(patterns, d) }
  .reduce(0, :+)
