def attachments_serializer(query):
    data = []
    for item in query:
        data.append({"tag": item.tag, "file_name": item.file_name, "file_url": item.file.url})
    return data
