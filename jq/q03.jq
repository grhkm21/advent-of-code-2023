def parse_data:
    [""] + [inputs | "." + . + "."] + [""];

def group3:
    range(length - 2) as $i | [.[$i], .[$i + 1], .[$i + 2]];

def part1:
    group3 as $group
    | $group[1]
    | match("\\d+"; "g")
    | select([$group[][.offset - 1 : .offset + .length + 1] | test("[^\\d|.]+")] | any)
    | .string
    | tonumber;

def part2_data:
    group3 as $group
    | $group[1]
    | match("\\d+"; "g")
    | .row = $group[]
    | .star = (.row[.offset - 1 : .offset + .length + 1] | match("\\*"))
    | .star.offset += .offset;

def part2:
    [part2_data]
    | group_by(.row, .star.offset)[]
    | select(length == 2)
    | map(.string | tonumber)
    | .[0] * .[1];

parse_data | {"part1": [part1] | add, "part2": [part2] | add}
