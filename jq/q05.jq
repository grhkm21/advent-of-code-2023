def strip:
    sub("^[\\n ]+"; "") | sub("[\\n ]+$"; "");

def parse_map:
    split(" ") | map(tonumber) | if length == 3 then
        { "dest": .[0], "src": .[1], "length": .[2] }
    else
        .[]
    end;

def parse_data:
    [inputs] | join("\n") | split("\n\n") | map(
        split(":").[1] | strip | split("\n") | map(parse_map)
    );

def part1:
    reduce .[1:][] as $map (.[0];
        map(. as $data | $map | map(
            $map
            | map(
                select(.src <= $data and $data < .src + .length) | .dest + $data - .src
              ) | .[]) + [$data]
            | .[0]
        )
    ) | min;

def part2:
    0;

parse_data | part1
