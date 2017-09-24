#!/usr/bin/env python3
import csv
from datetime import timedelta
from dateutil.parser import parse


duration2question_time = {
    50: 5,
    40: 5,
    25: 4,
    15: 3,
    2: 0,
}

minute = timedelta(minutes=1)


def calculate_duration_questions(row):
    title, speaker, start, end = row
    start, end = (parse(i) for i in (start, end))
    duration = end - start
    duration_m = duration // minute
    questions = duration2question_time[duration_m]
    duration = duration_m - questions
    row = [title, speaker, duration]
    rowq = [title, 'Questions to ' + speaker, questions]
    if questions > 0:
        return row, rowq
    else:
        return [row]


def convert2question_time(input_f, output_f):
    with open(input_f, newline='') as inf, open(output_f, 'w', newline='') as outf:
        reader = csv.reader(inf)
        writer = csv.writer(outf)
        for row in reader:
            rows = calculate_duration_questions(row)
            writer.writerows(rows)


if __name__ == '__main__':
    import os
    import sys
    try:
        input_f = sys.argv[1]
    except IndexError:
        print('an input filename must be supplied as first argument')
        sys.exit(1)
    input_f_b, ext = os.path.splitext(input_f)
    output_f = input_f_b + '_qt' + ext
    convert2question_time(input_f, output_f)
