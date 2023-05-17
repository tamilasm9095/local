from  main import  daywise,SendMail,yesterday_str,df
from  main import  hourwise,SendMail,yesterday_str,df,separatefilepdf,removepdf

daywise(df)

'''
push_s3(f'SmartFix_active_DaywiseReport_{yesterday_str}.pdf','daywisepdf')

push_s3(f'SmartFix_active_HourwiseReport_{yesterday_str}.pdf','hourwisepdf')
'''
hourwise(df)
SendMail(separatefilepdf)
removepdf()