from bcrypt import hashpw, gensalt, checkpw

class Hash:
    @staticmethod
    def bcrypt(password: str) -> str:
        return hashpw(password.encode('utf-8'), gensalt()).decode('utf-8')
    
    @staticmethod
    def verify(plain_password: str, hashed_password: str) -> bool:
        return checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
