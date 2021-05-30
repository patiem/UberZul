import datetime


class DataBase:
    def __init__(self, filename):
        self.filename = filename
        self.users = None
        self.file = None
        self.load()

    def load(self):
        self.file = open(self.filename, "r")
        self.users = {}

        for line in self.file:
            email, password, name, created = line.strip().split(";")
            self.users[email] = (password, name, created)

        self.file.close()

    def get_user(self, email):
        if email in self.users:
            return self.users[email]
        else:
            return -1

    def add_user(self, email, password, name):
        if email.strip() not in self.users:
            self.users[email.strip()] = (password.strip(), name.strip(), DataBase.get_date())
            self.save()
            return 1
        else:
            print("Email exists already")
            return -1

    def validate(self, email, password):
        if self.get_user(email) != -1:
            return self.users[email][0] == password
        else:
            return False

    def save(self):
        with open(self.filename, "w") as f:
            for user in self.users:
                f.write(user + ";" + self.users[user][0] + ";" + self.users[user][1] + ";" + self.users[user][2] + "\n")

    @staticmethod
    def get_date():
        return str(datetime.datetime.now()).split(" ")[0]


class Notice:
    """ Representation of a notice- entity added by the user to the database
    """
    def __init__(self, name=None, whom=None, job_type=None, price_value=None):
        self.name = name
        self.whom = whom
        self.job_type = job_type
        self.price_value = price_value
        self.notices = None
        self.file = None

    def load(self):
        self.file = open("notice.txt", "r")
        self.notices = {}

        for line in self.file:
            id, name, user, job_type, price_value = line.strip().split(";")
            self.notices[id] = (name, user, job_type, price_value)

        self.file.close()

    def get_notice(self, id):
        if id in self.notices:
            return self.notices[id]
        else:
            return -1

    def get_notices(self):
        return self.notices