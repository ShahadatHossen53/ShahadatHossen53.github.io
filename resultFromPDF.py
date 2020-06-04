from PyPDF2 import PdfFileReader

def find_grade(course):
    result = 0.0
    for grage in course:
        if grage == "A":
            result += 4
        elif grage == "A-":
            result += 3.7
        elif grage == "B+":
            result += 3.3
        elif grage == "B":
            result += 3.00
        elif grage == "B-":
            result += 2.7
        elif grage == "C+":
            result += 2.3
        elif grage == "C":
            result += 2.0
        elif grage == "C-":
            result += 1.7
        elif grage == "D+":
            result += 1.3
        elif grage == "D":
            result += 1
        elif grage == "F":
            result += 0
        else:
            result = 0
    return result




try:
    txtFName = open("myResultPdf.txt")

    while True:
        txtFName = open("myResultPdf.txt")
        sid = input("Enter student ID: ")
        if sid == "done": break
        tCourseDiction = dict()
        lCourseDiction = dict()

        tCourse = list()
        lCourse = list()
        for wline in txtFName:
            tempPage = list()
            wline = wline.replace("\n", "")
            tempPage = wline.split("__%__")

            try:
                indx = tempPage.index("Course")
            except:
                indx = -1
            if indx >= 0:
                if len(tempPage[indx + 2]) <= 3:
                    incIndx = 3
                else:
                    incIndx = 2
                tempCName = tempPage[indx - 2] + " " + tempPage[indx - 1] + " " + tempPage[indx + incIndx]
                lab_couse = False
                theory_couse = False
                if "lab" in tempCName.lower():
                    #tempCName = "Lab : " + tempCName
                    lab_couse = True
                else:
                    #tempCName = "Theory : " + tempCName
                    theory_couse = True

            for line in tempPage:
                found = False
                if sid == line:
                    #print(tempCName)
                    #print("Student ID:", line)
                    indx = tempPage.index(line) + 2
                    isNum = tempPage[indx]

                    stdName = ""
                    Withheld = False
                    while True:
                        if isNum[0] in "0123456789": break
                        stdName = stdName + tempPage[indx - 1] + " "
                        if isNum == "Withheld":
                            Withheld = True
                            break
                        indx += 1
                        try:
                            isNum = tempPage[indx]
                        except:
                            break
                    if Withheld:
                        grage = "W"
                    else:
                        grage = tempPage[indx - 1]
                    if lab_couse:
                        lCourse.append(grage)
                        lCourseDiction[tempCName] = grage
                    else:
                        tCourse.append(grage)
                        tCourseDiction[tempCName] = grage


                    #print("Student Name:", stdName)
                    #print("Student Grade:", grage)
                    found = True
                    break
            if found:
                found = False
                continue

        tGrade = find_grade(tCourse)*3
        lGrade = find_grade(lCourse)*1.5
        total_credit = (len(tCourse)*3) + (len(lCourse)*1.5)
        result = (tGrade+lGrade)/total_credit



        #print(tCourse)
        #print(lCourse)
        print("\nName :", stdName)
        print("ID :", sid)
        print("\t\n-----------Theory Courses--------------\n")
        for cname, cgrade in tCourseDiction.items():
            print(cname,"\t\t:", cgrade)

        print("\t\n-----------Lab Courses--------------\n")
        for cname, cgrade in lCourseDiction.items():
            print(cname, "\t\t:",cgrade)

        print("\n\nTotal Credit :", total_credit)
        print("Result :", "{:.2f}".format(result))
        print("\n|\n|\n|\n|\n")
        txtFName.close()
    txtFName.close()
except:
    file_path = 'myResult.pdf'
    txtFName = open("myResultPdf.txt", "w")
    pdf = PdfFileReader(file_path)

    coutner = 0
    courseTriger = -1
    courseName = list()
    for page_num in range(pdf.numPages):
        coutner += 1
        pageObj = pdf.getPage(page_num)
        try:
            txt = pageObj.extractText()
        except:
            pass
        else:
            page = str(txt).split("\n")
            tempPage = list()

            for line in page:
                tempPage.append(line.strip())
            tempPage = list(filter(None, tempPage))
            for line in tempPage:
                if len(line.strip()) < 1:
                    tempPage.remove(line)

            indx = 0
            for line in tempPage:
                if len(tempPage) <= indx + 1: break
                if len(line) < 2 and tempPage[indx + 1] == "-":
                    tempPage[indx] = line + "-"
                indx += 1

            for line in tempPage:
                if line == "-":
                    tempPage.remove(line)

            wstring = "__%__".join(tempPage)
            txtFName.write(wstring + "\n")
    txtFName.close()
    print("Run this program again :)")
