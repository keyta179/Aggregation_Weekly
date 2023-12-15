import csv, sys, math, unicodedata, datetime, collections
# import createDocument as c
from dataclasses import dataclass

@dataclass
class Student:
    year: int
    month: int
    date: int
    period: str
    department: str
    group: str
    schoolYear: str
    studentId: str
    subject: str
    question: str
    
    # 文字列を大文字にする('k'と'K'を同一のものとして捉えるため)
    def correction(student_id):
        return student_id.upper()

    # 学生証番号から学科を求める
    def checkDepartment(student_id):
        if student_id.upper()[2] == "K":
            if student_id[3] == "0":
                return "CS"
            elif student_id[3] == "1":
                return "DM"
        return "others"

    # 学生証番号からクラスを求める
    def checkGroup(student_id):
        if student_id.upper()[2] == "K":
            if student_id[3:5] == "00":
                return "A"
            elif student_id[3:5] == "01":
                return "B"
            elif student_id[3:5] == "10":
                return "C"
            elif student_id[3:5] == "11":
                return "D"
        return "others"

    # タイムスタンプから月、日、時限を求める
    def checkDay(time):
        time = time.split(" ")
        year = int(time[0].split("/")[0])
        month = int(time[0].split("/")[1])
        date = int(time[0].split("/")[2])
        period = datetime.datetime(year, month, date).weekday() # 0~6で返ってくる(0が月曜日)
        if period == 0:
            period = "月"
        elif period == 1:
            period = "火"
        elif period == 2:
            period = "水"
        elif period == 3:
            period = "木"
        elif period == 4:
            period = "金"
        elif period == 5:
            period = "土"
        else:
            period = "日"
        hour = int(time[1].split(":")[0])
        minute = int(time[1].split(":")[1])
        if ((hour == 10 and minute >=40) or hour == 11 or (hour == 12 and minute < 30)):
            period += "2"
        elif (hour == 12 or (hour == 13 and minute < 10)):
            period += "L"
        elif (hour == 13  or hour == 14):
            period += "3"
        elif (hour == 15 or (hour == 16 and minute < 50)):
            period += "4"
        elif (hour == 16 or hour == 17 or hour == 18):
            period += "5"
        else:
            period += ""
        return year, month, date, period
    
    # 特定のフィールドのみのリストを作る
    def createList(dataList, field):
        newList = []
        for data in dataList:
            if field == "year":
                newList.append(data.year)
            elif field == "month":
                newList.append(data.month)
            elif field == "date":
                newList.append(data.date)
            elif field == "period":
                newList.append(data.period)
            elif field == "department":
                newList.append(data.department)
            elif field == "group":
                newList.append(data.group)
            elif field == "schoolYear":
                newList.append(data.schoolYear)
            elif field == "studentId":
                newList.append(data.studentId)
            elif field == "subject":
                newList.append(data.subject)
            elif field == "question":
                newList.append(data.question)
            
        return newList
    
    # 対象の授業のデータを取り出す
    def checkSubject(dataList, target):
        targetList = []
        for data in dataList:
            if data.subject == target:
                targetList.append(data)
        return targetList    
    
    # 絞り込み
    def NarrowDown(dataList, field, target):
        newList = []
        for data in dataList:
            if field == "year" and target == data.year:
                newList.append(data)
            elif field == "month" and target == data.month:
                newList.append(data)
            elif field == "date" and target == data.date:
                newList.append(data)
            elif field == "period" and target == data.period:
                newList.append(data)
            elif field == "department" and target == data.department:
                newList.append(data)
            elif field == "group" and target == data.group:
                newList.append(data)
            elif field == "schoolYear" and target == data.schoolYear:
                newList.append(data)
            elif field == "studentId" and target == data.student:
                newList.append(data)
            elif field == "subject" and target == data.subject:
                newList.append(data)
            elif field == "question" and target == data.question:
                newList.append(data)
    
        return newList
    
    # 個々のデータを調べる(時限別来訪者数)
    def countIndividual(dataList, d):
        for data in dataList:
            if not data in d.keys():
                d[data] = 1
            else:
                d[data] += 1
        return d

# 文字列の調整
def text_count(s):
     text_counter = 0
     for c in s:
          j = unicodedata.east_asian_width(c)
          if 'F' == j:
               text_counter += 2
          elif 'H' == j:
               text_counter += 1
          elif 'W' == j:
               text_counter += 2
          elif 'Na' == j:
               text_counter += 1
          elif 'A' == j:
               text_counter += 2
          else:
               text_counter += 1
     return text_counter

