import sys
import os
import re
import argparse
import datetime
from collections import OrderedDict
from typing import List
from contextlib import contextmanager
import io


def load_srt_file(file_path: str) -> OrderedDict[int, str]:
    srt_data = OrderedDict()
    with open(file_path, 'r') as file:
        lines = file.readlines()
        sequence_number = None
        dialogue = ''
        for line in lines:
            line = line.strip()
            if re.match(r'^\d+$', line):
                if sequence_number is not None:
                    srt_data[sequence_number] = dialogue
                sequence_number = int(line)
                dialogue = ''
            elif re.match(r'^\d+:\d+:\d+,\d+ --> \d+:\d+:\d+,\d+$', line):
                continue
            elif line.startswith('[') and line.endswith(']'):
                continue
            else:
                dialogue += line + ' '
        if sequence_number is not None:
            srt_data[sequence_number] = dialogue
    return srt_data


def load_txt_file(file_path: str) -> List[str]:
    with open(file_path, 'r') as file:
        return file.read().splitlines()


def align_transcriptions(srt_data: OrderedDict[int, str], transcriptions: List[str]) -> OrderedDict[int, str]:
    aligned_data = OrderedDict()
    for i, (sequence_number, dialogue) in enumerate(srt_data.items()):
        if i < len(transcriptions):
            aligned_data[sequence_number] = transcriptions[i]
        else:
            aligned_data[sequence_number] = dialogue
    return aligned_data


def replace_dialogue_transcriptions(srt_data: OrderedDict[int, str], aligned_data: OrderedDict[int, str]) -> OrderedDict[int, str]:
    replaced_data = OrderedDict()
    for sequence_number, dialogue in srt_data.items():
        if sequence_number in aligned_data:
            replaced_data[sequence_number] = aligned_data[sequence_number]
        else:
            replaced_data[sequence_number] = dialogue
    return replaced_data


def save_corrected_srt_file(file_path: str, replaced_data: OrderedDict[int, str]):
    with open(file_path, 'w') as file:
        for sequence_number, dialogue in replaced_data.items():
            file.write(str(sequence_number) + '\n')
            file.write(dialogue + '\n')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--srt', help='path to the SRT file')
    parser.add_argument('--txt', help='path to the TXT file')
    args = parser.parse_args()

    srt_file_path = args.srt
    txt_file_path = args.txt

    srt_data = load_srt_file(srt_file_path)
    transcriptions = load_txt_file(txt_file_path)
    aligned_data = align_transcriptions(srt_data, transcriptions)
    replaced_data = replace_dialogue_transcriptions(srt_data, aligned_data)
    save_corrected_srt_file(srt_file_path, replaced_data)


if __name__ == '__main__':
    main()