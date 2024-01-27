import smtplib

my_dummy_email = "r9024166@gmail.com"
temp_passwd = "zwaj lzkx ldfb mhpx"

connection = smtplib.SMTP("smtp.gmail.com")  # SMTP Server connect
connection.starttls()  # Secure connection through TLS
connection.login(user=my_dummy_email, password=temp_passwd)


recepient_email = "rav73107@gmail.com"
content = "Greetings senor, this is the first step on the path to World domination!!!!" \
          "\n" \
          "Veni, Vidi, Vici..."
subject = "Automated quote for the day"
message = 'Subject: {}\n\n{}'.format(subject, content)
connection.sendmail(from_addr=my_dummy_email, to_addrs=recepient_email, msg=message)
connection.close()