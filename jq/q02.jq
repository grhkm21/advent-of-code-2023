def part1_threshold:
    {"red": 12, "green": 13, "blue": 14};

# 5 green, 6 red -> {"green": 5, "red": 6}
def extract_data:
    split(", ") | map(split(" ") | {"key": .[1], "value": .[0] | tonumber}) | from_entries;

def process_data:
    split("; ") | map(extract_data);

# [{"green": 3}, {"green": 5}] -> {"green": 5}
def max_data:
    map(to_entries) | flatten | group_by(.key) | map([(map(.key).[0]), (map(.value) | max)])
    | map({"key": .[0], "value": .[1]}) | from_entries;

def part1_check_data:
    to_entries | map(.value <= part1_threshold[.key]) | all;

def part2_compute_data:
    to_entries | map(.value) | reduce .[] as $val (1; . * $val);

def part1:
    map(split(": ") as [$id, $data] | [
        $id | split(" ").[1] | tonumber,
        ($data | process_data | max_data)
    ] | select(.[1] | part1_check_data) | .[0]) | add;

def part2:
    map(split(": ").[1] | process_data | max_data | part2_compute_data) | add;

[inputs] | {"part1": part1, "part2": part2}
