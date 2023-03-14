from influxdb import InfluxDBClient

class InfluxController:


  def __init__(self, host, port, username, password, database):
    self.host = host
    self.port = port
    self.username = username
    self.password = password
    self.database = database
    self.client = None

    def connect(self):
        self.client = InfluxDBClient(host=self.host, port=self.port, username=self.username, password=self.password,
                                     database=self.database)
        self.client.create_database(self.database)