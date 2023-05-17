from  main import  daywise,combainedpdf
from  main import  hourwise,SendMail,yesterday_str,df,separatefilepdf,removepdf

daywise(df)
'''
push_s3(f'SmartFix_active_DaywiseReport_{yesterday_str}.pdf','daywisepdf')
hourwise(df)
push_s3(f'SmartFix_active_HourwiseReport_{yesterday_str}.pdf','hourwisepdf')
'''
from pypdf import PdfMerger

pdfs = [f"/home/ubuntu/democron/SmartFix_active_DaywiseReport_{yesterday_str}.pdf", f"/home/ubuntu/democron/SmartFix_active_HourwiseReport_{yesterday_str}.pdf"]
merger = PdfMerger()
for pdf in pdfs:
    merger.append(pdf)
merger.write(
    f"/home/ubuntu/democron/SmartFix_active_DayandHourwise_{yesterday_str}.pdf"
)
print("day and hourwise pdf's merged")
merger.close()

SendMail(combainedpdf)
removepdf()