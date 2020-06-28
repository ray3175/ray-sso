from xy.utils.time import Time
from ...lib.database import DB
from ...dao.we_chat.user import DaoWeChatUser
from .. import Service
from ..user import ServiceUser
from ..person import ServicePerson
from ..phone import ServicePhone
from ..mail import ServiceMail


class ServiceWeChatUser(Service):
    def __init__(self, dao=DaoWeChatUser):
        super().__init__(dao)

    @DB.transaction(auto_commit=False)
    def get_user_with_account(self, account, xy=None, **kwargs):
        return ServiceUser().get_user_with_account(account, xy, **kwargs)

    @DB.transaction(auto_commit=False)
    def get_we_chat_user_with_openid(self, openid, **kwargs):
        return (we_chat_user:=self.dao.get_we_chat_user_with_openid(openid)) and we_chat_user(add_column=["person", "user", "phone", "mail"])

    @DB.transaction
    def add_we_chat_user_with_openid(self, openid, account, password, id_card, name, sex, birth_date, birth_place, native_place, nationality, phone, mail, **kwargs):
        person_id = person.id if (person:=ServicePerson().get_person_obj_with_id_card(id_card, **kwargs)) else ServicePerson().add_person(id_card, name, sex, birth_date, birth_place, native_place, nationality, **kwargs)["id"]
        if phone:
            ServicePhone().add({"phone": phone, "person_id": person_id}, **kwargs)
        if mail:
            ServiceMail().add({"mail": mail, "person_id": person_id}, **kwargs)
        if account and password:
            ServiceUser().add({"account": account, "password": password, "person_id": person_id, "register_time": Time().to_string()}, **kwargs)
        return self.add_we_chat_user(openid, person_id, **kwargs)

    @DB.transaction
    def add_we_chat_user(self, openid, person_id, **kwargs):
        return self.dao.add({"openid": openid, "person_id": person_id, "register_time": Time().to_string()})


