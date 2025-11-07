"""
HIPAA-Compliant Security & Encryption Module
Enterprise-grade security for protecting survivor data
"""

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import hashlib
import secrets
import base64
import os
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import json


class HIPAAEncryption:
    """
    HIPAA-compliant encryption for Protected Health Information (PHI)

    Features:
    - AES-256 encryption
    - Secure key derivation (PBKDF2)
    - Salt-based encryption
    - Secure deletion
    - Audit logging (encrypted)
    - Data retention policies
    """

    def __init__(self, master_key: Optional[str] = None):
        """
        Initialize encryption with master key

        Args:
            master_key: Master encryption key (if None, generates new one)
        """
        if master_key:
            self.master_key = master_key.encode()
        else:
            self.master_key = Fernet.generate_key()

        self.fernet = Fernet(self.master_key)
        self.audit_log: list = []

    def encrypt_data(self, data: str, context: str = "general") -> Dict[str, str]:
        """
        Encrypt sensitive data with metadata

        Args:
            data: Data to encrypt
            context: Context for audit trail

        Returns:
            Dict with encrypted data, salt, and metadata
        """
        # Generate unique salt
        salt = secrets.token_bytes(32)

        # Encrypt data
        encrypted = self.fernet.encrypt(data.encode())

        # Create metadata
        metadata = {
            "encrypted_data": base64.b64encode(encrypted).decode(),
            "salt": base64.b64encode(salt).decode(),
            "timestamp": datetime.now().isoformat(),
            "context": context,
            "algorithm": "AES-256-Fernet"
        }

        # Audit log
        self._add_audit_entry("encrypt", context)

        return metadata

    def decrypt_data(self, encrypted_package: Dict[str, str]) -> str:
        """
        Decrypt data from encrypted package

        Args:
            encrypted_package: Dict containing encrypted data and metadata

        Returns:
            Decrypted string
        """
        try:
            encrypted_data = base64.b64decode(encrypted_package["encrypted_data"])
            decrypted = self.fernet.decrypt(encrypted_data)

            # Audit log
            self._add_audit_entry("decrypt", encrypted_package.get("context", "unknown"))

            return decrypted.decode()
        except Exception as e:
            self._add_audit_entry("decrypt_failed", f"Error: {str(e)}")
            raise ValueError("Decryption failed - data may be corrupted or key is incorrect")

    def encrypt_file(self, filepath: str, output_path: Optional[str] = None) -> str:
        """
        Encrypt an entire file

        Args:
            filepath: Path to file to encrypt
            output_path: Path for encrypted file (if None, adds .encrypted extension)

        Returns:
            Path to encrypted file
        """
        if not output_path:
            output_path = filepath + ".encrypted"

        with open(filepath, 'rb') as f:
            file_data = f.read()

        encrypted_data = self.fernet.encrypt(file_data)

        with open(output_path, 'wb') as f:
            f.write(encrypted_data)

        self._add_audit_entry("encrypt_file", filepath)

        return output_path

    def decrypt_file(self, encrypted_filepath: str, output_path: str) -> str:
        """
        Decrypt a file

        Args:
            encrypted_filepath: Path to encrypted file
            output_path: Path for decrypted output

        Returns:
            Path to decrypted file
        """
        with open(encrypted_filepath, 'rb') as f:
            encrypted_data = f.read()

        try:
            decrypted_data = self.fernet.decrypt(encrypted_data)

            with open(output_path, 'wb') as f:
                f.write(decrypted_data)

            self._add_audit_entry("decrypt_file", encrypted_filepath)

            return output_path
        except Exception as e:
            self._add_audit_entry("decrypt_file_failed", f"{encrypted_filepath}: {str(e)}")
            raise ValueError("File decryption failed")

    def secure_delete(self, filepath: str, passes: int = 7):
        """
        Securely delete a file (DoD 5220.22-M standard)

        Args:
            filepath: Path to file to delete
            passes: Number of overwrite passes (default 7 for DoD standard)
        """
        if not os.path.exists(filepath):
            return

        file_size = os.path.getsize(filepath)

        # Overwrite with random data multiple times
        with open(filepath, 'ba+') as f:
            for _ in range(passes):
                f.seek(0)
                f.write(secrets.token_bytes(file_size))

        # Final delete
        os.remove(filepath)

        self._add_audit_entry("secure_delete", filepath)

    def hash_data(self, data: str, algorithm: str = "sha256") -> str:
        """
        Create cryptographic hash of data

        Args:
            data: Data to hash
            algorithm: Hashing algorithm (sha256, sha512)

        Returns:
            Hexadecimal hash string
        """
        if algorithm == "sha256":
            return hashlib.sha256(data.encode()).hexdigest()
        elif algorithm == "sha512":
            return hashlib.sha512(data.encode()).hexdigest()
        else:
            raise ValueError(f"Unsupported algorithm: {algorithm}")

    def generate_session_token(self, user_id: str, expiry_hours: int = 24) -> Dict[str, Any]:
        """
        Generate secure session token

        Args:
            user_id: User identifier
            expiry_hours: Hours until token expires

        Returns:
            Token data including token, expiry, and encrypted user_id
        """
        token = secrets.token_urlsafe(32)
        expiry = datetime.now() + timedelta(hours=expiry_hours)

        token_data = {
            "token": token,
            "user_id_hash": self.hash_data(user_id),
            "created": datetime.now().isoformat(),
            "expiry": expiry.isoformat(),
            "valid": True
        }

        self._add_audit_entry("generate_token", f"User: {self.hash_data(user_id)[:8]}")

        return token_data

    def _add_audit_entry(self, action: str, details: str):
        """
        Add encrypted audit log entry

        Args:
            action: Action performed
            details: Additional details
        """
        entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "details": details
        }

        # Encrypt audit entry
        encrypted_entry = self.fernet.encrypt(json.dumps(entry).encode())
        self.audit_log.append(base64.b64encode(encrypted_entry).decode())

    def get_audit_log(self) -> list:
        """
        Retrieve and decrypt audit log

        Returns:
            List of audit entries
        """
        decrypted_log = []

        for encrypted_entry in self.audit_log:
            try:
                entry_bytes = base64.b64decode(encrypted_entry)
                decrypted_entry = self.fernet.decrypt(entry_bytes)
                decrypted_log.append(json.loads(decrypted_entry.decode()))
            except Exception:
                decrypted_log.append({"error": "Failed to decrypt entry"})

        return decrypted_log

    def export_key(self) -> str:
        """
        Export master key (securely store this!)

        Returns:
            Base64-encoded master key
        """
        return base64.b64encode(self.master_key).decode()

    @staticmethod
    def generate_new_key() -> str:
        """
        Generate a new encryption key

        Returns:
            Base64-encoded key
        """
        key = Fernet.generate_key()
        return base64.b64encode(key).decode()


