import io


def test_upload_document(client):
    """Upload a text file and confirm response contains filename & id."""
    file_content = b"Hello world! This is a test document."
    files = {"files": ("test.txt", io.BytesIO(file_content), "text/plain")}

    response = client.post("/document/", files=files)
    assert response.status_code == 200

    docs = response.json()
    assert isinstance(docs, list)
    assert len(docs) == 1

    doc = docs[0]
    assert "id" in doc
    assert doc["filename"] == "test.txt"
    assert doc["content_preview"].startswith("Hello world!")


def test_list_documents(client):
    """Uploaded docs should be returned by GET /document/."""
    file_content = b"My climate notes"
    files = {"files": ("climate.txt", io.BytesIO(file_content), "text/plain")}
    upload_res = client.post("/document/", files=files)
    doc_id = upload_res.json()[0]["id"]

    response = client.get("/document/")
    assert response.status_code == 200

    docs = response.json()
    assert isinstance(docs, list)
    assert any(doc["id"] == doc_id and doc["filename"] == "climate.txt" for doc in docs)


def test_delete_document(client):
    """Upload → delete → confirm it's gone."""
    file_content = b"Temporary doc"
    files = {"files": ("temp.txt", io.BytesIO(file_content), "text/plain")}
    upload_res = client.post("/document/", files=files)
    doc_id = upload_res.json()[0]["id"]

    # Delete
    del_res = client.delete(f"/document/{doc_id}")
    assert del_res.status_code == 200
    assert del_res.json()["message"] == f"Document {doc_id} deleted successfully"

    # Confirm not in list
    list_res = client.get("/document/")
    assert all(doc["id"] != doc_id for doc in list_res.json())
