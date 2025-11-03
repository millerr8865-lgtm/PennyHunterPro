# REMOVE OLD send_sms
# ADD THIS INSTEAD (uses global from app.py)
def send_sms(title, url, score):
    from app import user_phone
    if not user_phone:
        print("No phone number set!")
        return
    message = f"PENNY ALERT: {title} $0.01 (Score: {score}) → {url}"
    client.messages.create(body=message, from_=twilio_number, to=user_phone)
    print(f"SMS SENT to {user_phone}: {message}")
