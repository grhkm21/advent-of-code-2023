def parse_data:
    [inputs/" " | .[1] |= tonumber];

def get_val1:
    map({"A": 14, "K": 13, "Q": 12, "J": 11, "T": 10}[.] // tonumber);

def get_val2:
    map({"A": 14, "K": 13, "Q": 12, "T": 11, "J" : 1}[.] // tonumber);

def get_key1:
    .[0] |= (./"" | [(group_by(.) | map(length) | sort | reverse), get_val1]);

def get_type2:
    group_by(.)
    | map({(.[0]): length})
    | add
    | .J as $J
    | [del(.J)[]]
    | sort
    | reverse
    | .[0] += $J;

def get_key2:
    .[0] |= (./"" | [get_type2, get_val2]);

def part1:
    map(get_key1) | sort | to_entries | map((.key + 1) * .value[-1]) | add;

def part2:
    map(get_key2) | sort | to_entries | map((.key + 1) * .value[-1]) | add;

parse_data | {"part1": part1, "part2": part2}
