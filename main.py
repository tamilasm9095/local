from Error_func  import  errorEmail
import traceback
from logger import logging
import datetime
today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)
yesterday_str = yesterday.strftime('%Y-%m-%d')
current_date =  yesterday_str
import  pandas as pd
df = pd.read_csv(f'/home/ubuntu/democron/{yesterday_str}.csv')
import  pandas as pd
try:
    df = pd.read_csv(f'/home/ubuntu/democron/{yesterday_str}.csv')
    logging.info('csv file read...')
except Exception as e:
    logging.critical('error while reading file from path...')

    subj = 'Error while reading file from path'
    error = traceback.format_exc()
    errorEmail(error, subj)

def daywise(df_pivot):  # Fetching data from database and make it to barchat and save as pdf with current date

    try:
        import pandas as pd
        import plotly.express as px
        pivot_table = df_pivot
        pivot_table.index = pd.to_datetime(pivot_table['resample_timestamp'])

        machines = sorted(
            [col for col in pivot_table.columns if "resample_timestamp" not in col]
        )

        start_date = pivot_table.index[0]
        end_date = pivot_table.index[-1]

        dates = pd.date_range(start_date, end_date)
        day = [f"day{i + 1}" for i in range(len(dates))]
        data = {"Day": day}
        for machine in machines:
            value = []
            for date in pd.date_range(start_date, end_date):
                date_str = yesterday_str
                df = pivot_table.loc[date_str]
                count = df[machine].count() // 60
                val = (count) / (24 * 60) * 100
                value.append(val)
            data[machine] = value
        df = pd.DataFrame(data)
        df_melted = df.melt(id_vars="Day", var_name="Machines", value_name="Efficiency")
        fig = px.bar(
            df_melted,
            x="Day",
            y="Efficiency",
            color="Machines",
            title=f"{date_str} Machine efficiencies",
            text="Efficiency",
        )
        fig.write_image(f"/home/ubuntu/democron/SmartFix_active_DaywiseReport_{date_str}.pdf", width=1800, height=1000)
        print('daywise pdf created')
        logging.info('daywise pdf created')
    except Exception as e:
        logging.critical('Error while creating daywise pdf')
        subj='Error at while Generating daywise pdf'
        logging.debug('debug')
        error = traceback.format_exc()
        print(error)
        errorEmail(error,subj)



