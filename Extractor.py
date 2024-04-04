import pdfplumber
from io import BytesIO
from utils import *
import json

def extract_data_from_pdf(pdf_data):
    with BytesIO(pdf_data) as pdf_buffer:
        with pdfplumber.open(pdf_buffer) as pdf:
            processed_dictionary = {}
            processed_dictionary['☐'] = []
            processed_dictionary['☒'] = []
            vendor_cond = True
            for p0 in pdf.pages:
                p0_tables = p0.extract_tables(table_settings={
                    "vertical_strategy": "lines",
                    "horizontal_strategy": "lines",
                    "snap_x_tolerance": 6,
                    "intersection_tolerance":6
                })
                if p0 == pdf.pages[0]:
                    for table in p0_tables:
                        table = table[1:]
                        table = [sublist for sublist in table if any(item not in (None, '') for item in sublist)]
                        for i in table:
                            i = [item for item in i if item is not None]
                            processed_strings = []
                            for u in i:
                                u = remove_newlines(u)
                                # u = remove_newline_after_colon(u)
                                # u = remove_newline_if_number_follows(u)
                                processed_strings.append(u)
                            processed_strings = remove_none_from_list(processed_strings)
                            s = process_string_list(processed_strings)
                            t = process_values(s)
                            processed_dictionary.update(t)
                else:
                    # p0_tables[0] = p0_tables[0][1:]
                    for table in p0_tables:
                        for index,i in enumerate(table):
                            i = [item for item in i if item is not None]
                            if i[0] == "":
                                last_key = list(processed_dictionary)[-1]
                                if len(i) > 1:
                                    processed_dictionary[last_key] = processed_dictionary[last_key] + i[1]
                                # print(processed_dictionary[last_key])
                                p0_tables = p0_tables[1:]
                                break
                    for table in p0_tables:
                        for i in table:
                            i = [item for item in i if item is not None]
                            processed_string = []
                            for u in i:
                                u = str(u)
                                u = u.strip()
                                u = remove_newlines(u)
                                processed_string.append(u)
                            z = strings_with_symbol(processed_string)
                            z = reverse_parse_strings(z)
                            processed_string = remove_none_from_list(processed_string)
                            if "Vendor Selection Criteria" in processed_dictionary.keys() and vendor_cond:
                                if "Justification" not in processed_string[0]:
                                    processed_dictionary["Vendor Selection Criteria"] = processed_dictionary["Vendor Selection Criteria"] +" "+ processed_string[0]
                                else:
                                    vendor_cond = False   
                                # while "Justification" not in processed_string[0]:
                                #     processed_dictionary["Vendor Selection Criteria"] = processed_dictionary["Vendor Selection Criteria"] + processed_string[0]
                            s = process_string_list(processed_string)
                            processed_dictionary.update(s)
                            for key in z.keys():
                                processed_dictionary[key].extend(z[key])
        processed_dictionary["Contact person"] = processed_dictionary["Contact Person"]
        del processed_dictionary["Contact Person"]
        print(processed_dictionary)
        return json.dumps(processed_dictionary)
