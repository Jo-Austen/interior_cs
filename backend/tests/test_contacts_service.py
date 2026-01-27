from datetime import datetime, timezone
from types import SimpleNamespace

from backend.services.contacts_service import create_contact, list_contacts_brief
from backend.services.contacts_service import send_appointment_emails


def test_create_contact_schedules_email_task(
    fake_db,
    fake_payload,
    fake_background,
    fake_contact_model,
    saved_contact,
    appointment_email_context,
    patch_to_contact_model,
    patch_repo_create,
    patch_build_appointment_email_context,
):
    # Act
    result = create_contact(
        db=fake_db,
        payload=fake_payload,
        ip="1.2.3.4",
        background=fake_background,
    )

    # Assert: mapper
    patch_to_contact_model.assert_called_once_with(fake_payload, ip="1.2.3.4")

    # Assert: repo persistence
    patch_repo_create.assert_called_once_with(fake_db, fake_contact_model)

    # Assert: email context builder
    patch_build_appointment_email_context.assert_called_once_with(saved_contact)

    # Assert: background task scheduled (关键)
    fake_background.add_task.assert_called_once_with(send_appointment_emails, appointment_email_context)

    # Assert: return value
    assert result is saved_contact


def test_list_contacts_brief_formats_output(mocker, fake_db):
    now = datetime(2026, 1, 26, 9, 0, 0, tzinfo=timezone.utc)

    rows = [
        SimpleNamespace(
            id=1,
            contact_type="appointment",
            name="Alice",
            email="a@b.com",
            submitted_at=now,
        ),
        SimpleNamespace(
            id=2,
            contact_type="question",
            name="Bob",
            email="b@b.com",
            submitted_at=now,
        ),
    ]

    patch_list_recent = mocker.patch(
        "backend.services.contacts_service.contacts_repo.list_recent",
        return_value=rows,
    )

    result = list_contacts_brief(fake_db, limit=50)

    patch_list_recent.assert_called_once_with(fake_db, limit=50)
    assert result == [
        {
            "id": 1,
            "contact_type": "appointment",
            "name": "Alice",
            "email": "a@b.com",
            "submitted_at": now.isoformat(),
        },
        {
            "id": 2,
            "contact_type": "question",
            "name": "Bob",
            "email": "b@b.com",
            "submitted_at": now.isoformat(),
        },
    ]
