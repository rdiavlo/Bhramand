from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText





import sys
import smtplib
import email
import re

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def sendmail(firm, fromEmail, to, template, subject, date):
    with open(template, encoding="utf-8") as template_file:
        message = template_file.read()

    msg = MIMEMultipart("alternative")
    msg["Subject"] = u'テストメール'
    part1 = MIMEText(u'\u3053\u3093\u306b\u3061\u306f\u3001\u4e16\u754c\uff01\n',
                     "plain", "utf-8")
    msg.attach(part1)

    msg.as_string().encode('ascii')


    msg.as_string().encode('ascii')



    msg = MIMEMultipart("alternative")
    msg.set_charset("utf-8")

    msg["Subject"] = subject
    msg["From"] = fromEmail
    msg["To"] = to





    msg.attach(part1)
    msg.attach(part2)

    try:
        server = smtplib.SMTP("10.0.0.5")
        server.sendmail(fromEmail, [to], msg.as_string())
        return 0
    except Exception as ex:
        # log error
        # return -1
        # debug
        raise ex
    finally:
        server.quit()


if __name__ == "__main__":
    # debug
    sys.argv.append("Moje")
    sys.argv.append("newsletter@example.cz")
    sys.argv.append("subscriber@example.com")
    sys.argv.append("may2011.template")
    sys.argv.append("This is subject")
    sys.argv.append("This is date")

    if len(sys.argv) != 7:
        exit(-2)

    firm = sys.argv[1]
    fromEmail = sys.argv[2]
    to = sys.argv[3]
    template = sys.argv[4]
    subject = sys.argv[5]
    date = sys.argv[6]