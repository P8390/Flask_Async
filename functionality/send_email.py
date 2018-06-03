from constants.common_constants import FROM_ADDR, SUBJECT, CC
from flask_models.send_email import SystemEmailLog
from flask_models.users import User
from database import session
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email(**kwargs):
    from_address = FROM_ADDR
    to_address = kwargs.get('email')

    user_id = session.query(User.id).filter(User.email == to_address).first()
    if not user_id:
        raise ValueError("Enter Valid Email")

    msg = MIMEMultipart('alternative')
    msg['Subject'] = SUBJECT
    msg['From'] = from_address
    msg['To'] = to_address

    text = "Your Account for "+ to_address + " is successfully created \n \n Thanks \n Flask Blog"
    p1 = MIMEText(text, 'plain')

    msg.attach(p1)

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login("pankaj@screen-magic.com", "Pankaj154!")
    s.sendmail(from_address, to_address, msg.as_string())
    s.quit()

    email_obj = SystemEmailLog(
        user_id=user_id,
        from_address=from_address,
        to_address=to_address,
        cc=CC,
        subject=SUBJECT,
        message_body=kwargs,
        status=1
    )
    session.add(email_obj)
    session.commit()
