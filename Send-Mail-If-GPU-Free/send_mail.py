#coding:utf -8
 
import smtplib
from email.mime.text import MIMEText
import re
import os
import time

def send_mail(content):
    subject = "GPU Free MessageBox"
    sender = "<your_163_email_address>"
    recver = "<your_163_email_address>"
    password = "<your_password>"
    message = MIMEText(content, "plain", "utf-8")
    
    message['Subject'] = subject
    message['To'] = recver
    message['From'] = sender
    
    smtp = smtplib.SMTP_SSL("smtp.163.com", 994)
    smtp.login(sender, password)
    smtp.sendmail(sender, [recver], message.as_string())
    smtp.close()


if __name__ == '__main__':
    FREE_THRESHOLD = 1000
    pattern = re.compile('(\d+)MiB / (\d+)MiB')
    pattern1 = re.compile('    ([0-9]) ')
    pattern2 = re.compile('(\d+)      [CG]')
    pattern3 = re.compile('  (\d+)MiB \|')
    
    last_send_time = 0.0
    while True:
        results = os.popen('nvidia-smi')
        res = results.read()
        matches = pattern.findall(res)
        matches1 = pattern1.findall(res)  # GPU ID
        matches2 = pattern2.findall(res)  # PID
        matches3 = pattern3.findall(res)  # GPU memory usage

        lines = res.split('\n')

        free = False
        for i, mat in enumerate(matches):
            if int(mat[0]) < FREE_THRESHOLD:
                free = True
                break
        
        if free and (time.time() - last_send_time >= 3600.0):
            last_send_time = time.time()
            content = 'GPU memory usage:\n'
            for i, mat in enumerate(matches):
                content += 'GPU {}: {}/{}\n'.format(i, mat[0], mat[1])

            content += 'GPU memory usage detail:\n'
            for (gid, pid, use) in zip(matches1, matches2, matches3):
                lines = os.popen('ps aux | grep %s' % (pid)).readlines()
                for line in lines:
                    if pid == line.split()[1]:
                        username = line.split()[0]
                        content += ('gpu id: %s, user name: %-10s, used: %sM\n' % (gid, username, use))
                        break

            send_mail(content)
            localtime = time.asctime(time.localtime(time.time()))
            print('send time:', localtime)
