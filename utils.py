import re


def remove_newlines(text):
    if text:
        return re.sub(r'\n', '', text)


def remove_strings_without_colon(string_list):
    # Date-like object regex
    date_regex = r'\b\d{1,2}[./-]\d{1,2}[./-]\d{2,4}\b'
    updated_list = []
    for string in string_list:
        if ':' in string:
            updated_list.append(string)
        else:
            # Check if the string contains a date-like object
            match = re.search(date_regex, string)
            if match:
                date_index = match.start()
                if date_index > 0 and string[date_index - 1] == ' ':
                    updated_string = string[:date_index] + \
                        ':' + string[date_index:]
                    updated_list.append(updated_string)
                else:
                    updated_list.append(string)
    return updated_list


def strings_with_symbol(lst):
    result = []
    for string in lst:
        if string:
            if '☒' in string or '☐' in string:
                result.append(string)
    return result


def convert_to_dict(lst):
    result_dict = {}
    for string in lst:
        if '☐' in string:
            key = string.replace('☐', '').strip()
            value = '☐'
            result_dict[key] = value
        elif '☒' in string:
            key = string.replace('☒', '').strip()
            value = '☒'
            result_dict[key] = value
    return result_dict


def reverse_parse_strings(lst):
    result_dict = {}
    for string in lst:
        if '☐' in string:
            key = '☐'
            value = string.replace('☐', '').strip()
            result_dict.setdefault(key, []).append(value)
        elif '☒' in string:
            key = '☒'
            value = string.replace('☒', '').strip()
            result_dict.setdefault(key, []).append(value)
    return result_dict


def process_values(dictionary):
    updated_dict = {}
    for key, value in dictionary.items():
        if "AFE" in value:
            segments = value.split('\n', 1)
            for segment in segments:
                if ':' in segment:
                    key_segment, value_segment = segment.split(':', 1)
                    if key_segment.strip() != key:
                        updated_dict[key_segment.strip()] = value_segment.strip()
        if key not in updated_dict:
            updated_dict[key] = value.split('\n', 1)[0]
    return updated_dict


def remove_newline_after_colon(text):
    return re.sub(r':\s*\n', ': ', text)


def remove_none_from_list(lst):
    return [item for item in lst if item is not None]


def remove_newline_if_number_follows(text):
    return re.sub(r'\n(\d)', r'\1', text)


def parse_string_to_key_value_pair(input_string, next_string=None):
    if ':' in input_string:
        key, value = input_string.split(':', 1)
        key = key.strip()
        value = value.strip()
        if not value and next_string:
            value = next_string.strip()
        return key, value
    else:
        return None, None


def process_string_list(input_strings):
    key_value_pairs = {}
    next_string = None
    condition_met = False
    for idx, input_string in enumerate(input_strings):
        key, value = parse_string_to_key_value_pair(
            input_string, input_strings[idx + 1] if idx + 1 < len(input_strings) else None)
        if key is not None and value is not None:
            res = list(key_value_pairs.values())
            for i in res:
                if key in i:
                    condition_met = True  #
                    break
            if condition_met:
                continue
            key_value_pairs[key] = value
            next_string = None
        elif key is not None and value is None:
            next_string = input_strings[idx + 1] if idx + \
                1 < len(input_strings) else None
            idx = idx + 1
    return key_value_pairs
