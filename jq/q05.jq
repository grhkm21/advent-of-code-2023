def strip:
    sub("^[\\n ]+"; "") | sub("[\\n ]+$"; "");

def parse_map:
    split(" ") | map(tonumber) | if length == 3 then
        { "dest": .[0], "src": .[1], "len": .[2] }
    else
        .[]
    end;

def parse_data:
    [inputs] | join("\n") | split("\n\n") | map(
        split(":").[1] | strip | split("\n") | map(parse_map)
    );

def group_pairs:
    [range(0; length; 2) as $i | { "start": .[$i], "end": (.[$i] + .[$i + 1] - 1) }];

def process_maps1($data; $maps):
    $maps | map(
        select(.src <= $data and $data < .src + .len) | .dest + $data - .src
    ) + [$data] | .[0];

def process_single_map2($state; $map):
    # Here $data ~ {"start": ..., "end": ...}
    # and $prev ~ [{"start": ..., "end": ...}, ...]
    # and $map ~ {"dest": ..., "src": ..., "len": ...}
    $state as [$data, $prev] | $map
    | if $data == null then
        [$data, $prev]
    elif .src <= $data.start and $data.start < .src + .len then
        if $data.end < .src + .len then
            [null,
             $prev + [{"start": (.dest + $data.start - .src), "end": (.dest + $data.end - .src) }]]
        else
            [{ "start": (.src + .len), "end": $data.end },
             $prev + [{ "start": (.dest + $data.start - .src), "end": (.dest + .len - 1) }]]
        end
    else
        [$data, $prev]
    end;

def init_state($data; $map):
    $map | if $data.start < .src then
        [{ "start": .src, "end": $data.end }, [{ "start": $data.start, "end": (.src - 1)}]]
    else
        [$data, []]
    end | .;

def process_maps2($data; $maps):
    $maps | sort_by(.src) |
    reduce .[] as $map (init_state($data; .[0]); process_single_map2(.; $map))
    | if .[0] == null then .[1][] else .[0] + .[1][] end;

def part1:
    reduce .[1:][] as $maps (.[0]; map(process_maps1(.; $maps))) | min;

def part2:
    reduce .[1:][] as $maps (.[0] | group_pairs; map(process_maps2(.; $maps)))
    | min_by(.start).start;

parse_data | {"part1": part1, "part2": part2}
