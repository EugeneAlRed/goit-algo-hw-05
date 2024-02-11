from collections import defaultdict
import sys
import re


def parse_log_line(line):
    if not re.match(r'(\d{4}(?:-\d{2}){2} \d{2}(?::\d{2}){2}) (\w+) (.*)', line):
        return None
    date, time, level, *message = line.split(' ')
    return {'date': date, 'time': time, 'level': level, 'message': ' '.join(message)}


def load_logs(file_path):
    with open(file_path, 'r+') as logfile:
        lines = list(filter(lambda x: x is not None,
                     (map(parse_log_line, logfile.readlines()))))
    return lines


def filter_logs_by_level(logs, level):
    return list(filter(lambda x: x['level'] == level, logs))


def count_logs_by_level(logs):
    count_dict = defaultdict()
    count_dict.default_factory = int
    for log in logs:
        count_dict[log['level']] += 1
    return dict(count_dict)


def display_log_counts(counts):
    print(f"\n{'Рівень логування':20}| Кількість ")
    print(f"{'-'*20}|{'-'*10}")
    print('\n'.join(list(map(lambda x: f'{x:20}| {counts[x]}', counts))))


if __name__ == '__main__':
    file_name = sys.argv[1]
    logs = load_logs(file_name)
    display_log_counts(count_logs_by_level(logs))
    if len(sys.argv) == 3:
        level = sys.argv[2]
        logs = filter_logs_by_level(logs, level)
        print(f'\nДеталі логів для рівня "{level}"')
        print(
            ''.join(map(lambda x: f"{x['date']} {x ['time'] } - {x['message']}", logs)))
