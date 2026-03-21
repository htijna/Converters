import urllib.request
import urllib.parse
import os
import uuid

def test_api():
    url = 'http://localhost:8000/convert'
    boundary = uuid.uuid4().hex
    
    file_path = 'test.docx'
    
    if not os.path.exists(file_path):
        print("Skipping, test.docx not found.")
        return
        
    with open(file_path, 'rb') as f:
        file_content = f.read()

    body = (
        f"--{boundary}\r\n"
        f"Content-Disposition: form-data; name=\"file\"; filename=\"test.docx\"\r\n"
        f"Content-Type: application/vnd.openxmlformats-officedocument.wordprocessingml.document\r\n\r\n".encode('utf-8') +
        file_content +
        f"\r\n--{boundary}\r\n"
        f"Content-Disposition: form-data; name=\"target_format\"\r\n\r\n"
        f"pdf\r\n"
        f"--{boundary}--\r\n".encode('utf-8')
    )
    
    req = urllib.request.Request(url, data=body)
    req.add_header('Content-Type', f'multipart/form-data; boundary={boundary}')
    
    try:
        response = urllib.request.urlopen(req)
        print("SUCCESS:")
        print(response.read().decode())
    except urllib.error.HTTPError as e:
        print(f"HTTP ERROR {e.code}:")
        print(e.read().decode())
    except Exception as e:
        print(f"OTHER ERROR: {e}")

test_api()
