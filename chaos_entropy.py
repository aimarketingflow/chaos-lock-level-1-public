#!/usr/bin/env python3
"""
Chaos Entropy Collection System
Ultimate entropy generation with 17+ collection methods
Shared across all Chaos Lock levels
"""

import time
import secrets
import hashlib
import datetime
import math
from PyQt6.QtGui import QCursor


class ChaosEntropyCollector:
    """
    Ultimate entropy collection system with keyboard mapping and pattern detection.
    
    Features:
    - Keyboard position mapping (any character → 0-9)
    - 17+ entropy collection methods
    - Pattern detection (palindrome, ascending, descending, repeating)
    - NFC passkey modifiers (timing, samples, modes)
    """
    
    def __init__(self, nfc_passkey="", log_callback=None):
        """
        Initialize the entropy collector.
        
        Args:
            nfc_passkey: NFC passkey string (last 4 chars control entropy)
            log_callback: Function to call for logging (optional)
        """
        self.nfc_passkey = nfc_passkey
        self.log = log_callback if log_callback else lambda x: None
        
        # Keyboard position mapping
        self.keyboard_map = self.build_keyboard_map()
        
        # Default entropy modifiers
        self.timing_multiplier = 1.0
        self.sample_count = 5
        self.entropy_modes = []
        self.digit_sum = 0
        self.digit_product = 1
        self.is_palindrome = False
        self.is_ascending = False
        self.is_descending = False
        self.repeating_pattern = None
        self.conversion_log = ""
        
        # Parse NFC passkey if provided
        if nfc_passkey and len(nfc_passkey) >= 4:
            self._parse_nfc_passkey()
    
    def _parse_nfc_passkey(self):
        """Parse last 4 characters of NFC passkey for entropy modifiers"""
        last_4 = self.nfc_passkey[-4:]
        last_4_numeric = self.chars_to_numbers(last_4)
        
        self.conversion_log = f"'{last_4}' → {last_4_numeric}"
        
        # Digit 1: Timing multiplier (0-9 → 0.5x to 5.0x)
        self.timing_multiplier = 0.5 + (last_4_numeric[0] * 0.5)
        
        # Digit 2: Sample count (0-9 → 1 to 10 samples)
        self.sample_count = max(1, last_4_numeric[1])
        
        # Digit 3-4: Enable special entropy modes
        mode_code = last_4_numeric[2] * 10 + last_4_numeric[3]
        self.entropy_modes = self.decode_entropy_modes(mode_code)
        
        # Calculate additional modifiers
        self.digit_sum = sum(last_4_numeric)
        self.digit_product = 1
        for d in last_4_numeric:
            self.digit_product *= d if d > 0 else 1
        
        # Check patterns
        self.is_palindrome = (last_4_numeric[0] == last_4_numeric[3] and 
                             last_4_numeric[1] == last_4_numeric[2])
        self.is_ascending = all(last_4_numeric[i] <= last_4_numeric[i+1] 
                               for i in range(3))
        self.is_descending = all(last_4_numeric[i] >= last_4_numeric[i+1] 
                                for i in range(3))
        self.repeating_pattern = self.detect_repeating(last_4_numeric)
    
    def build_keyboard_map(self):
        """Build keyboard position map (left to right, top to bottom)"""
        keyboard = [
            ['esc', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=', 'del'],
            ['tab', 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[', ']', '\\'],
            ['caps', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', "'", 'enter'],
            ['shift', 'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/', 'shift'],
            ['fn', 'ctrl', 'alt', 'cmd', 'space', 'cmd', 'alt', 'left', 'up', 'down', 'right']
        ]
        
        key_map = {}
        position = 1
        for row in keyboard:
            for key in row:
                key_map[key.lower()] = position % 10
                key_map[key.upper()] = position % 10
                position += 1
        
        # Add special characters
        special_chars = {
            '!': 2, '@': 3, '#': 4, '$': 5, '%': 6, '^': 7, '&': 8, '*': 9, '(': 10, ')': 11,
            '_': 12, '+': 13, '~': 1, '`': 1, '{': 11, '}': 12, '|': 13, ':': 10, '"': 11,
            '<': 9, '>': 10, '?': 11, ' ': 5
        }
        for char, val in special_chars.items():
            key_map[char] = val % 10
        
        return key_map
    
    def chars_to_numbers(self, chars):
        """Convert characters to numbers using keyboard position"""
        numbers = []
        for char in chars:
            if char.isdigit():
                numbers.append(int(char))
            elif char.lower() in self.keyboard_map:
                numbers.append(self.keyboard_map[char.lower()])
            else:
                numbers.append(ord(char) % 10)
        return numbers
    
    def detect_repeating(self, digits):
        """Detect repeating digit patterns"""
        if len(set(digits)) == 1:
            return digits[0]
        return None
    
    def decode_entropy_modes(self, mode_code):
        """Decode 2-digit mode code into entropy collection modes"""
        modes = []
        
        if mode_code % 2 == 0:
            modes.append('fibonacci')
        if mode_code % 3 == 0:
            modes.append('prime_walk')
        if mode_code % 5 == 0:
            modes.append('chaos_spiral')
        if mode_code % 7 == 0:
            modes.append('golden_ratio')
        if mode_code >= 50:
            modes.append('reverse_timing')
        if mode_code >= 75:
            modes.append('exponential_sampling')
        
        return modes if modes else ['standard']
    
    # ========== Entropy Collection Methods ==========
    
    def fibonacci_entropy(self):
        """Collect entropy using Fibonacci sequence timing"""
        entropy = b''
        fib = [1, 1]
        for i in range(8):
            if i > 1:
                fib.append(fib[-1] + fib[-2])
            time.sleep(fib[i] / 1000000.0)
            entropy += secrets.token_bytes(fib[i] % 16 + 1)
        self.log(f"🌀 Fibonacci: {len(entropy)} bytes")
        return entropy
    
    def prime_walk_entropy(self):
        """Collect entropy by walking through prime numbers"""
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
        entropy = b''
        for prime in primes[:self.sample_count]:
            entropy += secrets.token_bytes(prime)
            time.sleep(prime / 1000000.0)
        self.log(f"🔢 Prime walk: {len(entropy)} bytes")
        return entropy
    
    def chaos_spiral_entropy(self):
        """Collect entropy in a spiral pattern based on mouse movement"""
        entropy = b''
        center_pos = QCursor.pos()
        
        for i in range(self.sample_count):
            angle = i * (2 * math.pi / self.sample_count)
            radius = i * 10
            target_x = int(center_pos.x() + radius * math.cos(angle))
            target_y = int(center_pos.y() + radius * math.sin(angle))
            
            entropy += target_x.to_bytes(4, 'big', signed=True)
            entropy += target_y.to_bytes(4, 'big', signed=True)
            entropy += secrets.token_bytes(4)
        
        self.log(f"🌀 Chaos spiral: {len(entropy)} bytes")
        return entropy
    
    def golden_ratio_entropy(self):
        """Collect entropy using golden ratio timing"""
        phi = 1.618033988749895
        entropy = b''
        
        for i in range(self.sample_count):
            delay = (phi ** i) / 1000000.0
            time.sleep(min(delay, 0.1))
            byte_count = int((phi ** i) % 32) + 1
            entropy += secrets.token_bytes(byte_count)
        
        self.log(f"✨ Golden ratio: {len(entropy)} bytes")
        return entropy
    
    def palindrome_entropy(self):
        """Mirror sampling for palindrome patterns"""
        entropy = b''
        forward = []
        
        for i in range(self.sample_count):
            forward.append(secrets.token_bytes(8))
        
        backward = forward[::-1]
        
        for f, b in zip(forward, backward):
            xor_result = bytes(a ^ b for a, b in zip(f, b))
            entropy += xor_result
        
        self.log(f"🔄 Palindrome mirror: {len(entropy)} bytes")
        return entropy
    
    def ascending_ramp_entropy(self):
        """Ramp up entropy collection"""
        entropy = b''
        
        for i in range(self.sample_count):
            byte_count = (i + 1) * 4
            entropy += secrets.token_bytes(byte_count)
            time.sleep((i + 1) / 1000000.0)
        
        self.log(f"📈 Ascending ramp: {len(entropy)} bytes")
        return entropy
    
    def descending_ramp_entropy(self):
        """Ramp down entropy collection"""
        entropy = b''
        
        for i in range(self.sample_count):
            byte_count = (self.sample_count - i) * 4
            entropy += secrets.token_bytes(byte_count)
            time.sleep((self.sample_count - i) / 1000000.0)
        
        self.log(f"📉 Descending ramp: {len(entropy)} bytes")
        return entropy
    
    def repeating_multiplier_entropy(self):
        """Multiply sampling based on repeating digit"""
        entropy = b''
        
        if self.repeating_pattern is not None:
            multiplier = max(1, self.repeating_pattern)
            for _ in range(self.sample_count * multiplier):
                entropy += secrets.token_bytes(multiplier * 2)
            self.log(f"🔁 Repeating ×{multiplier}: {len(entropy)} bytes")
        
        return entropy
    
    def digit_sum_strategy_entropy(self):
        """Strategy based on digit sum"""
        entropy = b''
        
        if self.digit_sum < 10:
            for i in range(self.sample_count):
                entropy += secrets.token_bytes(i + 1)
            self.log(f"➡️ Sequential (sum={self.digit_sum}): {len(entropy)} bytes")
        elif self.digit_sum < 20:
            for _ in range(self.sample_count):
                byte_count = secrets.randbelow(16) + 1
                entropy += secrets.token_bytes(byte_count)
            self.log(f"🎲 Random (sum={self.digit_sum}): {len(entropy)} bytes")
        else:
            for _ in range(self.sample_count):
                entropy += secrets.token_bytes(32)
            self.log(f"⚡ Parallel (sum={self.digit_sum}): {len(entropy)} bytes")
        
        return entropy
    
    def digit_product_chaos_entropy(self):
        """Chaos level based on digit product"""
        entropy = b''
        chaos_level = min(self.digit_product, 100)
        
        for i in range(self.sample_count):
            byte_count = max(1, (chaos_level // 10) + i)
            entropy += secrets.token_bytes(byte_count)
        
        self.log(f"💥 Chaos level {chaos_level}: {len(entropy)} bytes")
        return entropy
    
    def modulo_time_entropy(self):
        """Time-based entropy using modulo"""
        entropy = b''
        now = datetime.datetime.now()
        
        if self.conversion_log:
            dow_mod = now.weekday()
            entropy += secrets.token_bytes(dow_mod + 1)
            
            hour_mod = now.hour % 12
            entropy += secrets.token_bytes(hour_mod + 1)
            
            minute_mod = now.minute % 10
            entropy += secrets.token_bytes(minute_mod + 1)
        
        self.log(f"🕐 Time-based: {len(entropy)} bytes")
        return entropy
    
    def collect_creative_entropy(self):
        """Collect creative, low-permission entropy sources"""
        # Try to import psutil
        try:
            import psutil
            HAS_PSUTIL = True
        except ImportError:
            HAS_PSUTIL = False
        
        entropy_bytes = b''
        
        # 1. Mouse position entropy
        try:
            cursor_pos = QCursor.pos()
            
            if self.nfc_passkey:
                nfc_hash = hashlib.md5(self.nfc_passkey.encode()).hexdigest()
                x_offset = int(nfc_hash[:4], 16) % 100 - 50
                y_offset = int(nfc_hash[4:8], 16) % 100 - 50
                sample_x = cursor_pos.x() + x_offset
                sample_y = cursor_pos.y() + y_offset
            else:
                sample_x = cursor_pos.x()
                sample_y = cursor_pos.y()
            
            entropy_bytes += sample_x.to_bytes(4, 'big')
            entropy_bytes += sample_y.to_bytes(4, 'big')
            self.log(f"🖱️  Mouse: ({cursor_pos.x()}, {cursor_pos.y()})")
        except Exception as e:
            self.log(f"⚠️  Mouse sampling: {str(e)[:30]}")
        
        # 2. System metrics
        if HAS_PSUTIL:
            try:
                cpu_percent = psutil.cpu_percent(interval=0.1)
                memory = psutil.virtual_memory()
                disk_io = psutil.disk_io_counters()
                
                entropy_bytes += str(cpu_percent).encode()
                entropy_bytes += str(memory.percent).encode()
                entropy_bytes += str(memory.available).encode()
                if disk_io:
                    entropy_bytes += str(disk_io.read_bytes).encode()
                    entropy_bytes += str(disk_io.write_bytes).encode()
                
                self.log(f"💻 CPU: {cpu_percent:.1f}% | RAM: {memory.percent:.1f}%")
            except Exception as e:
                self.log(f"⚠️  System metrics: {str(e)[:30]}")
        else:
            import os
            entropy_bytes += str(os.getpid()).encode()
            entropy_bytes += str(time.time()).encode()
            self.log("💻 Basic system entropy (install psutil for more)")
        
        # 3. Process timing jitter
        try:
            timings = []
            adjusted_samples = int(self.sample_count * self.timing_multiplier)
            
            for i in range(adjusted_samples):
                start = time.perf_counter_ns()
                iterations = int(1 + (i * self.timing_multiplier))
                for _ in range(iterations):
                    _ = hashlib.sha256(secrets.token_bytes(16)).digest()
                end = time.perf_counter_ns()
                timings.append(end - start)
            
            for timing in timings:
                entropy_bytes += timing.to_bytes(8, 'big')
            
            self.log(f"⏱️  Timing jitter: {len(timings)} samples (×{self.timing_multiplier:.1f})")
        except Exception as e:
            self.log(f"⚠️  Timing jitter: {str(e)[:30]}")
        
        # 4. Network stats
        if HAS_PSUTIL:
            try:
                net_io = psutil.net_io_counters()
                entropy_bytes += str(net_io.bytes_sent).encode()
                entropy_bytes += str(net_io.bytes_recv).encode()
                entropy_bytes += str(net_io.packets_sent).encode()
                entropy_bytes += str(net_io.packets_recv).encode()
                
                self.log(f"🌐 Network: {net_io.packets_sent} sent, {net_io.packets_recv} recv")
            except Exception as e:
                self.log(f"⚠️  Network stats: {str(e)[:30]}")
        
        # 5. Process PIDs
        if HAS_PSUTIL:
            try:
                pids = [p.pid for p in psutil.process_iter(['pid'])][:10]
                for pid in pids:
                    entropy_bytes += pid.to_bytes(4, 'big')
                self.log(f"🔢 Processes: {len(pids)} PIDs sampled")
            except Exception as e:
                self.log(f"⚠️  Process list: {str(e)[:30]}")
        
        # 6. Special entropy modes
        if self.entropy_modes and 'standard' not in self.entropy_modes:
            self.log(f"🎲 Special modes: {', '.join(self.entropy_modes)}")
            
            if 'fibonacci' in self.entropy_modes:
                entropy_bytes += self.fibonacci_entropy()
            if 'prime_walk' in self.entropy_modes:
                entropy_bytes += self.prime_walk_entropy()
            if 'chaos_spiral' in self.entropy_modes:
                entropy_bytes += self.chaos_spiral_entropy()
            if 'golden_ratio' in self.entropy_modes:
                entropy_bytes += self.golden_ratio_entropy()
        
        # 7. Pattern-based entropy
        if self.is_palindrome:
            self.log("🔄 Palindrome detected!")
            entropy_bytes += self.palindrome_entropy()
        
        if self.is_ascending:
            self.log("📈 Ascending pattern detected!")
            entropy_bytes += self.ascending_ramp_entropy()
        
        if self.is_descending:
            self.log("📉 Descending pattern detected!")
            entropy_bytes += self.descending_ramp_entropy()
        
        if self.repeating_pattern is not None:
            self.log(f"🔁 Repeating digit: {self.repeating_pattern}")
            entropy_bytes += self.repeating_multiplier_entropy()
        
        # 8. Always-active advanced entropy
        entropy_bytes += self.digit_sum_strategy_entropy()
        entropy_bytes += self.digit_product_chaos_entropy()
        entropy_bytes += self.modulo_time_entropy()
        
        return entropy_bytes
    
    def get_config_summary(self):
        """Get a summary of the current configuration"""
        summary = []
        
        if self.nfc_passkey and len(self.nfc_passkey) >= 4:
            last_4 = self.nfc_passkey[-4:]
            summary.append(f"🔑 NFC Last 4: [{last_4}]")
            
            if self.conversion_log:
                summary.append(f"   🔢 Converted: {self.conversion_log}")
            
            summary.append(f"   ⏱️  Timing: ×{self.timing_multiplier:.1f}")
            summary.append(f"   📊 Samples: {self.sample_count}")
            summary.append(f"   🎲 Modes: {', '.join(self.entropy_modes)}")
            summary.append(f"   ➕ Sum: {self.digit_sum}")
            summary.append(f"   ✖️  Product: {self.digit_product}")
            
            patterns = []
            if self.is_palindrome:
                patterns.append("🔄 Palindrome")
            if self.is_ascending:
                patterns.append("📈 Ascending")
            if self.is_descending:
                patterns.append("📉 Descending")
            if self.repeating_pattern is not None:
                patterns.append(f"🔁 Repeating {self.repeating_pattern}")
            
            if patterns:
                summary.append(f"   🎯 Patterns: {', '.join(patterns)}")
        
        return summary
