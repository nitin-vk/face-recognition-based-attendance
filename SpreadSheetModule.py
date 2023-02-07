import xlsxwriter
import openpyxl
class SpreadSheetModule():
    def __init__(self,people):
        self.people =people

    def createSpreadSheet(self,dir):
        workbook = xlsxwriter.Workbook(dir,{'in_memory':True})
        worksheet = workbook.add_worksheet()
 
        worksheet.write('A1', 'USN')
        worksheet.write('B1', 'Name')
        worksheet.write('C1', 'Status')
        worksheet.write('D1', 'Total')

        s=0
        r=1
        while s<len(self.people):
            worksheet.write(r,1,self.people[s])
            worksheet.write(r,3,0)
            s+=1
            r+=1
        workbook.close()

    def updateSpreadSheet(self,peoplePresent,dir):
        #print("from spreadsheet {}".format(peoplePresent))
        wb_obj=openpyxl.load_workbook(dir)
        sheet=wb_obj.active
        last_empty_row=len(list(sheet.rows))
        #print(last_empty_row)
        for j in peoplePresent:
            if (sum(peoplePresent[j])/len(peoplePresent[j]))<=55:
                for i in range(2,last_empty_row+1):
                    if sheet.cell(row=i,column=2).value==j:
                        sheet.cell(row=i,column=3).value='P'
                        sheet.cell(row=i,column=4).value=sheet.cell(row=i,column=4).value+1
                        break
                    
            elif (sum(peoplePresent[j])/len(peoplePresent[j]))>55:
                for i in range(2,last_empty_row+1):
                    if sheet.cell(row=i,column=2).value==j:
                        sheet.cell(row=i,column=3).value='A'
                        break
                
                    
        wb_obj.save(dir)


            
        

        
