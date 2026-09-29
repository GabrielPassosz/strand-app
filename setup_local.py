"""Create private local configuration once. Never overwrites existing configuration."""

from pathlib import Path
import secrets

root = Path(__file__).resolve().parent
config = root / ".env"
if not config.exists():
    with config.open("x", encoding="utf-8") as f:
        f.write(
            "DEBUG=True\nSECRET_KEY="
            + secrets.token_urlsafe(64)
            + "\nALLOWED_HOSTS=127.0.0.1,localhost\nPUBLIC_ORIGIN=http://127.0.0.1:8000\n"
        )
    try:
        config.chmod(0o600)
    except OSError:
        pass
    print(
        "Local configuration created. Development emails are written to data/emails/."
    )
else:
    print("Existing .env preserved.")
