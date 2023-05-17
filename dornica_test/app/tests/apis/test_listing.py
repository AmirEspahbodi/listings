import json

from fastapi.testclient import TestClient

from app.tests.utils.override import TestingSessionLocal
from app.tests.utils.user import  user_authentication_headers, get_random_user
from app.tests.utils.listing import get_random_listing
from app.core.config import settings

from app.main import app
from app.crud.user import user_crud
from app.crud.listing import listing_crud

client = TestClient(app)



global_user_in = get_random_user()
global_response = client.post(
    f"{settings.AUTH_ROUTE_PREFIX}/register/",
    content=global_user_in.json()
)
global_user_in2 = get_random_user()
global_response2 = client.post(
    f"{settings.AUTH_ROUTE_PREFIX}/register/",
    content=global_user_in2.json()
)
db = TestingSessionLocal()
global_user_db = user_crud.get_user(db, username=global_user_in.username)
global_user_db2 = user_crud.get_user(db, username=global_user_in2.username)
db.close()
headers = user_authentication_headers(client=client, username=global_user_in.username, password=global_user_in.password1)
headers2 = user_authentication_headers(client=client, username=global_user_in2.username, password=global_user_in2.password1)


def test_read_listings():
    listing_in = get_random_listing()

    response = client.post(
        "/listings/",
        content=listing_in.json(),
        headers=headers
    )
    response_get = client.get(
        "/listings/"
    )
    
    post_re_con = json.loads(response.content.decode('utf-8'))
    get_re_con = json.loads(response_get.content.decode('utf-8'))
    
    assert response.status_code == 201
    assert response_get.status_code == 200
    assert post_re_con in get_re_con


def test_read_single_listing():
    listing_in = get_random_listing()
    response = client.post(
        "/listings/",
        content=listing_in.json(),
        headers=headers
    )
    post_re_con = json.loads(response.content.decode('utf-8'))
    response_get = client.get(
        f"/listings/{post_re_con['id']}"
    )
    assert response.status_code == 201
    assert response_get.status_code == 200


def test_put_listing():
    listing_in = get_random_listing()
    response = client.post(
        "/listings/",
        content=listing_in.json(),
        headers=headers
    )
    post_re_con = json.loads(response.content.decode('utf-8'))
    listing_in = get_random_listing()
    response_put = client.put(
        f"/listings/{post_re_con['id']}",
        content=listing_in.json(),
        headers=headers
    )
    put_re_con = json.loads(response_put.content.decode('utf-8'))

    assert response.status_code == 201
    assert response_put.status_code == 200
    assert post_re_con['address'] != put_re_con['address']


def test_delete_listing():
    db = TestingSessionLocal()
    listing_in = get_random_listing()
    response = client.post(
        "/listings/",
        content=listing_in.json(),
        headers=headers
    )
    post_re_con = json.loads(response.content.decode('utf-8'))
    response_delete = client.delete(
        f"/listings/{post_re_con['id']}",
        headers=headers
    )
    listing_db = listing_crud.get(db, id=post_re_con['id'])

    db.close()
    assert response.status_code == 201
    assert response_delete.status_code == 200
    assert listing_db is None


def test_access_denied_put_listing():
    listing_in = get_random_listing()
    response = client.post(
        "/listings/",
        content=listing_in.json(),
        headers=headers
    )
    post_re_con = json.loads(response.content.decode('utf-8'))
    listing_in = get_random_listing()
    response_put = client.put(
        f"/listings/{post_re_con['id']}",
        headers=headers2,
        content=listing_in.json()
    )
    assert response.status_code == 201
    assert response_put.status_code == 403


def test_access_denied_delete_listing():
    listing_in = get_random_listing()
    response = client.post(
        "/listings/",
        content=listing_in.json(),
        headers=headers
    )
    post_re_con = json.loads(response.content.decode('utf-8'))
    response_delete = client.delete(
        f"/listings/{post_re_con['id']}",
        headers=headers2
    )
    assert response.status_code == 201
    assert response_delete.status_code == 403
