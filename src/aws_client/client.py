import boto3
from botocore.exceptions import BotoCoreError, NoCredentialsError, ClientError
from typing import Optional


class Client:
    def __init__(self, service_name: str, region: str, use_sso: bool = False, sso_profile: Optional[str] = None):
        """
        AWS client wrapper that supports both credentials and SSO.

        Args:
            service_name (str): e.g., "s3", "rds", "ec2", etc.
            region (str): AWS region (e.g., "us-west-2")
            use_sso (bool): If True, use SSO authentication
            sso_profile (str): AWS profile name configured for SSO
        """
        self.service_name = service_name
        self.region = region
        self.use_sso = use_sso
        self.sso_profile = sso_profile
        self.client = self._create_client()

    def _create_client(self):
        try:
            if self.use_sso and self.sso_profile:
                print(f"[i] Using SSO profile: {self.sso_profile}")
                session = boto3.Session(profile_name=self.sso_profile, region_name=self.region)
            else:
                print("[i] Using default AWS credentials (access key or IAM role)")
                session = boto3.Session(region_name=self.region)

            client = session.client(self.service_name)
            print(f"[✓] Connected to {self.service_name} in {self.region}")
            return client

        except NoCredentialsError:
            print("[✗] AWS credentials not found. Please run `aws configure` or `aws sso login`.")
        except ClientError as e:
            print(f"[✗] AWS ClientError: {e}")
        except BotoCoreError as e:
            print(f"[✗] BotoCoreError: {e}")
        return None

    def get_client(self):
        return self.client