def upto3(n):
     return int(math.log10(n)) + 1 if n > 0 else 1

# main
studentList = []

with open(f"{sys.argv[1]}.csv","r",encoding="utf-8") as file:
     reader=csv.reader(file)
     header=next(reader)
    
    #  来訪者データをStudentクラスにして、studentListに入れる
     for row in reader:
         time = row[0]
         year = Student.checkDay(time)[0]
         month = Student.checkDay(time)[1]
         date = Student.checkDay(time)[2]
         period = Student.checkDay(time)[3]
         department = Student.checkDepartment(row[2])
         group = Student.checkGroup(row[2])
         school_year = row[1]
         student_id = Student.correction(row[2])
         subject = row[4]
         question = row[5]
         subjectInformation = Student(year, month, date, period, department, group, school_year, student_id,subject, question)
         studentList.append(subjectInformation)
         
# 科目別来訪者数を計算する
print("\n科目別来訪者数")
lessonList = Student.createList(studentList, "subject")
lessonDictionary = {}
lessonDictionary = dict(sorted(Student.countIndividual(lessonList, lessonDictionary).items(), key=lambda x: x[1], reverse=True))

text_len = []
for key, value in lessonDictionary.items():
     text_len.append(text_count(key))

max_len = max(text_len)

sum = 0
target = 1000 # 大きい値
topSubjectList = []
deleteList = ["自習", "プロジェクト", "卒業論文", "修士論文/Master's Thesis"]
twoPartLessonList = ["数理実験", "数学演習1", "数学・物理演習", "自然科学の基礎", 
                     "線形代数の基礎", "線形代数の応用1", "線形代数の応用2", 
                     "微積分法の基礎 (微分法の基礎と応用)", "微積分法の応用", 
                     "情報科学入門", "コンピュータシステム入門1", "コンピュータシステム入門2",
                     "離散構造1", "離散構造2", "離散構造2演習", 
                     "統計学1", "統計学1演習", "統計学2",
                     "プログラミング1(C/C++)", "プログラミング1(Java)", 
                     "形式言語とオートマトン", "データ構造とアルゴリズム1",
                     "データベース", "人工知能",
                     "最適化",
                     ]
fourPartLessonList = ["プログラミング入門(1・2)", "プログラミング入門3（プログラミング演習1(python)）", 
                      "離散構造1演習", "データ構造とアルゴリズム1演習",
                      ]

for key, value in lessonDictionary.items():
    targetList = Student.checkSubject(studentList, key)
    if key in twoPartLessonList:
        departmentDictionary = {"CS": 0, "DM": 0}
        twoPartList = Student.createList(targetList, "department")
        departmentDictionary = Student.countIndividual(twoPartList, departmentDictionary)
        more = f"({departmentDictionary['CS']}/{departmentDictionary['DM']})"
    elif key in fourPartLessonList:
        groupDictionary = {"A": 0, "B": 0, "C": 0, "D": 0}
        fourPartList = Student.createList(targetList, "group")
        departmentDictionary = Student.countIndividual(fourPartList, groupDictionary)
        more = f"({groupDictionary['A']}/{groupDictionary['B']}/{groupDictionary['C']}/{groupDictionary['D']})"
    else:
        more = ""
    fixed_width = " " * (max_len - text_count(key) - upto3(value) + 5)
    print(f"{key}{fixed_width}{value}{more}")
    if sum < 5 and target > value:
            target = value
    if (sum < 5 or value == target) and not key in deleteList:
        sum += 1
        topSubjectList.append(key)

fixedWidth = " " * (max_len - 4 - upto3(len(studentList)) + 5)
print(f"\n合計 {len(studentList)}")

# 上位科目の出力
print(f"\n<来訪人数上位{sum}科目の来訪理由>\n")
for subject in topSubjectList:
    print(f"・{subject}：")
    

# 時限別来訪者数を計算する
periodList = Student.createList(studentList, "period")
periodDictionary = {
              '月2': 0, '月L': 0, '月3': 0, '月4': 0, '月5': 0, 
              '火2': 0, '火L': 0, '火3': 0, '火4': 0, '火5': 0, 
              '水2': 0, '水L': 0, '水3': 0, '水4': 0, '水5': 0, 
              '木2': 0, '木L': 0, '木3': 0, '木4': 0, '木5': 0, 
              '金2': 0, '金L': 0, '金3': 0, '金4': 0, '金5': 0,
              }

