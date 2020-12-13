import pytest
from mixer.backend.django import mixer
from django.test import RequestFactory

@pytest.fixture(scope='module')
def factory():
    fact = RequestFactory()
    return fact

@pytest.fixture
def item1(db):
    item1 = mixer.blend('item.Item', name='item one')
    return item1

@pytest.fixture
def item2(db):
    item2 = mixer.blend('item.Item', name='item two')
    return item2

@pytest.fixture
def item3(db):
    item3 = mixer.blend('item.Item', name='item three')
    return item3

@pytest.fixture
def item4(db, category1, shelf1):
    item4 = mixer.blend('item.Item', name='item four', category=category1, item_sage_id='001', \
        description='forth item', unit='pcs', sub_category='plumbing', shelf_lbl=shelf1 , \
            reorder_quantity=5, status='in stock', recent=False)
    return item4

@pytest.fixture
def image1(db, item1):
    img1 = mixer.blend('item.Image', item=item1, featured=False, image='img.jpg')
    return img1

@pytest.fixture
def location1(db):
    loc1 = mixer.blend('item.Location', name='location one', summary='first location')
    return loc1

@pytest.fixture
def project1(db, department1):
    proc1 = mixer.blend('item.Project', name='project one', department=department1)
    return proc1

@pytest.fixture
def department1(db):
    dept1 = mixer.blend('item.Department', name='dept one', hod='hod 1')
    return dept1

@pytest.fixture
def category1(db):
    cat1 = mixer.blend('item.Category', name='cat one', summary='first category')
    return cat1

@pytest.fixture
def shelf1(db, location1):
    shelf = mixer.blend('item.Shelf', name='shelf a', location=location1)
    return shelf

@pytest.fixture
def receive1(item1, project1):
    return mixer.blend('item.Receive',item=item1, quantity=100, project=project1)

@pytest.fixture
def receive2(item2):
    return mixer.blend('item.Receive',item=item2, quantity=100)

@pytest.fixture
def receive3(item3, project1):
    return mixer.blend('item.Receive',item=item3, quantity=100, project=project1, delivery_mode='road', \
        receive_by='worker b', status='damaged')

@pytest.fixture
def receive4(item1):
    return mixer.blend('item.Receive',item=item1, quantity=50)

@pytest.fixture
def receive5(item1, project1):
    return mixer.blend('item.Receive',item=item1, quantity=100, project=project1)

@pytest.fixture
def issue1(item2, project1):
    return mixer.blend('item.Issue',item=item2, quantity=50, project=project1)

@pytest.fixture
def issue2(item1, project1):
    return mixer.blend('item.Issue',item=item1, quantity=100, purpose='work a', issued_to='worker one', \
         issue_type='online', project=project1)

@pytest.fixture
def issue3(item3, project1):
    return mixer.blend('item.Issue',item=item3, quantity=50, project=project1)

@pytest.fixture
def issue4(item2):
    return mixer.blend('item.Issue',item=item2, quantity=50)

@pytest.fixture
def spreturn1(receive3):
    return mixer.blend('item.ReturnToSupplier',item=receive3, quantity=10, reason='damaged', return_by='driver a')

@pytest.fixture
def streturn1(issue3):
    return mixer.blend('item.ReturnToStore',item=issue3, quantity=5, reason='damaged', return_by='worker a')

