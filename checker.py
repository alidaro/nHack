import pandas as pd
import json

def score_programming_skills(value):
    if value == "Имею хорошие базовые навыки на уровне студента ИТ-университета":
        return 4
    elif value == "Обучаюсь программированию на курсах или самостоятельно":
        return 3
    elif value == "Профессиональный разработчик":
        return 5
    elif value == "Спортивный программист":
        return 4
    return 0

def score_telegram(value):
    if value == "Есть":
        return 2
    return 0

def score_socialmedia(value):
    if value in ["Есть", "Иногда"]:
        return 1
    return 0

def score_github(value):
    if value == "Есть":
        return 3
    return 0

def score_studyplace(value, projects):
    if isinstance(projects, float):
        projects = ""
    score = 0
    if "РФМШ" in value or "КТЛ" in value or "НИШ" in value:
        score = 3 if projects.strip() else 1
    elif "ауыл" in value.lower():
        score = 4
    return score

def score_major(value):
    if pd.isna(value):
        return 0
    major_keywords = {
        "прикладная математика": 4,
        "математическое и компьютерное моделирование": 5,
        "математика": 3,
        "информационные системы": 4,
        "софтвейр инженер": 5
    }
    for keyword, points in major_keywords.items():
        if keyword in value.lower():
            return points
    return 0

def score_workplace(value):
    if value == "Не работал":
        return 0
    elif value == "Работал на фрилансе":
        return 1
    elif value == "Работал в стартапе":
        return 2
    elif value == "Работал в крупной компании":
        return 3
    return 0

def score_experience(value):
    if pd.isna(value) or value == "":
        return -7
    length = len(value)
    score = 0
    if length > 1000:
        score = 7
    elif length > 200:
        score = 5
    elif length > 50:
        score = 3
    elif length > 20:
        score = 1
    business_keywords = ["сделал", "решил", "управлял", "организовал"]
    for keyword in business_keywords:
        if keyword in value.lower():
            score += 1
            break
    return score

def score_projects(value):
    if pd.isna(value) or value.strip() == "":
        return 0
    length = len(value)
    if length > 1000:
        return 5
    elif length > 200:
        return 3
    elif length > 50:
        return 2
    return 1

def score_besthonors(value):
    if pd.isna(value) or value.strip() == "":
        return 0
    score = 0
    honor_keywords = ["ICPC", "Olympiad", "Hackathon"]
    for keyword in honor_keywords:
        if keyword.lower() in value.lower():
            score += 2
    return score

def score_almaty(value):
    if value == "ИСТИНА":
        return 0
    elif value == "ЛОЖЬ":
        return -1000
    return 0

file_path = r'C:\Users\Alida\Desktop\nHackd.xlsx'
df = pd.read_excel(file_path)

print("Названия столбцов в файле Excel:")
print(df.columns)

df.columns = [col.strip() for col in df.columns]

df['programming_skills_score'] = df['Какое из вариантов лучше всего описывает Ваш уровень навыков программирования?'].apply(score_programming_skills)
df['telegram_score'] = df['Профиль в Telegram'].apply(score_telegram)
df['socialmedia_score'] = df['Ссылки на профили в социальных сетях'].apply(score_socialmedia)
df['github_score'] = df['Ссылка на GitHub'].apply(score_github)
df['studyplace_score'] = df.apply(lambda row: score_studyplace(row['Университет/школа, где Вы учились/учитесь'], row['Если есть, Ваши прошлые проекты по программированию']), axis=1)
df['major_score'] = df['Специальность в университете'].apply(score_major)
df['workplace_score'] = df['Место работы (если есть)'].apply(score_workplace)
df['experience_score'] = df['Подробное описание Вашего опыта в программировании'].apply(score_experience)
df['projects_score'] = df['Если есть, Ваши прошлые проекты по программированию'].apply(score_projects)
df['besthonors_score'] = df['Ваши самые впечатляющие достижения (в программировании, учебе, спорте и пр.)'].apply(score_besthonors)
df['almaty_score'] = df['Можете ли Вы находиться в Алматы на время инкубатора (5 июня - 9 августа 2024г)?'].apply(score_almaty)

df['total_score'] = (df['programming_skills_score'] + df['telegram_score'] + df['socialmedia_score'] + df['github_score'] +
                     df['studyplace_score'] + df['major_score'] + df['workplace_score'] + df['experience_score'] +
                     df['projects_score'] + df['besthonors_score'] + df['almaty_score'])

df_sorted = df.sort_values(by='total_score', ascending=False)

filtered_df = df_sorted[df_sorted['total_score'] >= 0]

excel_file = 'sorted_filtered_users1.xlsx'
filtered_df.to_excel(excel_file, index=False)
print(f"Sorted data saved to {excel_file}")

json_file = 'filtered_users.json'
filtered_df.to_json(json_file, orient='records', force_ascii=False, indent=4)
print(f"Filtered data saved to {json_file}")
