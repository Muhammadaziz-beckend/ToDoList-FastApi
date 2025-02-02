


class ServerRun:
    port:int=8000
    host:str="127.0.0.1"



class BaseSettings(ServerRun):
    pass


settings = BaseSettings()