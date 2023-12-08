def words:
    ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
     "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"];

def get_pos:
    (words[:10] | join("|")) as $pat
    | match("^.*?([0-9]|\($pat))(.*([0-9]|\($pat)))?.*$")
    | [.captures[0].string, .captures[-1].string]
    | map(. as $in | words | index([$in]) | select(.) % 10);

def part1:
    map([scan("\\d"; "g")] | first + last | tonumber) | add;

def part2:
    map(get_pos | first * 10 + last) | add;

[inputs] | {"part1": part1, "part2": part2}
