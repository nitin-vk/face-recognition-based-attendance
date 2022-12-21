import xlsxwriter
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
            s+=1
            r+=1
        workbook.close()
        