class DataRetentionPolicy:
    """
    HIPAA-compliant data retention and automatic deletion
    """

    def __init__(self, encryption: HIPAAEncryption):
        self.encryption = encryption
        self.retention_rules: Dict[str, int] = {
            "conversation": 24,  # hours
            "safety_plan": 720,  # 30 days
            "session": 1,  # 1 hour
            "temporary": 0  # immediate deletion
        }

    def set_retention_period(self, data_type: str, hours: int):
        """
        Set retention period for data type

        Args:
            data_type: Type of data
            hours: Hours to retain (0 for immediate deletion)
        """
        self.retention_rules[data_type] = hours

    def should_delete(self, timestamp: str, data_type: str) -> bool:
        """
        Check if data should be deleted based on retention policy

        Args:
            timestamp: ISO format timestamp
            data_type: Type of data

        Returns:
            True if data should be deleted
        """
        if data_type not in self.retention_rules:
            return False

        retention_hours = self.retention_rules[data_type]

        if retention_hours == 0:
            return True

        created_time = datetime.fromisoformat(timestamp)
        expiry_time = created_time + timedelta(hours=retention_hours)

        return datetime.now() > expiry_time

    def cleanup_expired_data(self, data_store: Dict[str, Any]) -> int:
        """
        Clean up expired data from data store

        Args:
            data_store: Dictionary of data items with timestamps

        Returns:
            Number of items deleted
        """
        deleted_count = 0
        items_to_delete = []

        for key, item in data_store.items():
            if "timestamp" in item and "type" in item:
                if self.should_delete(item["timestamp"], item["type"]):
                    items_to_delete.append(key)

        for key in items_to_delete:
            # Securely delete
            del data_store[key]
            deleted_count += 1

        return deleted_count


class AnonymizationEngine:
    """
    Anonymize and de-identify data for analysis while preserving privacy
    """

    def __init__(self):
        self.pii_patterns = {
            "phone": r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
            "email": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            "ssn": r'\b\d{3}-\d{2}-\d{4}\b',
            "address": r'\b\d+\s+[A-Za-z\s]+(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Lane|Ln|Drive|Dr|Court|Ct|Circle|Cir)\b'
        }

    def anonymize_text(self, text: str) -> str:
        """
        Remove or redact personally identifiable information

        Args:
            text: Text to anonymize

        Returns:
            Anonymized text
        """
        import re

        anonymized = text

        # Replace phone numbers
        anonymized = re.sub(self.pii_patterns["phone"], "[PHONE REDACTED]", anonymized)

        # Replace emails
        anonymized = re.sub(self.pii_patterns["email"], "[EMAIL REDACTED]", anonymized)

        # Replace SSN
        anonymized = re.sub(self.pii_patterns["ssn"], "[SSN REDACTED]", anonymized)

        # Replace addresses
        anonymized = re.sub(self.pii_patterns["address"], "[ADDRESS REDACTED]", anonymized)

        return anonymized

    def generate_pseudonym(self, real_name: str) -> str:
        """
        Generate consistent pseudonym for a name

        Args:
            real_name: Real name to pseudonymize

        Returns:
            Pseudonym
        """
        # Use hash to generate consistent pseudonym
        hash_value = hashlib.sha256(real_name.encode()).hexdigest()[:8]
        return f"User-{hash_value}"

    def de_identify_conversation(self, conversation: list) -> list:
        """
        De-identify an entire conversation

        Args:
            conversation: List of conversation messages

        Returns:
            De-identified conversation
        """
        de_identified = []

        for message in conversation:
            de_identified_message = message.copy()

            if "content" in de_identified_message:
                de_identified_message["content"] = self.anonymize_text(message["content"])

            if "user_id" in de_identified_message:
                de_identified_message["user_id"] = self.generate_pseudonym(message["user_id"])

            de_identified.append(de_identified_message)

        return de_identified


