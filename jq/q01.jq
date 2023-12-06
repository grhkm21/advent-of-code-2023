def words:
    ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
     "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"];

def get_pos($in) :
    [ words, [range(20)] ] | transpose
    | [ .[] as [$pat, $idx] | $in | ([index($pat), $idx % 10], [rindex($pat), $idx % 10]) ];

def part2_line:
    get_pos(.) | map(select(.[0] != null)) | sort | map(.[1] | tostring);

def part1:
    map([match("\\d"; "g").string] | .[0] + .[-1] | tonumber) | add;

def part2:
    map(part2_line | .[0] + .[-1] | tonumber) | add;

[inputs] | {"part1": part1, "part2": part2}
