from types import SimpleNamespace 
# 创建一个简单对象，允许你用obj.attr访问数据，用于Mock（模拟对象）、打包参数或者临时存储一些相关数据
import pytest

# pytest.fixture是“后勤组（道具师）”：负责在来拍前把场景布置好（准备数据、 建立连接），拍完后负责清理现场。
# mock.Mock()是“替身演员”：当真正的演员（比如真实的数据库、 第三方支付接口）太贵、太危险或还没到场时，用这个家人代替它出镜。负责模拟行为和记录行为。
@pytest.fixture
def fake_db(mocker):
    return mocker.Mock(name="db")

@pytest.fixture
def fake_payload(mocker):
    return mocker.Mock(name="payload")

@pytest.fixture
def fake_background(mocker):
    bg = mocker.Mock(name="background")
    # bg.add_task 会被 assert_called_once_with(...) 验证
    return bg

@pytest.fixture
def fake_contact_model():
    # mapper 输出的 ORM model（这里不需要真实 Contact 实例）
    return object()

@pytest.fixture
def saved_contact():
    # repo.create 返回的“保存后 contact”
    return SimpleNamespace(
        id=123,
        contact_type="appointment",
        name="Alice",
        email="a@b.com",
        submitted_at=None,
    )

@pytest.fixture
def appointment_email_context():
    return {"id": 123, "email": "a@b.com"}


@pytest.fixture
def patch_to_contact_model(mocker, fake_contact_model):
    """
    patch 一定 patch ‘使用处’：
    backend.services.contacts_service 里 import 了 to_contact_model
    所以 patch 这里。
    理由：在原代码的contacts_service.create_contact()方法下有
    contact = to_contact_model(payload, ip=ip)
    但是：to_contact_model由import导入而没有在方法的传参中，所以需要制造一个假的顶替。
    """
    return mocker.patch(
        "backend.services.contacts_service.to_contact_model",
        return_value=fake_contact_model,
    )

@pytest.fixture
def patch_repo_create(mocker, saved_contact):
    return mocker.patch(
        "backend.services.contacts_service.contacts_repo.create",
        return_value=saved_contact,
    )

@pytest.fixture
def patch_build_appointment_email_context(mocker, appointment_email_context):
    return mocker.patch(
        "backend.services.contacts_service.build_appointment_email_context",
        return_value=appointment_email_context,
    )


