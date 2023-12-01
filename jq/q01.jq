def words:
    ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
     "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"];

def get_pos($in) :
    [ words, [range(20)] ] | transpose # enumerate(words)
    | [ .[] as [$pat, $idx] | $in | ([index($pat), $idx % 10], [rindex($pat), $idx % 10]) ];

def part2_line:
    get_pos(.) | [.[] | select(.[0] != null)] | sort | map(.[1] | tostring);

def part1:
    [ .[] | [match("\\d"; "g").string] | .[0] + .[-1] | tonumber ] | add;

def part2:
    [ .[] | part2_line | .[0] + .[-1] | tonumber ] | add;

[inputs] | ["part1: " + (part1 | tostring), "part2: " + (part2 | tostring)]
