from auth.main import Database
from typing import Any

from auth.models import UserDto, RequestDto

d: dict[str, Any] = {}

if __name__ == '__main__':
    db = Database()
    d["user1"] = db.post_user(UserDto("aagonua", "test@gmail.com", "12345"))
    user_id = d["user1"].id
    assert db.get_user(user_id) == d["user1"], "same users are not equal"
    d["request1"] = db.post_request(RequestDto(user_id, "input1", "output1"))
    d["request2"] = db.post_request(RequestDto(user_id, "input2", "output2"))
    assert db.get_all_requests_by_user_id(user_id) == [d['request1'], d["request2"]]


