def strip:
    sub("^[\\n ]+"; "") | sub("[\\n ]+$"; "");

def parse_data:
    [inputs] | map(split(":").[1] | strip);

def solve_pair:
    # Want x^2 - tx + d < 0 -> x >= (y := floor((t - sqrt(t^2 - 4d)) / 2) + 1)
    # By symmetry, answer is t + 1 - 2y
    . as [$t, $d] | ($t - ($t * $t - 4 * $d | sqrt)) / 2 + 1 | floor | $t + 1 - 2 * .;
    # . as [$t, $d] | [range($t + 1) | select(. * ($t - .) > $d)] | length;

def part1:
    map(split(" ") | map(select(. != "") | tonumber)) | transpose | map(solve_pair)
    | reduce .[] as $a (1; . * $a);

def part2:
    map(gsub(" "; "") | tonumber) | solve_pair;

parse_data | {"part1": part1, "part2": part2}
