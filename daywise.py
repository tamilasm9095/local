from  main import  daywise,onlydaywise,SendMail,yesterday_str,df,removepdf,Mail

daywise(df)
SendMail(onlydaywise)

Mail('stselvan9095@gmail.com','bqbsvuepcyctpdui',['tamilselvan.s@asmltd.com'],[f'/home/ubuntu/democron/SmartFix_active_DaywiseReport_{yesterday_str}.pdf'],'customized Email','customized Email')


removepdf()



