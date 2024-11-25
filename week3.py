from jinja2 import Template
import sys
import pyhtml as h
import matplotlib.pyplot as plt
import csv

def main():
    fr = open('data.csv', 'r')
    csvreader = csv.reader(fr)
    header = next(csvreader)
    rows = []
    for row in csvreader:
        rows.append(row)
    if(len(sys.argv)>1):
        if(sys.argv[1]=='-s'):
            TEMPLATE=studentTemplate(header,rows)
        elif(sys.argv[1]=='-c'):
            TEMPLATE = courseTemplate(rows)
    else:
        TEMPLATE = wrongTemplate()
    template = TEMPLATE.render()
    fw=open('output.html','w')
    fw.write(template)
    fw.close()
    fr.close()

def studentTemplate(header,rows):
   
    stId = sys.argv[2]
    value = 0
    for row in rows:
        if row[0] == stId:
            value += int(row[2])
    if(value==0):
        TEMPLATE = wrongTemplate()
    else:
        TEMPLATE = h.html(
            h.head(
                h.title('Student Data')
            ),
            h.body(
                h.h1('Student Details'),
                h.table(border='1')(
                    h.tr(
                        h.th(cell) for cell in header
                    ),
                    (h.tr(
                        h.td(cell) for cell in row
                    ) for row in rows if row[0] == stId
                    ),
                    h.tr(
                        h.td(colspan='2')('Total Marks'),
                        h.td(value)
                    )
                )
            )
        )
    return TEMPLATE

def courseTemplate(rows):
    
    cId = sys.argv[2]
 
    value = 0
    max = 0
    data = {}
    for row in rows:
        
        if int(row[1]) == int(cId):
            i = int(row[2])
            
            if (i not in data.keys()):
                data[i] = 1
            else:
                data[i] += 1
            
            value += i
            if (i > max):
                max = i
    avg = value / len(rows)
    if (value == 0):
        TEMPLATE = wrongTemplate()
    else:
       
        courses = list(data.keys())
        values = list(data.values())
        fig = plt.figure(figsize=(10, 5))
        plt.bar(courses, values)
        plt.xlabel("Marks")
        plt.ylabel("Frequency")
        fig.savefig('my_plot.png')
        TEMPLATE = h.html(
            h.head(
                h.title('Course Data')
            ),
            h.body(
                h.h1('Course Details'),
                h.table(border='1')(
                    h.tr(
                        h.th('Average Marks'),
                        h.th('Maximum Marks')
                    ),
                    h.tr(
                        h.td(avg),
                        h.td(max)
                    )
                ),
                h.img(src='my_plot.png')
            )
        )
    return TEMPLATE

def wrongTemplate():
    return h.html(
            h.head(
                h.title('Something Went Wrong')
            ),
            h.body(
                h.h1('Wrong Inputs'),
                h.p('Something went wrong')
            )
        )

if __name__=='__main__':
    main()