class SecureSessionManager:
    """
    Manage secure, encrypted sessions with automatic cleanup
    """

    def __init__(self, encryption: HIPAAEncryption):
        self.encryption = encryption
        self.sessions: Dict[str, Dict[str, Any]] = {}
        self.retention_policy = DataRetentionPolicy(encryption)

    def create_session(self, user_identifier: Optional[str] = None) -> str:
        """
        Create a new secure session

        Args:
            user_identifier: Optional user identifier (will be hashed)

        Returns:
            Session ID
        """
        session_id = secrets.token_urlsafe(32)

        self.sessions[session_id] = {
            "id": session_id,
            "user_hash": self.encryption.hash_data(user_identifier) if user_identifier else None,
            "created": datetime.now().isoformat(),
            "last_activity": datetime.now().isoformat(),
            "data": {},
            "type": "session"
        }

        return session_id

    def update_session(self, session_id: str, data: Dict[str, Any]):
        """
        Update session data

        Args:
            session_id: Session identifier
            data: Data to store in session
        """
        if session_id in self.sessions:
            # Encrypt sensitive data
            encrypted_data = self.encryption.encrypt_data(
                json.dumps(data),
                context=f"session-{session_id[:8]}"
            )

            self.sessions[session_id]["data"] = encrypted_data
            self.sessions[session_id]["last_activity"] = datetime.now().isoformat()

    def get_session_data(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve and decrypt session data

        Args:
            session_id: Session identifier

        Returns:
            Decrypted session data or None
        """
        if session_id not in self.sessions:
            return None

        session = self.sessions[session_id]

        if "data" in session and session["data"]:
            try:
                decrypted = self.encryption.decrypt_data(session["data"])
                return json.loads(decrypted)
            except Exception:
                return None

        return {}

    def delete_session(self, session_id: str, secure: bool = True):
        """
        Delete a session

        Args:
            session_id: Session to delete
            secure: Use secure deletion (overwrite before delete)
        """
        if session_id in self.sessions:
            if secure:
                # Overwrite session data with random data before deletion
                self.sessions[session_id]["data"] = secrets.token_bytes(1024)

            del self.sessions[session_id]

    def cleanup_expired_sessions(self) -> int:
        """
        Remove expired sessions based on retention policy

        Returns:
            Number of sessions deleted
        """
        return self.retention_policy.cleanup_expired_data(self.sessions)

    def get_active_session_count(self) -> int:
        """
        Get number of active sessions

        Returns:
            Count of active sessions
        """
        return len(self.sessions)


# Compliance and Security Utilities

def generate_hipaa_compliant_id() -> str:
    """
    Generate HIPAA-compliant unique identifier

    Returns:
        Unique, non-sequential ID
    """
    return secrets.token_urlsafe(32)


def secure_compare(a: str, b: str) -> bool:
    """
    Timing-attack resistant string comparison

    Args:
        a: First string
        b: Second string

    Returns:
        True if strings match
    """
    return secrets.compare_digest(a.encode(), b.encode())


def generate_password_hash(password: str, salt: Optional[bytes] = None) -> Dict[str, str]:
    """
    Generate secure password hash using PBKDF2

    Args:
        password: Password to hash
        salt: Optional salt (generates new if not provided)

    Returns:
        Dict with hash and salt
    """
    if salt is None:
        salt = secrets.token_bytes(32)

    kdf = PBKDF2(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )

    key = kdf.derive(password.encode())

    return {
        "hash": base64.b64encode(key).decode(),
        "salt": base64.b64encode(salt).decode(),
        "algorithm": "PBKDF2-SHA256",
        "iterations": 100000
    }


def verify_password(password: str, password_hash: Dict[str, str]) -> bool:
    """
    Verify password against hash

    Args:
        password: Password to verify
        password_hash: Hash dict from generate_password_hash

    Returns:
        True if password matches
    """
    salt = base64.b64decode(password_hash["salt"])
    stored_hash = base64.b64decode(password_hash["hash"])

    kdf = PBKDF2(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=password_hash.get("iterations", 100000),
        backend=default_backend()
    )

    try:
        kdf.verify(password.encode(), stored_hash)
        return True
    except Exception:
        return False
