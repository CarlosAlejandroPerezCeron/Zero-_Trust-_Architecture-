from app.auth import create_token, verify_token

def test_token_creation():
    token = create_token("user1")
    assert isinstance(token, str)

def test_token_verification():
    token = create_token("user2")
    user = verify_token(token)
    assert user == "user2"
