#!/usr/bin/env python3
"""
Level 1 Easy Mode Crypto
AES-128 with 100,000 PBKDF2 iterations (optimized for speed)
"""

from enhanced_crypto import EnhancedCrypto


class Level1Crypto(EnhancedCrypto):
    """
    Level 1 Easy Mode Crypto
    - AES-128 (16-byte keys)
    - 100,000 PBKDF2 iterations (vs 500k in higher levels)
    - Optimized for speed and usability
    """
    
    # Override iterations for Easy Mode
    PBKDF2_ITERATIONS = 100000  # Easy Mode: 100k iterations
    
    def __init__(self, nfc_passkey: str, alphabet_salt: bytes):
        """
        Initialize Level 1 Easy Mode crypto
        
        Args:
            nfc_passkey: NFC tag passkey or user password
            alphabet_salt: Vault chaos alphabet as bytes
        """
        # Always use AES-128 (key_size=16) for Level 1
        super().__init__(
            nfc_passkey=nfc_passkey,
            alphabet_salt=alphabet_salt,
            key_size=16  # AES-128
        )
    
    def get_security_info(self):
        """Get security parameters for Level 1"""
        return {
            'level': 'Level 1 - Easy Mode',
            'algorithm': 'AES-128-CBC',
            'key_size': '128-bit',
            'pbkdf2_iterations': self.PBKDF2_ITERATIONS,
            'salt_size': f'{self.SALT_SIZE * 8}-bit',
            'iv_size': f'{self.IV_SIZE * 8}-bit',
            'authentication': 'HMAC-SHA256',
            'compression': 'zlib (level 9)',
            'key_derivation': 'PBKDF2-HMAC-SHA256',
            'per_file_keys': True,
            'security_level': 'PERSONAL USE (STRONG)'
        }
