import unittest
import sys
import os
from unittest.mock import patch, MagicMock

# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.aws_client.client import Client

class TestClient(unittest.TestCase):

    @patch("boto3.Session.client")
    def test_create_client_with_access_key(self, mock_client):
        # Giả lập client trả về một đối tượng mock
        mock_client.return_value = MagicMock()
        
        # Tạo Client với access key (không dùng SSO)
        aws_client = Client(service_name="s3", region="us-west-2", use_sso=False)
        client = aws_client.get_client()

        # Kiểm tra nếu client được tạo thành công
        self.assertIsNotNone(client)
        mock_client.assert_called_once_with("s3")
        print("[✓] Test create client with access key passed.")

    @patch("boto3.Session.client")
    @patch("boto3.Session")
    def test_create_client_with_sso(self, mock_session, mock_client):
        # Giả lập behavior của boto3.Session
        mock_session.return_value.client.return_value = MagicMock()

        # Tạo Client với SSO
        aws_client = Client(service_name="ec2", region="us-west-2", use_sso=True, sso_profile="my-sso")
        client = aws_client.get_client()

        # Kiểm tra nếu client được tạo thành công
        self.assertIsNotNone(client)
        mock_session.return_value.client.assert_called_once_with("ec2")
        print("[✓] Test create client with SSO passed.")

    @patch("boto3.Session.client")
    def test_create_client_with_invalid_credentials(self, mock_client):
        # Giả lập ngoại lệ khi không có credentials
        mock_client.side_effect = Exception("Credentials not found")

        # Kiểm tra khi không có thông tin đăng nhập
        aws_client = Client(service_name="s3", region="us-west-2")
        client = aws_client.get_client()

        # Kiểm tra nếu client là None khi có lỗi kết nối
        self.assertIsNone(client)
        print("[✓] Test create client with invalid credentials passed.")

if __name__ == "__main__":
    unittest.main()