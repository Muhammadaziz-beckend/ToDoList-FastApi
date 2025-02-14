class ServerRun:
    port:int=8000
    host:str="127.0.0.1"

class SwaggerTitele:
    PROJECT_NAME = "TodoList API"

class BaseSettings(ServerRun,SwaggerTitele):
    pass


settings = BaseSettings()