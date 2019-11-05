from datetime import datetime


class Logfile(object):

    def __init__(self, file_name = "file.log"):
        self.file_name = file_name
        

    def write_to_file(self, data: str, file_name = None):
        

        if file_name is None:
            server = "server"
            file_name = self.file_name
    
        with open(file_name, "a", encoding="utf-8") as f:
            print(f"{data} {datetime.now().time()}", file=f)

    def serverstart(self):
        self.write_to_file(" connection was started at")

    def serverend(self):  
        self.write_to_file(" connection was stopped")


