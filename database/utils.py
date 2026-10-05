from pydantic import BaseModel

class Message(BaseModel):
    author: str
    text: str

    def to_dict(self) -> dict:
        return {"author": self.author, "text": self.text}

    def to_list(self) -> list:
        return [self.author, self.text]