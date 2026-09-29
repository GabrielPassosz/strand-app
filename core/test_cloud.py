import os
import sys
import subprocess
from pathlib import Path
from django.test import TestCase, override_settings
from django.conf import settings

class CloudConfigurationTests(TestCase):
    def config(self, **changes):
        env={**os.environ, 'VERCEL':'1', 'DEBUG':'False', 'SECRET_KEY':'cloud-configuration-test-key-with-more-than-fifty-characters-only', 'PUBLIC_ORIGIN':'https://strand-example.vercel.app','DATABASE_URL':'postgresql://test:test@localhost/test','EMAIL_HOST':'smtp.example.com','EMAIL_HOST_USER':'test','DEFAULT_FROM_EMAIL':'noreply@example.com','STORAGE_BACKEND':'s3','S3_ENDPOINT_URL':'https://example.supabase.co/storage/v1/s3','S3_REGION':'us-east-1','S3_ACCESS_KEY_ID':'test','S3_SECRET_ACCESS_KEY':'test','S3_BUCKET_NAME':'private',**changes}
        return subprocess.run([sys.executable,'-c','from strand import settings as s; assert s.DATA_DIR.as_posix()=="/tmp/strand"; assert s.DATABASES["default"]["CONN_MAX_AGE"]==0; assert s.DATABASES["default"]["OPTIONS"]["prepare_threshold"] is None; assert s.STORAGES["default"]["OPTIONS"]["querystring_auth"]; print("OK")'],cwd=settings.BASE_DIR,env=env,capture_output=True,text=True)
    def test_cloud_configuration(self):
        result=self.config();self.assertEqual(result.returncode,0,result.stderr)
    def test_no_local_storage_on_vercel(self):
        self.assertNotEqual(self.config(STORAGE_BACKEND='local').returncode,0)
    def test_no_sqlite_on_vercel(self):
        self.assertNotEqual(self.config(DATABASE_URL='sqlite:///:memory:').returncode,0)
    def test_no_debug_on_vercel(self):
        self.assertNotEqual(self.config(DEBUG='True').returncode,0)
    @override_settings(CRON_SECRET='unit-test-secret')
    def test_maintenance_requires_secret(self):
        self.assertEqual(self.client.get('/api/maintenance/').status_code,401)
        self.assertEqual(self.client.get('/api/maintenance/',HTTP_AUTHORIZATION='Bearer unit-test-secret').status_code,200)
