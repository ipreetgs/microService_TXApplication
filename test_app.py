from app import app as main_app
from external_blog_app import external_blog_app

import pytest
from flask import url_for

@pytest.fixture
def client():
    main_app.config['TESTING'] = True
    client = main_app.test_client()

    yield client

def test_home_route(client):
    response = client.get('/')
    assert b"Welcome to the Home Page!" in response.data

def test_about_route(client):
    response = client.get('/about')
    assert b"Learn More About Us!" in response.data

def test_redirect_to_external_blog(client):
    response = client.get('/blog')
    assert response.status_code == 302  # 302 is the HTTP status code for redirection

def test_external_blog_home_route():
    external_client = external_blog_app.test_client()
    response = external_client.get('/')
    assert b"Welcome to the External Blog Home Page!" in response.data

def test_external_blog_post_route():
    external_client = external_blog_app.test_client()
    response = external_client.get('/post/1')
    assert b"Viewing Blog Post #1 on the External Blog App" in response.data
