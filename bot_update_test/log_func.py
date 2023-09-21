import datetime


def write_log(message):
    now = datetime.datetime.now()
    actual_hour = now.strftime("%Y-%m-%d %H:%M:%S")
    final_message = f"[{actual_hour}] {message}"

    with open('log.txt', 'a') as file:
        file.write(final_message + '\n')
