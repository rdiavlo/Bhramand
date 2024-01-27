import smtplib

from main import get_amazon_product_params

my_dummy_email = "r9024166@gmail.com"
temp_passwd = "zwaj lzkx ldfb mhpx"
recepient_email = "rav73107@gmail.com"

connection = smtplib.SMTP("smtp.gmail.com")  # SMTP Server connect
connection.starttls()                        # Secure connection through TLS
connection.login(user=my_dummy_email, password=temp_passwd)



def send_email(message):



    content = f"Greetings senor, this is the first step on the path to World domination!!!!" \
              "\n\n" \
              f"{output_product_details_string}"
    subject = f"Amazon price tracker quote for product on {res[1]} "
    message = 'Subject: {}\n\n{}'.format(subject, content)
    connection.sendmail(from_addr=my_dummy_email, to_addrs=recepient_email, msg=message)
    connection.close()
    print("The email has been sent !!!")