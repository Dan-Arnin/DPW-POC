import pdfplumber
from io import BytesIO
from utils import *
import json

def extract_data_from_pdf(pdf_data):
    with BytesIO(pdf_data) as pdf_buffer:
        with pdfplumber.open(pdf_buffer) as pdf:
            try:
                p0 = pdf.pages[0]
                p1 = pdf.pages[1]
                p2 = pdf.pages[2]
            except:
                print("No need to worry")
            processed_dictionary = {}
            processed_dictionary['☐'] = []
            processed_dictionary['☒'] = []
            p0_tables = p0.extract_tables(table_settings={
                "vertical_strategy": "lines",
                "horizontal_strategy": "lines",
                "snap_x_tolerance": 6,
            })

            for table in p0_tables:
                table = table[1:]
                for i in table:
                    i = remove_none_from_list(i)
                    processed_strings = []
                    for u in i:
                        u = remove_newline_after_colon(u)
                        u = remove_newline_if_number_follows(u)
                        processed_strings.append(u)
                    s = process_string_list(processed_strings)
                    t = process_values(s)
                    processed_dictionary.update(t)

            p1_tables = p1.extract_tables(table_settings={
                "vertical_strategy": "lines",
                "horizontal_strategy": "lines",
                "snap_x_tolerance": 6,
                "text_x_tolerance": 1,
                "text_y_tolerance": 1,
            })
            for table in p1_tables:
                # print(table)
                for i in table:
                    if i[0] == "":
                        last_key = list(processed_dictionary)[-1]
                        i = remove_none_from_list(i)
                        processed_dictionary[last_key] = processed_dictionary[last_key] + i[1]
                        p1_tables = p1_tables[1:]
                        break
            for table in p1_tables:
                for i in table:
                    i = remove_none_from_list(i)
                    if (len(i) > 1):
                        processed_strings = []
                        for u in i:
                            u = remove_newline_after_colon(u)
                            u = remove_newline_if_number_follows(u)
                            processed_strings.append(u)
                        z = strings_with_symbol(processed_strings)
                        z = reverse_parse_strings(z)
                        s = process_string_list(processed_strings)
                        processed_dictionary.update(s)
                        for key in z.keys():
                            processed_dictionary[key].extend(z[key])
            try:

                p2_tables = p2.extract_tables(table_settings={
                    "vertical_strategy": "lines",
                    "horizontal_strategy": "lines",
                    "snap_x_tolerance": 6,
                    "text_x_tolerance": 1,
                    "text_y_tolerance": 1,
                })
                p2_tables[0] = p2_tables[0][1:]

                for table in p2_tables:
                    # print(table)
                    for i in table:
                        if i[0] == "":
                            last_key = list(processed_dictionary)[-1]
                            i = remove_none_from_list(i)
                            processed_dictionary[last_key] = processed_dictionary[last_key] + i[1]
                            p2_tables = p2_tables[1:]
                            break

                for table in p2_tables:
                    for i in table:
                        processed_string = []
                        for u in i:
                            u = str(u)
                            u = u.strip()
                            u = remove_newlines(u)
                            # u = remove_newline_after_colon(u)
                            # u = remove_newline_if_number_follows(u)
                            processed_string.append(u)
                        z = strings_with_symbol(processed_string)
                        z = reverse_parse_strings(z)
                        processed_string = remove_strings_without_colon(
                            processed_string)
                        s = process_string_list(processed_string)
                        processed_dictionary.update(s)
                        for key in z.keys():
                            processed_dictionary[key].extend(z[key])
            except:
                print("No thrid page")
        if "Contact Person" in processed_dictionary.keys():
            processed_dictionary["Contact person"] = processed_dictionary["Contact Person"]
        processed_dictionary["Unchecked"] = processed_dictionary.pop('☐')
        processed_dictionary["Checked"] = processed_dictionary.pop('☒')
        print(json.dumps(processed_dictionary))
        return json.dumps(processed_dictionary)
