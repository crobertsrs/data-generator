import json
import pandas as pd

output = dict()

with open('student_organization_types_raw.txt', 'r') as f:
    data = json.load(f)
    for item in data["items"]:
        output[item["name"]] = []

list_of_types_for_df = []
list_of_names_for_df = []

with open('student_organizations_raw.txt', 'r') as f:
    data = json.load(f)
    for response in data:
        for item in response['value']:
            for category in item["CategoryNames"]:
                if category in output.keys():
                    list_of_types_for_df.append(category)
                    list_of_names_for_df.append(item["Name"])
                    output[category].append(item["Name"])

data = {
    "Type": list_of_types_for_df,
    "Name": list_of_names_for_df
}
df = pd.DataFrame(data)
print(df.head)
df.to_csv('student_organizations.csv', index=False)

with open('student_organizations.txt', 'w') as f:
    f.write(str(output))

