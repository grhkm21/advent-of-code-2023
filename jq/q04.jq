def parse_data:
    inputs / ": "
    | .[1] / " | "
    | map(. / " " | map(select(. != "") | tonumber))
    | . as [$win, $cards]
    | $cards - ($cards - $win)
    | length;

def part1:
    map(exp2 / 2 | floor) | add;

def part2:
    [.[] | [1, .]] | recurse(.[1:][:.[0][1]][][0] += .[0][0] | .[1:]; length > 0)[0][0];

[parse_data] | {"part1": part1, "part2": [part2] | add}
