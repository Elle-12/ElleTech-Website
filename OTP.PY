#!/usr/bin/env python3
"""
OTP.PY

Simple email OTP sender + verifier.

Usage:
    - Set environment variables:
            SMTP_SERVER, SMTP_PORT, SMTP_USER, SMTP_PASSWORD, FROM_EMAIL
            (optional) SMTP_USE_SSL (1 or 0). Default: 1 if port==465 else 0

    - Send OTP:
            python OTP.PY send recipient@example.com

    - Verify OTP:
            python OTP.PY verify recipient@example.com 123456

Notes:
    - OTPs are stored in otp_store.json in the same directory and expire by default after 5 minutes.
    - This script uses the stdlib only (smtplib, email). Keep SMTP credentials secret.
"""


STORE_PATH = os.path.join(os.path.dirname(__file__), "otp_store.json")
DEFAULT_EXPIRY_SECONDS = 300  # 5 minutes


def _load_store():
        try:
                with open(STORE_PATH, "r", encoding="utf-8") as f:
                        return json.load(f)
        except FileNotFoundError:
                return {}
        except Exception:
                return {}


def _save_store(store):
        with open(STORE_PATH, "w", encoding="utf-8") as f:
                json.dump(store, f)


def _now_iso():
        return datetime.datetime.utcnow().isoformat()


def _iso_to_dt(s: str) -> datetime.datetime:
        return datetime.datetime.fromisoformat(s)


def generate_otp(length: int = 6) -> str:
        digits = string.digits
        return "".join(secrets.choice(digits) for _ in range(length))


def _get_smtp_config():
        server = os.environ.get("SMTP_SERVER")
        port = int(os.environ.get("SMTP_PORT", "465"))
        user = os.environ.get("SMTP_USER")
        password = os.environ.get("SMTP_PASSWORD")
        from_email = os.environ.get("FROM_EMAIL", user)
        use_ssl_env = os.environ.get("SMTP_USE_SSL")
        if use_ssl_env is None:
                use_ssl = (port == 465)
        else:
                use_ssl = use_ssl_env.strip() not in ("0", "false", "False", "")
        if not all([server, port, user, password, from_email]):
                raise RuntimeError(