from datetime import datetime
def successful_login_notification(username: str, message=""):
    print(f"successful login at {datetime.utcnow()} - {username}")

def increase_count_file():
    with open("count.txt", mode="r+") as count_file:
        content = count_file.read().strip().split('\n')
        number = int(0 if not content[0] else content[0]) + 1
        count_file.truncate(0)
        count_file.seek(0)
        count_file.write(f"{number}\n")
