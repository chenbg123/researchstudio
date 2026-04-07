from app.services.thread_persistence import ThreadPersistenceService


def test_upsert_thread_snapshot_persists_messages(fake_session):
    service = ThreadPersistenceService(fake_session)

    service.upsert_thread_snapshot(
        user_id="00000000-0000-0000-0000-000000000001",
        thread_id="thread-1",
        title="Quarterly Research",
        profile_key="default",
        messages=[
            {"id": "m1", "type": "human", "content": [{"type": "text", "text": "hello"}]},
            {"id": "m2", "type": "ai", "content": [{"type": "text", "text": "world"}]},
        ],
        artifacts=[],
    )

    snapshot = service.get_thread("thread-1")
    assert snapshot is not None
    assert snapshot.title == "Quarterly Research"
    messages = service.get_messages("thread-1")
    assert len(messages) == 2
    assert messages[0].text_content == "hello"


def test_upsert_thread_updates_existing(fake_session):
    service = ThreadPersistenceService(fake_session)

    service.upsert_thread_snapshot(
        user_id="00000000-0000-0000-0000-000000000001",
        thread_id="thread-2",
        title="Draft Report",
        profile_key="default",
        messages=[{"id": "m1", "type": "human", "content": [{"type": "text", "text": "first"}]}],
        artifacts=[],
    )

    service.upsert_thread_snapshot(
        user_id="00000000-0000-0000-0000-000000000001",
        thread_id="thread-2",
        title="Final Report",
        profile_key="reporting",
        messages=[
            {"id": "m1", "type": "human", "content": [{"type": "text", "text": "first"}]},
            {"id": "m2", "type": "ai", "content": [{"type": "text", "text": "second"}]},
        ],
        artifacts=[],
    )

    thread = service.get_thread("thread-2")
    assert thread.title == "Final Report"
    messages = service.get_messages("thread-2")
    assert len(messages) == 2


def test_register_element(fake_session):
    service = ThreadPersistenceService(fake_session)

    # Need a thread first
    service.upsert_thread_snapshot(
        user_id="00000000-0000-0000-0000-000000000001",
        thread_id="thread-3",
        title="Upload Test",
        profile_key="default",
        messages=[],
        artifacts=[],
    )

    service.register_element(
        thread_id="thread-3",
        user_id="00000000-0000-0000-0000-000000000001",
        element_id="upload-1",
        name="report.pdf",
        mime="application/pdf",
        size=12345,
        source="upload",
        storage_provider="local",
        object_key="threads/thread-3/uploads/report.pdf",
    )

    elements = service.get_elements("thread-3")
    assert len(elements) == 1
    assert elements[0].name == "report.pdf"
