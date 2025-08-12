from passenger_wsgi import application

def test_application_is_flask_app():
    assert hasattr(application, 'route')
