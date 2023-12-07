def parse_data:
    [inputs] | map(split(""));

def is_digit:
    ("0" <= .) and (. <= "9");

def is_symbol:
    (is_digit | not) and (. != ".");

# Only [0, $x), [0, $y) supported
def range2d($x; $y):
    range($x) | . as $i | range($y) | [$i, .];

def range2d($x0; $x1; $y0; $y1):
    range($x0; $x1) | . as $i | range($y0; $y1) | [$i, .];

def adj8($x; $y):
    range2d($x - 1; $x + 2; $y - 1; $y + 2) | select(. != [$x, $y]);

def adj8:
    adj8(.[0]; .[1]);

def group_consecutive_by(f):
    reduce .[] as $val (null ;
        if (. == null) then
            .cur = [$val]
        elif (($val | f) == (.cur[-1] | f) + 1) then
            .cur += [$val]
        else
            .result += [.cur] | .cur = [$val]
        end
    )
    | .result + [.cur];

def find_filtered(filter_fn):
    . as $data
    | [length, .[0] | length] as [$r, $c]
    | range2d($r; $c)
    | select($data[.[0]][.[1]] | filter_fn);

def adj_symbols:
    [length, .[0] | length] as [$r, $c]
    | find_filtered(is_symbol)
    | adj8;

def find_nums:
    [find_filtered(is_digit)]
    | group_consecutive_by(if . == null then -1 else .[0] * 10000 + .[1] end)
    | .[];

def part1:
    . as $data
    | [adj_symbols] as $symbols
    | find_nums
    | select($symbols - . != $symbols)
    | map($data[.[0]][.[1]])
    | join("")
    | tonumber;

def part2:
    error("not implemented; see q03.jq";

parse_data | [part1] | add
# parse_data | {"part1": [part1] | add, "part2": part2}
