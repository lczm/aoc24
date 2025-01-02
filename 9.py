from pprint import pprint
from typing import List, Tuple, Literal
from itertools import batched, chain
from dataclasses import dataclass

def build(diskmap) -> List:
    sequence = []
    index = 0
    for i, item in enumerate(diskmap):
        if i % 2 == 0:
            for _ in range(int(item)):
                sequence.append(index)
            index += 1
        else:
            for _ in range(int(item)):
                sequence.append('.')
    return sequence

@dataclass
class Item:
    type: Literal["file", "gap"]
    size: int
    id_: int = 0

def parse_ints(l):
    return [int(i) for i in l]

def solve1(filename):
    with open(filename, 'r') as file:
        diskmap = file.readline()
        sequence1 = build(diskmap)
        for i, item in enumerate(sequence1):
            if item == '.':
                left_ptr = i
                break
        right_ptr = len(sequence1) - 1
        while not type(sequence1[right_ptr]) == int:
            right_ptr -= 1
        while left_ptr < right_ptr:
            sequence1[left_ptr], sequence1[right_ptr] = sequence1[right_ptr], sequence1[left_ptr]
            while sequence1[left_ptr] != '.':
                left_ptr += 1
            while not type(sequence1[right_ptr]) == int:
                right_ptr -= 1
        count = 0
        for i, item in enumerate(sequence1):
            if item == '.':
                break
            count += i * int(item)
        print(count)

def expand(i: Item):
    return [i.id_] * i.size

def solve2(filename):
    with open(filename, 'r') as file:
        diskmap = file.readline()
        # Build disk map
        disk: List[Item] = []
        for file_id, (file_size, gap_size) in enumerate(
            batched(parse_ints(diskmap + "0"), 2)
        ):
            disk.append(Item("file", id_=file_id, size=file_size))
            disk.append(Item("gap", gap_size))

        reader = len(disk) - 1
        for file_id in range(disk[-2].id_, -1, -1):
            while (f := disk[reader]).type != "file" or f.id_ != file_id:
                reader -= 1
            try:
                writer, g = next(
                    (writer, g)
                    for writer, g in enumerate(disk)
                    if g.type == "gap" and g.size >= f.size
                )
            except StopIteration:
                continue
            if writer > reader:
                continue
        
            disk[reader] = Item("gap", f.size)
            disk.insert(writer, f)
            g.size -= f.size

        print(sum(idx * i for idx, i in enumerate(chain.from_iterable(map(expand, disk)))))

# solve1('9.sample')
# solve1('9.input')
solve2('9.sample')
solve2('9.input')
