filename = "21.sample"
filename = "21.input"

lines = File.readlines(filename, chomp:true)
p lines

NUMERIC_POSITIONS = {
  '7' => [0, 0], '8' => [0, 1], '9' => [0, 2],
  '4' => [1, 0], '5' => [1, 1], '6' => [1, 2],
  '1' => [2, 0], '2' => [2, 1], '3' => [2, 2],
                 '0' => [3, 1], 'A' => [3, 2]
}

DIRECTIONAL_POSITIONS = {
                 '^' => [0, 1], 'A' => [0, 2],
  '<' => [1, 0], 'v' => [1, 1], '>' => [1, 2]
}

GREEDY_CACHE = {}
DEPTH_CACHE = {}

def greedy_path(start_val, dest_val, positions, is_numeric_keypad)
  cache_key = [start_val, dest_val, is_numeric_keypad]
  return GREEDY_CACHE[cache_key] if GREEDY_CACHE.key?(cache_key)

  start = positions[start_val]
  dest = positions[dest_val]

  result = if start == dest
    "A"
  else
    start_row, start_col = start
    dest_row, dest_col = dest
    
    row_diff = dest_row - start_row
    col_diff = dest_col - start_col
    
    updo = if row_diff > 0
      'v' * row_diff
    elsif row_diff < 0
      '^' * (-row_diff)
    else
      ''
    end
    
    leri = if col_diff > 0
      '>' * col_diff
    elsif col_diff < 0
      '<' * (-col_diff)
    else
      ''
    end
    
    if updo.empty?
      leri + 'A'
    elsif leri.empty?
      updo + 'A'
    else
      path = if is_numeric_keypad
        apply_numeric_heuristics(start_row, start_col, dest_row, dest_col, updo, leri)
      else
        apply_directional_heuristics(start_row, start_col, dest_row, dest_col, updo, leri)
      end
      path + 'A'
    end
  end

  GREEDY_CACHE[cache_key] = result
  result
end

def get_sequence_length_at_depth(sequence, depth)
  return sequence.length if depth == 0
  
  cache_key = [sequence, depth]
  return DEPTH_CACHE[cache_key] if DEPTH_CACHE.key?(cache_key)
  
  sequence_with_start = "A" + sequence
  pairs = sequence_with_start
    .chars
    .each_cons(2)
    .map(&:join)
  
  total_length = 0
  pairs.each do |pair|
    path = greedy_path(pair[0], pair[1], DIRECTIONAL_POSITIONS, false)
    total_length += get_sequence_length_at_depth(path, depth - 1)
  end
  
  DEPTH_CACHE[cache_key] = total_length
  total_length
end

def apply_numeric_heuristics(start_row, start_col, dest_row, dest_col, updo, leri)
  # If you are on the bottom row (row 3) and going to the left column (col 0) -> updo + leri
  if start_row == 3 && dest_col == 0
    return updo + leri
  end
  
  # If you are in the far-left column (col 0) and travelling to the bottom row (row 3) -> leri + updo
  if start_col == 0 && dest_row == 3
    return leri + updo
  end
  apply_general_heuristics(start_row, start_col, dest_row, dest_col, updo, leri)
end

def apply_directional_heuristics(start_row, start_col, dest_row, dest_col, updo, leri)
  # If you are starting on the farthest left column (col 0, the "<" key) -> leri + updo
  if start_col == 0
    return leri + updo
  end
  
  # If you are traveling to the farthest left column (col 0, the "<" key) -> updo + leri
  if dest_col == 0
    return updo + leri
  end
  apply_general_heuristics(start_row, start_col, dest_row, dest_col, updo, leri)
end

def apply_general_heuristics(start_row, start_col, dest_row, dest_col, updo, leri)
  up_movement = dest_row < start_row  
  left_movement = dest_col < start_col 
  
  case [up_movement, left_movement]
  when [true, true]
    leri + updo
  when [false, true]
    leri + updo
  when [false, false]
    updo + leri
  when [true, false]
    updo + leri
  end
end

def get_initial_sequence(steps, positions, is_numeric_keypad)
  steps.prepend("A")
  pos = steps
    .chars
    .each_cons(2)
    .map(&:join)  

  result = ""
  pos.each do |p|
    result += greedy_path(p[0], p[1], positions, is_numeric_keypad)
  end

  result
end

sum = 0
lines.each do |line|
  # First level: numeric keypad - get the initial sequence
  result = get_initial_sequence(line, NUMERIC_POSITIONS, true)
  
  # Calculate the final length after 25 levels of directional keypads
  total_length = get_sequence_length_at_depth(result, 25)
  sum += (total_length * line[1..-2].to_i)
end

pp sum