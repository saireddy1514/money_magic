from django.urls import reverse,resolve

class TestUrls:
    def test_detailurl(self):
        path=reverse('inbox')
        assert resolve(path).view_name=='inbox'
    

