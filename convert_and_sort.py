import pandas as pd
import json

# Чтение JSON файла
json_file = 'filtered_users.json'

with open(json_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Создание DataFrame из данных JSON
df = pd.DataFrame(data)

# Сортировка по итоговому баллу (total_score)
df_sorted = df.sort_values(by='total_score', ascending=False)

# Запись в Excel файл
excel_file = 'sorted_filtered_users2.xlsx'

df_sorted.to_excel(excel_file, index=False)

print(f"Sorted data saved to {excel_file}")
