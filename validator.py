import configparser
import os
import uuid
import re
from pathlib import Path

class ConfigValidator:
    def __init__(self, config_path=None):
        if config_path is None:
            config_path = os.getenv("CONFIG_PATH")
            if not config_path:
                raise ValueError("CONFIG_PATH not set and no path provided")
        self.config = configparser.ConfigParser()
        self.config.read(config_path)
        self.errors = []

    def validate(self):
        self._validate_general_section()
        self._validate_watchdog_section()
        return self.errors

    def _validate_general_section(self):
        if "General" not in self.config:
            self.errors.append("Missing 'General' section")
            return

        general = self.config["General"]
        expected_params = {
            "ScanMemoryLimit": self._validate_int_range(1024, 8192),
            "PackageType": lambda x: x.lower() in ["rpm", "deb"],
            "ExecArgMax": self._validate_int_range(10, 100),
            "AdditionalDNSLookup": self._validate_bool,
            "CoreDumps": self._validate_bool,
            "RevealSensitiveInfoInTraces": self._validate_bool,
            "ExecEnvMax": self._validate_int_range(10, 100),
            "MaxInotifyWatches": self._validate_int_range(1000, 1000000),
            "CoreDumpsPath": self._validate_path,
            "UseFanotify": self._validate_bool,
            "KsvlaMode": self._validate_bool,
            "MachineId": self._validate_uuid,
            "StartupTraces": self._validate_bool,
            "MaxInotifyInstances": self._validate_int_range(1024, 8192),
            "Locale": self._validate_locale,
        }

        self._check_params(general, expected_params, "General")

    def _validate_watchdog_section(self):
        if "Watchdog" not in self.config:
            self.errors.append("Missing 'Watchdog' section")
            return

        watchdog = self.config["Watchdog"]
        expected_params = {
            "ConnectTimeout": self._validate_timeout,
            "MaxVirtualMemory": self._validate_memory,
            "MaxMemory": self._validate_memory,
            "PingInterval": self._validate_int_range(100, 10000),
        }

        self._check_params(watchdog, expected_params, "Watchdog")

    
    def _check_params(self, section, expected_params, section_name):
    # Приводим ключи секции к нижнему регистру для сравнения
        section_keys_lower = {k.lower(): k for k in section.keys()}
        expected_params_lower = {k.lower(): v for k, v in expected_params.items()}
    
        for param, validator in expected_params.items():
            param_lower = param.lower()
            if param_lower not in section_keys_lower:
                self.errors.append(f"Missing '{param}' in {section_name}")
            else:
                try:
                    actual_key = section_keys_lower[param_lower]
                    if not validator(section[actual_key]):
                        self.errors.append(f"Invalid value for '{param}' in {section_name}: {section[actual_key]}")
                except (ValueError, TypeError):
                    self.errors.append(f"Invalid format for '{param}' in {section_name}: {section[actual_key]}")

        extra_params = set(section_keys_lower.keys()) - set(expected_params_lower.keys())
        for param_lower in extra_params:
            actual_key = section_keys_lower[param_lower]
            self.errors.append(f"Unexpected parameter '{actual_key}' in {section_name}")

    def _validate_int_range(self, min_val, max_val):
        def validator(value):
            try:
                val = int(value)
                return min_val <= val <= max_val
            except ValueError:
                return False
        return validator

    def _validate_bool(self, value):
        return value.lower() in ["true", "false", "yes", "no"]

    def _validate_path(self, value):
        return Path(value).is_absolute() and Path(value).exists()

    def _validate_uuid(self, value):
        try:
            uuid.UUID(value)
            return True
        except ValueError:
            return False

    def _validate_locale(self, value):
        pattern = r"^[a-z]{2,3}_[A-Z]{2}(?:\.[A-Za-z0-9-]+)?$"
        return bool(re.match(pattern, value))

    def _validate_timeout(self, value):
        if not value.endswith("m"):
            return False
        try:
            val = int(value[:-1])
            return 1 <= val <= 120
        except ValueError:
            return False

    def _validate_memory(self, value):
        if value.lower() in ["off", "auto"]:
            return True
        try:
            val = float(value)
            return 0 < val <= 100
        except ValueError:
            return False