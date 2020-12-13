from mixer.backend.django import mixer
import pytest

# 1. ============================ TESTING MODELS FIELDS =====================================

def test_category_model_fields(category1):
    assert category1.name == 'cat one'
    assert category1.summary == 'first category'

def test_location_model_fields(location1):
    assert location1.name == 'location one'
    assert location1.summary == 'first location'

def test_shelf_model_fields(shelf1, location1):
    assert shelf1.name == 'shelf a'
    assert shelf1.location == location1

def test_item_model_fields(item4, category1, shelf1):
    assert item4.name == 'item four'
    assert item4.category == category1
    assert item4.item_sage_id == '001'
    assert item4.description == 'forth item'
    assert item4.unit == 'pcs'
    assert item4.sub_category == 'plumbing'
    assert item4.shelf_lbl == shelf1
    assert item4.reorder_quantity == 5
    assert item4.status == 'in stock'
    assert item4.recent == False

def test_image_model_fields(image1, item1):
    assert image1.item == item1
    assert image1.featured == False
    assert image1.image == 'img.jpg'

def test_receive_model_fields(receive3, project1, item3):
    assert receive3.item == item3
    assert receive3.project == project1
    assert receive3.status == 'damaged'
    assert receive3.quantity == 100
    assert receive3.receive_by == 'worker b'
    assert receive3.delivery_mode == 'road'

def test_issue_model_fields(issue2, project1, item1):
    assert issue2.item == item1
    assert issue2.project == project1
    assert issue2.purpose == 'work a'
    assert issue2.quantity == 100
    assert issue2.issued_to == 'worker one'
    assert issue2.issue_type == 'online'

def test_returntostore_model_fields(issue3, streturn1):
    assert streturn1.item == issue3
    assert streturn1.quantity == 5
    assert streturn1.reason == 'damaged'
    assert streturn1.return_by == 'worker a'

def test_returntosupllier_model_fields(receive3, spreturn1):
    assert spreturn1.item == receive3
    assert spreturn1.quantity == 10
    assert spreturn1.reason == 'damaged'
    assert spreturn1.return_by == 'driver a'
    
def test_department_model_fields(department1):
    assert department1.name == 'dept one'
    assert department1.hod == 'hod 1'

def test_project_model_fields(project1, department1):
    assert project1.name == 'project one'
    assert project1.department == department1
    assert project1.completed == False

def test_category_str_method(category1):
    assert str(category1) == 'cat one'

def test_location_str_method(location1):
    assert str(location1) == 'location one'

def test_shelf_str_method(shelf1):
    assert str(shelf1) == 'shelf a'

def test_item_str_method(item1):
    assert str(item1) == 'item one'

def test_image_str_method(image1):
    assert str(image1) == 'item one'

def test_receive_str_method(receive1):
    assert str(receive1) == 'item one - 100'

def test_issue_str_method(issue1):
    assert str(issue1) == 'item two - 50'

def test_return_to_store_str_method(streturn1):
    assert str(streturn1) == 'item three - 5'

def test_return_to_supplier_str_method(spreturn1):
    assert str(spreturn1) == 'item three - 10'

def test_department_str_method(department1):
    assert str(department1) == 'dept one'

def test_project_str_method(project1):
    assert str(project1) == 'project one'

# item3 balance: receive3=100, issue3=50
def test_item_get_total_balance(item3, receive3, issue3, spreturn1, streturn1):
    assert item3.get_total_balance == 45

#  is_in_stock() >> return True when stock > 0
def test_item_is_in_stock(item3, receive3, issue3):
    assert item3.is_in_stock() == True

# get_total_balance >> received=0, issued=0
def test_item_get_zero_balance(item4):
    assert item4.get_total_balance == 0

#  is_in_stock() >> return False when stock <= 0
def test_item_is_not_in_stock(item2, receive2, issue1, issue4):
    assert item2.is_in_stock() == False

def test_item_slug_generated_on_creation(item4):
    assert item4.slug == 'item-four'

# get_absolute_url() >> reverse('detail', kwargs={'slug':'self.slug'})
def test_item_get_absolute_url(item4):
    assert item4.get_absolute_url() == f'/detail/{item4.slug}'

# get_add_to_cart_url() >> reverse('cart:add-to-cart', kwargs={'slug':'self.slug'})
def test_item_get_add_to_cart_url(item4):
    assert item4.get_add_to_cart_url() == f'/cart/add-to-cart/{item4.slug}/'

# get_remove_from_cart_url() >> reverse('cart:remove-from-cart', kwargs={'slug':'self.slug'})
def test_item_get_remove_from_cart_url(item4):
    assert item4.get_remove_from_cart_url() == f'/cart/remove-from-cart/{item4.slug}/'

# 2.====================== TESTING Receive MODEL METHODS ====================================

#  get_total_received >> return total quantity of item received
def test_get_total_received(item1, receive1, receive4):
    assert item1.get_total_received == 150

def test_get_total_return_to_supplier(item3, spreturn1):
    assert item3.get_total_returned_to_supplier == 10

def test_get_total_return_to_store(item3, streturn1):
    assert item3.get_total_returned_to_store == 5

#  get_total_received_for_project >> return total quantity of item received for a specific project
def test_for_project_items(project1, item1, receive5):
    assert item1 in project1.project_items()
    
# 3.======================== TESTING Issue MODEL METHODS =======================================

def test_get_total_issued(item2, issue1, issue4):
    assert item2.get_total_issued == 100

    

# 4. ======================= TESTING Slug CREATION ON SAVE =======================================

def test_location_slug_generated_on_creation(location1):
    assert location1.slug == 'location-one'

def test_category_slug_generated_on_creation(category1):
    assert category1.slug == 'cat-one'

def test_project_slug_created_on_save(project1):
    assert project1.slug == 'project-one'

def test_department_slug_created_on_save(department1):
    assert department1.slug == 'dept-one'

    
