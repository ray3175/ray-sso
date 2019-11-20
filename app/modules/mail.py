from sqlalchemy import Column, ForeignKey, String, BigInteger
from sqlalchemy.orm import relationship
from ..lib.database.base import Base


class Mail(Base):
    __tablename__ = "mail"

    id = Column(BigInteger, primary_key=True, comment="用户邮箱ID")
    mail = Column(String(128), comment="用户邮箱")
    person_id = Column(BigInteger, ForeignKey("person.id", ondelete="CASCADE"), index=True, comment="用户ID")
    person = relationship("Person", backref="mail_from_person")

