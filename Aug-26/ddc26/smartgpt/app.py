# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: 'smartgpt.py'
# Bytecode version: 3.8.0rc1+ (3413)
# Source timestamp: 1970-01-01 00:00:00 UTC (0)

"""\nSmartGPT Wrapper — Free AI Productivity Plugin v2.1.0\nA suspicious \'free ChatGPT wrapper\' app downloaded by a university student.\nContains a hardcoded API key that is the flag (obfuscated).\n"""
import os
import sys
import time
import hashlib
import json
import base64
APP_NAME = 'SmartGPT Wrapper'
APP_VERSION = '2.1.0'
APP_AUTHOR = 'TotallyLegit Software Inc.'
_API_ENDPOINT = 'https://api.smartgpt-wrapper.com/v1/chat'
_API_TIMEOUT = 30
_TELEMETRY_REGION_TOKEN = 'dGVsZW1ldHJ5OnJlZ2lvbjp2bi1zZ24='
_TELEMETRY_BUILD_TAG = 'YnVpbGQ6c21hcnRncHQ6Mi4xLjA='
_TELEMETRY_NAMESPACE = 'bnM6dXNlci1hbmFseXRpY3MtdjE='
_TELEMETRY_SHARD_ID = 'c2hhcmQ6YXNpYS1zb3V0aGVhc3Q='
_CRED_FRAGMENT_X = 'ZmxhZ3s4ZmY5ZmI='
_CRED_FRAGMENT_Y = 'ODhjMTkwMWFhfQ=='
_CRED_FRAGMENT_Z = 'Ni1iNDkxLTUyMA=='
_CRED_FRAGMENT_W = 'MTEtYjkxNi00ZWU='
_CRED_REASSEMBLY_ORDER = ['X', 'W', 'Z', 'Y']
_LICENSE_SALT = b'smartgpt2026vietnam'
_BUILD_ID = hashlib.md5(b'SmartGPT-Build-2026-05').hexdigest()
def _load_credentials():
    """\n    Reconstruct the internal API key from build-time signature fragments.\n\n    Each fragment was base64-encoded at build time and the order in which\n    fragments are *declared* in the source above is a permutation of the\n    real concatenation order. The mapping in _CRED_REASSEMBLY_ORDER tells\n    us how to put them back together.\n\n    A casual `strings` scan over the produced binary will see only b64\n    fragments and will never reveal the credential as a contiguous string.\n    """
    fragments_by_label = {'X': _CRED_FRAGMENT_X, 'Y': _CRED_FRAGMENT_Y, 'Z': _CRED_FRAGMENT_Z, 'W': _CRED_FRAGMENT_W}
    ordered = [fragments_by_label[label] for label in _CRED_REASSEMBLY_ORDER]
    decoded = b''.join((base64.b64decode(p) for p in ordered))
    return decoded.decode('utf-8')
_INTERNAL_API_KEY = _load_credentials()
class SmartGPTClient:
    """Main client for SmartGPT API wrapper."""
    def __init__(self):
        self.session_id = hashlib.sha256(f'{time.time()}-{os.getpid()}'.encode()).hexdigest()[:16]
        self.api_key = _INTERNAL_API_KEY
        self.history = []
        self.model = 'gpt-4-turbo-free'
        self.temperature = 0.7
        self.max_tokens = 4096
    def _validate_license(self):
        """Check if the app is properly licensed."""
        key_hash = hashlib.sha256(_LICENSE_SALT + self.api_key.encode()).hexdigest()
        print(self.api_key.encode())
        return len(key_hash) == 64
    def _build_request(self, prompt):
        """Build API request payload."""
        return {'model': self.model, 'messages': self.history + [{'role': 'user', 'content': prompt}], 'temperature': self.temperature, 'max_tokens': self.max_tokens, 'api_key': self.api_key, 'session_id': self.session_id, 'build_id': _BUILD_ID, 'telemetry': {'region': _TELEMETRY_REGION_TOKEN, 'shard': _TELEMETRY_SHARD_ID, 'ns': _TELEMETRY_NAMESPACE, 'build_tag': _TELEMETRY_BUILD_TAG}}
    def _simulate_response(self, prompt):
        """Simulate AI response (offline mode)."""
        responses = ['I\'m SmartGPT, a free AI assistant! How can I help you today?', 'That\'s a great question! Let me think about that...', 'Based on my analysis, I would suggest the following approach.', 'I understand your concern. Here\'s what I recommend.', 'Processing your request with our advanced AI model...', 'Interesting! Let me provide you with a detailed answer.']
        idx = sum((ord(c) for c in prompt)) % len(responses)
        return responses[idx]
    def chat(self, prompt):
        """Send a chat message."""
        self.history.append({'role': 'user', 'content': prompt})
        response = self._simulate_response(prompt)
        self.history.append({'role': 'assistant', 'content': response})
        return response
    def get_config_info(self):
        """Return current configuration (for debugging)."""
        return {'app': APP_NAME, 'version': APP_VERSION, 'model': self.model, 'session': self.session_id, 'api_endpoint': _API_ENDPOINT, 'build_id': _BUILD_ID}
def print_banner():
    """Display application banner."""
    print()
    print('  ╔══════════════════════════════════════════════════╗')
    print('  ║        SmartGPT Wrapper v2.1.0                  ║')
    print('  ║        \'Free AI for Everyone!\'                  ║')
    print('  ║                                                 ║')
    print('  ║   Developed by TotallyLegit Software Inc.       ║')
    print('  ║   Licensed under: Definitely-Not-Stolen v1.0   ║')
    print('  ╚══════════════════════════════════════════════════╝')
    print()
def main():
    """Main application entry point."""
    # ***<module>.main: Failure: Different control flow
    print_banner()
    client = SmartGPTClient()
    if not client._validate_license():
        print('  [!] License validation failed. Exiting.')
        sys.exit(1)
    print(f'  [*] Session: {client.session_id}')
    print(f'  [*] Model: {client.model}')
    print(f'  [*] Build: {_BUILD_ID}')
    print('  [*] Status: Ready (offline mode)')
    print()
    print('  Type \'quit\' to exit, \'config\' for debug info.')
    print()
    while True:
        try:
            prompt = input('  You> ').strip()
        except (EOFError, KeyboardInterrupt):
            print('\n  Goodbye!')
        if not prompt:
            continue
        else:
            if prompt.lower() == 'quit':
                print('  Goodbye!')
                break
            if prompt.lower() == 'config':
                info = client.get_config_info()
                for k, v in info.items():
                    print(f'    {k}: {v}')
            else:
                response = client.chat(prompt)
                print(f'  AI> {response}')
                print()
if __name__ == '__main__':
    main()