periodDictionary = Student.countIndividual(periodList, periodDictionary)

# print(periodDictionary)

print("\n時限別来訪者数\n")

total2 = periodDictionary['月2']+periodDictionary['火2']+periodDictionary['水2']+periodDictionary['木2']+periodDictionary['金2']
totalL = periodDictionary['月L']+periodDictionary['火L']+periodDictionary['水L']+periodDictionary['木L']+periodDictionary['金L']
total3 = periodDictionary['月3']+periodDictionary['火3']+periodDictionary['水3']+periodDictionary['木3']+periodDictionary['金3']
total4 = periodDictionary['月4']+periodDictionary['火4']+periodDictionary['水4']+periodDictionary['木4']+periodDictionary['金4']
total5 = periodDictionary['月5']+periodDictionary['火5']+periodDictionary['水5']+periodDictionary['木5']+periodDictionary['金5']

totalMon = periodDictionary['月2']+periodDictionary['月L']+periodDictionary['月3']+periodDictionary['月4']+periodDictionary['月5']
totalTue = periodDictionary['火2']+periodDictionary['火L']+periodDictionary['火3']+periodDictionary['火4']+periodDictionary['火5']
totalWed = periodDictionary['水2']+periodDictionary['水L']+periodDictionary['水3']+periodDictionary['水4']+periodDictionary['水5']
totalThu = periodDictionary['木2']+periodDictionary['木L']+periodDictionary['木3']+periodDictionary['木4']+periodDictionary['木5']
totalFri = periodDictionary['金2']+periodDictionary['金L']+periodDictionary['金3']+periodDictionary['金4']+periodDictionary['金5']

totalAll = total2+totalL+total3+total4+total5

printTop = "     月曜 火曜 水曜 木曜 金曜 合計"
print2 = f" 2限 {periodDictionary['月2']:4d} {periodDictionary['火2']:4d} {periodDictionary['水2']:4d} {periodDictionary['木2']:4d} {periodDictionary['金2']:4d} {total2:4d}"
printL = f" L限 {periodDictionary['月L']:4d} {periodDictionary['火L']:4d} {periodDictionary['水L']:4d} {periodDictionary['木L']:4d} {periodDictionary['金L']:4d} {totalL:4d}"
print3 = f" 3限 {periodDictionary['月3']:4d} {periodDictionary['火3']:4d} {periodDictionary['水3']:4d} {periodDictionary['木3']:4d} {periodDictionary['金3']:4d} {total3:4d}"
print4 = f" 4限 {periodDictionary['月4']:4d} {periodDictionary['火4']:4d} {periodDictionary['水4']:4d} {periodDictionary['木4']:4d} {periodDictionary['金4']:4d} {total4:4d}"
print5 = f" 5限 {periodDictionary['月5']:4d} {periodDictionary['火5']:4d} {periodDictionary['水5']:4d} {periodDictionary['木5']:4d} {periodDictionary['金5']:4d} {total5:4d}"
printTotal = f"合計 {totalMon:4d} {totalTue:4d} {totalWed:4d} {totalThu:4d} {totalFri:4d} {totalAll:4d}"

print(printTop)
print(print2)
print(printL)
print(print3)
print(print4)
print(print5)
print(printTotal)

# 上位の時限を出力する
sum = 0
target = 1000 # 大きい値
topPeriodList = []
sortPeriodDictionary = dict(sorted(periodDictionary.items(), key=lambda x: x[1], reverse=True))

for key, value in sortPeriodDictionary.items():
    if sum < 5 and target > value:
            
            target = value
    if sum < 5 or value == target:
        sum += 1
        topPeriodList.append(key)

print(f"\n<来訪者が多い時限{sum}つの主な来訪科目>\n")
for key, value in periodDictionary.items():
    first, second = "", ""
    i = 0
    if key in topPeriodList:
        narrowList = Student.NarrowDown(studentList, "period", key)
        narrowSubjectList = Student.createList(narrowList, "subject")
        c = collections.Counter(narrowSubjectList)
        while first == "" or second == "":
            if first == "" and not c.most_common()[i][0] in deleteList:
                first = c.most_common()[i][0]
            elif second == "" and not c.most_common()[i][0] in deleteList:
                second = c.most_common()[i][0]
            i += 1
        print(f"・{key[0]}曜{key[1]}限：{first},{second}")

# 学生別来訪回数を計算する
visitList = Student.createList(studentList, "studentId")
# print(visitList)

# print(studentList)
