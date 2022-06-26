import requests
import datetime as dt
import smtplib
import time

MY_LAT = 13.339168
MY_LONG = 77.113998

my_email = "abeingboss@gmail.com"
password = "my@password"


def is_iss_overhead():
    iss_response = requests.get("http://api.open-notify.org/iss-now.json")
    iss_response.raise_for_status()

    iss_data = iss_response.json()
    iss_latitude = float(iss_data["iss_position"]["latitude"])
    iss_longitude = float(iss_data["iss_position"]["longitude"])

    if MY_LAT-5 <= iss_latitude <= MY_LAT+5 and MY_LONG-5 <= iss_longitude <= MY_LONG+5:
        return True


def is_dark():
    params = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=params)
    response.raise_for_status()

    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    now = dt.datetime.now().hour

    if now >= sunset or now <= sunrise:
        return True


while True:
    time.sleep(60)
    if is_iss_overhead() and is_dark():
        with smtplib.SMTP() as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(from_addr=my_email,
                                to_addrs="sanjaypm09@gmail.com",
                                msg="Subject:Look Up!\n\nThe ISS is above you in the Sky.")