def hourwise(df_pivot):
    try:
        import pandas as pd
        import plotly.express as px
        import datetime

        now = datetime.datetime.utcnow()
        import datetime
        from matplotlib.backends.backend_pdf import PdfPages
        import matplotlib.pyplot as plt
        import datetime

        today = datetime.date.today()
        date_str = today.strftime("%Y-%m-%d")

        today = datetime.date.today()
        file = df_pivot
        file.index = pd.to_datetime(file['resample_timestamp'])

        file = file.resample("1s").max()

        dt = pd.DatetimeIndex(file.index)

        machine_names = [col for col in file.columns]

        file["hour"] = dt.hour

        earliest_date = pd.to_datetime(file.index[0])
        latest_date = pd.to_datetime(file.index[-1])

        days = []
        for date in pd.date_range(start=earliest_date, end=latest_date):
            day = file.loc[date.strftime("%Y-%m-%d")]
            days.append(day)
        hourly_counts = {}
        for machine in machine_names:
            hourly_counts[machine] = []
            for day in days:
                hourly_count = day.groupby("hour")[machine].count() / 60
                hourly_counts[machine].append(hourly_count)
        daily_hourly_avgs = {}
        for machine, hourly_counts_list in hourly_counts.items():
            daily_hourly_avgs[machine] = []
            for i, hourly_counts in enumerate(hourly_counts_list):
                complete_hours = range(24)
                hourly_count = hourly_counts.reindex(complete_hours, fill_value=-1)
                daily_hourly_avgs[machine].append(hourly_count)
                if i == len(hourly_counts_list) - 1:
                    hourly_count_df = pd.concat(daily_hourly_avgs[machine], axis=1)
                    hourly_count_df.index = complete_hours
                    hourly_count_df.columns = range(len(daily_hourly_avgs[machine]))
                    hourly_count_mean = hourly_count_df.select_dtypes(
                        include="number"
                    ).mean(axis=1)
                    daily_hourly_avgs[machine] = hourly_count_mean
        with PdfPages(f"/home/ubuntu/democron/SmartFix_active_HourwiseReport_{yesterday_str}.pdf") as pdf_file:
            for machine in machine_names:
                hourly_avgs = daily_hourly_avgs[machine]
                fig, ax = plt.subplots()
                bars = ax.bar(range(24), hourly_avgs / 60 * 100)
                ax.set_xticks(range(24))
                ax.set_xlabel("Hour")
                ax.set_ylabel("Efficiency")
                ax.set_title(f"Hourly Efficiency for {machine}")
                ax.set_ylim([0, 100])
                for bar in bars:
                    height = bar.get_height()
                    ax.text(
                        bar.get_x() + bar.get_width() / 2.0,
                        height / 2,
                        "%.1f%%" % height,
                        ha="center",
                        va="center",
                        color="white",
                        fontsize=8,
                    )
                # Change the figure size here if desired:
                fig.set_size_inches(18, 10)
                pdf_file.savefig(fig)
        print('hourwise pdf created')
        logging.info('hourwise pdf created')

    except Exception as e:
        logging.critical('Error at while Generating hourwise pdf')
        subj = 'Error at while Generating hourwise pdf'
        error = traceback.format_exc()
        errorEmail(error,subj)







from datetime import datetime

current_date = datetime.today().strftime('%Y-%m-%d')
import os





onlydaywise = {
    'sender': 'tamilasm9095@gmail.com',
    'key': 'esxxurifnzqvljsd',
    'reciverlist': ['tamilselvan.s@asmltd.com', 'stselvan9095@gmail.com'],
    'file_path': [f'/home/ubuntu/democron/SmartFix_active_DaywiseReport_{yesterday_str}.pdf'],
    'body': f"""
Hi all,

Please find the attachment displaying the analytics procured from SmartFix for the day {yesterday_str}.

Kindly reach out the SmartFix team for any queries.


Disclaimer: This is an auto-generated email, hence please do not respond to this email.

""",
    'sub': f'SmartFix_active_DaywiseReport_{yesterday_str}.pdf'
}  # Receiver can get only daywise chart

onlyhourwise = {
    'sender': 'tamilasm9095@gmail.com',
    'key': 'esxxurifnzqvljsd',
    'reciverlist': ['tamilselvan.s@asmltd.com', 'tamilasm9095@gmail.com'],
    'file_path': [f'/home/ubuntu/democron/SmartFix_active_HourwiseReport_{yesterday_str}.pdf'],
    'body': f"""
Hi all,

Please find the attachment displaying the analytics procured from SmartFix for the day {yesterday_str}.

Kindly reach out the SmartFix team for any queries.


Disclaimer: This is an auto-generated email, hence please do not respond to this email.

""",
    'sub': f'SmartFix_active_HourwiseReport_{yesterday_str}.pdf'
}  # Receiver can get only hourwise chart

combainedpdf = {
    'sender': 'tamilasm9095@gmail.com',
    'key': 'esxxurifnzqvljsd',
    'reciverlist': ['tamilselvan.s@asmltd.com', 'tamilasm9095@gmail.com'],
    'file_path': [f'/home/ubuntu/democron/SmartFix_active_DayandHourwise_{yesterday_str}.pdf'],
    'body': f"""
Hi all,

Please find the attachment displaying the analytics procured from SmartFix for the day {yesterday_str}.

Kindly reach out the SmartFix team for any queries.


Disclaimer: This is an auto-generated email, hence please do not respond to this email.

""",
    'sub': f'SmartFix_active_DayandHourwise_{yesterday_str}.pdf'
}  # Receiver can get merged chart both daywise chart and hourwise chart such sd merged.pdf

