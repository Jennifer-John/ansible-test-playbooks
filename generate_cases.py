import pandas as pd
df0 = pd.read_excel('storage_container_params.xlsx')

module = "storage_container"
df = df0.where(pd.notnull(df0), None)

df1 = {}
name =[]
id =[]
index = 1
failed_when = []
output_key = "storage_container_details"
case_create = module + " create with all_params "
case_fw = ""
for param in range(len(df)):
  if df['Create'][param] == "Yes":
    case_create = case_create + df['Parameter name'][param] + " as " + df['Parameter name'][param] + "_1 "
    if df['api_mapping'][param] and df['api_mapping'][param] != "NA":
      if df['conversion'][param] and df['conversion'][param] != "NA":
            case_fw = case_fw + output_key + "." + df['api_mapping'][param] + " is not " + df['Parameter name'][param] + "_1" + df['conversion'][param] + " or "
      else:
            case_fw = case_fw + output_key + "." + df['api_mapping'][param] + " is not " + df['Parameter name'][param] + "_1 or "
name.append(case_create + "[check_mode] [idempotency]")
failed_when.append(case_fw + "changed is not true")
id.append(index)
index = index + 1

case_modify = module + " modify with all_params "
case_fw = ""
for param in range(len(df)):
  if df['Modify'][param] == "Yes" and df['Parameter name'][param] != module + "_id":
    case_modify = case_modify + df['Parameter name'][param] + " as " + df['Parameter name'][param] + "_2 "
    case_fw = case_fw + output_key + "." + df['Parameter name'][param] + " is not " + df['Parameter name'][param] + "_2 or "
name.append(case_modify + "[check_mode] [idempotency]")
failed_when.append(case_fw + "changed is not true")
id.append(index)
index = index + 1


case_get = module + " get with "
case_fw = ""
for param in range(len(df)):
  if df['Get'][param] == "Yes" and df['Parameter name'][param] != module + "_name":
    case_get = case_get + df['Parameter name'][param] + " as " + df['Parameter name'][param] + "_1 "
    case_fw = case_fw + output_key + "." + df['Parameter name'][param] + " is not " + df['Parameter name'][param] + "_1 or "
name.append(case_get)
failed_when.append(case_fw + "changed is true")
id.append(index)
index = index + 1

case_delete = module + " delete with "
case_fw = ""
for param in range(len(df)):
  if df['Delete'][param] == "Yes" and df['Parameter name'][param] != module + "_name":
    case_delete = case_delete + df['Parameter name'][param] + " as " + df['Parameter name'][param] + "_1 "
    case_fw = case_fw + output_key + "." + df['Parameter name'][param] + " is not " + df['Parameter name'][param] + "_1 or "
name.append(case_delete + "[check_mode] [idempotency]")
failed_when.append(case_fw + "changed is not true")
id.append(index)
index = index + 1

for param in range(len(df)):
  # if (df['Type'][param] == "str" or df['Type'][param] == "bool")  and df['Create'][param]:
  #   name.append(module + " create " + module +  " with " + df['Parameter name'][param] + " as " +  "invalid_" +df['Parameter name'][param] +  " - Negative")
  #   failed_when.append("invalid_" +df['Parameter name'][param] + " not in result.msg")
  #   id.append(index)
  #   index = index + 1
  if df['Type'][param] == "int":
    name.append(module + " create with " + df['Parameter name'][param] + " as " + "invalid_" + df['Parameter name'][param] + " - Negative")
    failed_when.append("invalid_" +df['Parameter name'][param] + " not in result.msg")
    id.append(index)
    index = index + 1
  # elif df['Type'][param] == "bool":
  #   name.append(module + " create " + module + " with " + df['Parameter name'][param] + " as " + df['Parameter name'][param] + "_invalid - Negative")
  #   failed_when.append("changed is True")
  #   id.append(index)
  #   index = index + 1
  if df['Mutually exclusive'][param] != None:
    name.append(module + " create with " + df['Parameter name'][param] + " as " + df['Parameter name'][param] + "_1 " + df['Mutually exclusive'][param] + " as " + df['Mutually exclusive'][param] + "_1 - Negative")
    failed_when.append("mutually_exclusive_param_name not in result.msg")
    id.append(index)
    index = index + 1

df1 = {"ID": id, "TC_NAME": "TC", "TESTCASE": name, "FAILED_WHEN": failed_when, "CHECK_MODE_ASSERTS": None, "NORMAL_MODE_ASSERTS": None, "IDEMPOTENCY_MODE_ASSERTS": None}
df2 = pd.DataFrame(df1)
df2.to_csv('test-cases.csv', index=False)