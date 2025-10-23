import sys
import os
import ast
import json
import pandas as pd
from datetime import datetime
from pydantic import ValidationError, BaseModel
from typing import Optional
#from models import *
from models import MetaModel, DataModel, RecordModel 


# CSV → JSON converter
def csv_to_json_pydantic(data: pd.DataFrame):
    """Convert CSV DataFrame to list of validated JSON dicts."""
    data = data.dropna(how='all')  # remove completely blank rows
    result = []
    mistakes=[]

    for _, row in data.iterrows():
        try:
            meta = MetaModel(timestamp=datetime.now().isoformat())

            level_val = row.get("level")
            if isinstance(level_val, str) and level_val.strip().startswith("["):
                try:
                    level_val = ast.literal_eval(level_val)
                except (ValueError, SyntaxError):
                    level_val = level_val



            data_model = DataModel(
                term_code=row["Term"],
                course_code=row["course_code"],
                seek_course_namespace=row.get("seek_course_namespace"),
                link_to_seek=row.get("link_to_seek"),
                program_type=row.get("program_type"),
                start_date=row.get("start_date"),
                end_date=row.get("end_Date"),
                exam_date=row.get("exam_Date"),
                #level=row.get("level")
                level= str(level_val)
            )
            record = RecordModel(meta=meta, data=data_model)
            result.append(record.model_dump())
            #record_dict = {
            #    "meta": meta.model_dump(),
            #    "data": data_model.model_dump()
            #}
            #result.append(record_dict)
        #except ValidationError as e:
            #print(f"Validation error in row: {e}")
        except:
            mis_dict= {
                "row" : _,
                "na ni?": "a mistake"
            }
            result.append(mis_dict)

    return result



# processing function

def process_file(filename: str, return_json: bool = False):
    """Read CSV, convert to JSON list, optionally save to file."""
    filepath = os.path.join('uploads', filename)

    if filename.endswith('.csv'):
        df = pd.read_csv(filepath, skip_blank_lines=True)
    elif filename.endswith('.xlsx'):
        df = pd.read_excel(filepath)
    else:
        raise ValueError("Unsupported file format")

    # call 
    json_output = csv_to_json_pydantic(df)

    # Optionally save
    if return_json:
        output_dir = "outputs"
        os.makedirs(output_dir, exist_ok=True)
        json_filename = os.path.splitext(filename)[0] + ".json"
        output_path = os.path.join(output_dir, json_filename)

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(json_output, f, indent=2, ensure_ascii=False)

        print(f"JSON file saved at: {output_path}")

    return json_output

#
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No filename provided"}))
        sys.exit(1)

    filename = sys.argv[1]
    return_json = False

    if len(sys.argv) > 2 and sys.argv[2].lower() == "true":
        return_json = True

    output = process_file(filename, return_json)
    print(json.dumps(output, indent=2, ensure_ascii=False))