separatefilepdf = {
    'sender': 'tamilasm9095@gmail.com',
    'key': 'esxxurifnzqvljsd',
    'reciverlist': ['tamilselvan.s@asmltd.com', 'tamilasm9095@gmail.com'],
    'file_path': [f'/home/ubuntu/democron/SmartFix_active_HourwiseReport_{yesterday_str}.pdf', f'/home/ubuntu/democron/SmartFix_active_DaywiseReport_{yesterday_str}.pdf'],
    'body': f"""
Hi all,

Please find the attachment displaying the analytics procured from SmartFix for the day {yesterday_str}.

Kindly reach out the SmartFix team for any queries.


Disclaimer: This is an auto-generated email, hence please do not respond to this email.

""",
    'sub': f'SmartFix_active_Hourwise,DaywiseReport_{yesterday_str}.pdf'
}  # Receiver can get two pdf's such as daywise.pdf and hourwise.pdf


# send mail function
def SendMail(template):  # separte file
    try:
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        from email.mime.application import MIMEApplication

        # Set up email information
        from_address = template['sender']
        to_address = template['reciverlist']
        subject = template['sub']
        body = template['body']
        files = template['file_path']

        # Create a multi-part email message
        msg = MIMEMultipart()
        msg['From'] = from_address
        msg['To'] = ', '.join(to_address)
        msg['Subject'] = subject

        # Attach the message body
        msg.attach(MIMEText(body))

        # Attach the files
        for file in files:
            with open(file, 'rb') as f:
                attachment = MIMEApplication(f.read(), _subtype='pdf')
                attachment.add_header('Content-Disposition', 'attachment', filename=file[22:])
                msg.attach(attachment)

        # Connect to SMTP server and send the email
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        smtp_username = template['sender']
        smtp_password = template['key']

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(from_address, to_address, msg.as_string())

        print('Email sent successfully.')
        logging.info('Email sent successfully.')

    except Exception as e:
        logging.exception('send email function failed')
        subj = 'send email function failed'
        error = traceback.format_exc()
        errorEmail(error, subj)

def Mail(sender,key,recivers_list,file_path,body,sub):  # separte file
    try:
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        from email.mime.application import MIMEApplication

        # Set up email information
        from_address = sender
        to_address = recivers_list
        subject = sub
        body = body
        files = file_path

        # Create a multi-part email message
        msg = MIMEMultipart()
        msg['From'] = from_address
        msg['To'] = ', '.join(to_address)
        msg['Subject'] = subject

        # Attach the message body
        msg.attach(MIMEText(body))

        # Attach the files
        for file in files:
            with open(file, 'rb') as f:
                attachment = MIMEApplication(f.read(), _subtype='pdf')
                attachment.add_header('Content-Disposition', 'attachment', filename=file[22:])
                msg.attach(attachment)

        # Connect to SMTP server and send the email
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        smtp_username = sender
        smtp_password = key

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(from_address, to_address, msg.as_string())

        print('Email sent successfully without template.')
        logging.info('Email sent successfully without template.')

    except Exception as e:
        logging.critical('without template Email func failed')
        subj = 'Without Email function failed'
        error = traceback.format_exc()
        errorEmail(error, subj)



# Mail('stselvan9095@gmail.com','bqbsvuepcyctpdui',['tamilselvan.s@asmltd.com'],[f'SmartFix_active_DaywiseReport_{yesterday_str}.pdf'],'Body of the mail , without  template','without  template')

#Mail(sender,key,recivers_list,file,body,sub)

def removepdf():
    try:
        for file in os.listdir("."):
            if file.endswith(".pdf"):
                os.remove(file)
        logging.info('pdf files are removed from path')
    except Exception as e:
        logging.critical('fail while removeing pdf file')
        subj = 'fail while removeing pdf file'
        error = traceback.format_exc()
        errorEmail(error, subj)

