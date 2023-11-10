import pytest
from flask import url_for
from requests import get

@pytest.fixture
def client():
    from app import app as main_app
    main_app.config['TESTING'] = True
    client = main_app.test_client()

    yield client

def test_home_route(client):
    response = client.get('/')
    assert b"Welcome to the Home Page!" in response.data

def test_about_route(client):
    response = client.get('/about')
    assert b"Learn More About Us!" in response.data

def test_redirect_to_external_blog():
    # Assuming the external blog app is running in a different Docker container
    external_blog_url = 'http://flask-blog-app:5000'  # Adjust the URL accordingly

    response = get(external_blog_url)
    assert response.status_code == 200  # Assuming a successful response

def test_external_blog_post_route():
    # Assuming the external blog app is running in a different Docker container
    external_blog_url = 'http://flask-blog-app:5000'  # Adjust the URL accordingly

    response = get(f'{external_blog_url}/post/1')
    assert b"Viewing Blog Post #1 on the External Blog App" in response.content
