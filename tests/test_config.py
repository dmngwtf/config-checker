import pytest
import os
from pathlib import Path
from validator import ConfigValidator

@pytest.fixture
def config_dir(tmp_path):
    config_dir = tmp_path / "configs"
    config_dir.mkdir()
    return config_dir

def create_config(config_dir, filename, content):
    config_path = config_dir / filename
    config_path.write_text(content)
    return config_path

def test_valid_config(config_dir):
    content = """
[General]
ScanMemoryLimit=8192
PackageType=rpm
ExecArgMax=20
AdditionalDNSLookup=false
CoreDumps=no
RevealSensitiveInfoInTraces=true
ExecEnvMax=50
MaxInotifyWatches=300000
CoreDumpsPath=/tmp
UseFanotify=yes
KsvlaMode=no
MachineId=7b5cc0e7-0205-48e1-bf63-347531eef193
StartupTraces=false
MaxInotifyInstances=2048
Locale=en_US.UTF-8
[Watchdog]
ConnectTimeout=20m
MaxVirtualMemory=auto
MaxMemory=70.5
PingInterval=3000
"""
    config_path = create_config(config_dir, "valid_config.ini", content)
    validator = ConfigValidator(config_path)
    errors = validator.validate()
    assert not errors, f"Valid config has errors: {errors}"

def test_missing_general_section(config_dir):
    content = """
[Watchdog]
ConnectTimeout=20m
MaxVirtualMemory=auto
MaxMemory=70.5
PingInterval=3000
"""
    config_path = create_config(config_dir, "missing_general.ini", content)
    validator = ConfigValidator(config_path)
    errors = validator.validate()
    assert "Missing 'General' section" in errors

def test_missing_watchdog_section(config_dir):
    content = """
[General]
ScanMemoryLimit=8192
PackageType=rpm
ExecArgMax=20
AdditionalDNSLookup=false
CoreDumps=no
RevealSensitiveInfoInTraces=true
ExecEnvMax=50
MaxInotifyWatches=300000
CoreDumpsPath=/tmp
UseFanotify=yes
KsvlaMode=no
MachineId=7b5cc0e7-0205-48e1-bf63-347531eef193
StartupTraces=false
MaxInotifyInstances=2048
Locale=en_US.UTF-8
"""
    config_path = create_config(config_dir, "missing_watchdog.ini", content)
    validator = ConfigValidator(config_path)
    errors = validator.validate()
    assert "Missing 'Watchdog' section" in errors

def test_missing_parameter(config_dir):
    content = """
[General]
PackageType=rpm
ExecArgMax=20
AdditionalDNSLookup=false
CoreDumps=no
RevealSensitiveInfoInTraces=true
ExecEnvMax=50
MaxInotifyWatches=300000
CoreDumpsPath=/tmp
UseFanotify=yes
KsvlaMode=no
MachineId=7b5cc0e7-0205-48e1-bf63-347531eef193
StartupTraces=false
MaxInotifyInstances=2048
Locale=en_US.UTF-8
[Watchdog]
ConnectTimeout=20m
MaxVirtualMemory=auto
MaxMemory=70.5
PingInterval=3000
"""
    config_path = create_config(config_dir, "missing_param.ini", content)
    validator = ConfigValidator(config_path)
    errors = validator.validate()
    assert "Missing 'ScanMemoryLimit' in General" in errors

def test_invalid_scan_memory_limit(config_dir):
    content = """
[General]
ScanMemoryLimit=9000
PackageType=rpm
ExecArgMax=20
AdditionalDNSLookup=false
CoreDumps=no
RevealSensitiveInfoInTraces=true
ExecEnvMax=50
MaxInotifyWatches=300000
CoreDumpsPath=/tmp
UseFanotify=yes
KsvlaMode=no
MachineId=7b5cc0e7-0205-48e1-bf63-347531eef193
StartupTraces=false
MaxInotifyInstances=2048
Locale=en_US.UTF-8
[Watchdog]
ConnectTimeout=20m
MaxVirtualMemory=auto
MaxMemory=70.5
PingInterval=3000
"""
    config_path = create_config(config_dir, "invalid_scan_memory.ini", content)
    validator = ConfigValidator(config_path)
    errors = validator.validate()
    assert "Invalid value for 'ScanMemoryLimit' in General: 9000" in errors

def test_invalid_package_type(config_dir):
    content = """
[General]
ScanMemoryLimit=8192
PackageType=apt
ExecArgMax=20
AdditionalDNSLookup=false
CoreDumps=no
RevealSensitiveInfoInTraces=true
ExecEnvMax=50
MaxInotifyWatches=300000
CoreDumpsPath=/tmp
UseFanotify=yes
KsvlaMode=no
MachineId=7b5cc0e7-0205-48e1-bf63-347531eef193
StartupTraces=false
MaxInotifyInstances=2048
Locale=en_US.UTF-8
[Watchdog]
ConnectTimeout=20m
MaxVirtualMemory=auto
MaxMemory=70.5
PingInterval=3000
"""
    config_path = create_config(config_dir, "invalid_package_type.ini", content)
    validator = ConfigValidator(config_path)
    errors = validator.validate()
    assert "Invalid value for 'PackageType' in General: apt" in errors

def test_invalid_uuid(config_dir):
    content = """
[General]
ScanMemoryLimit=8192
PackageType=rpm
ExecArgMax=20
AdditionalDNSLookup=false
CoreDumps=no
RevealSensitiveInfoInTraces=true
ExecEnvMax=50
MaxInotifyWatches=300000
CoreDumpsPath=/tmp
UseFanotify=yes
KsvlaMode=no
MachineId=invalid-uuid
StartupTraces=false
MaxInotifyInstances=2048
Locale=en_US.UTF-8
[Watchdog]
ConnectTimeout=20m
MaxVirtualMemory=auto
MaxMemory=70.5
PingInterval=3000
"""
    config_path = create_config(config_dir, "invalid_uuid.ini", content)
    validator = ConfigValidator(config_path)
    errors = validator.validate()
    assert "Invalid value for 'MachineId' in General: invalid-uuid" in errors

def test_invalid_locale(config_dir):
    content = """
[General]
ScanMemoryLimit=8192
PackageType=rpm
ExecArgMax=20
AdditionalDNSLookup=false
CoreDumps=no
RevealSensitiveInfoInTraces=true
ExecEnvMax=50
MaxInotifyWatches=300000
CoreDumpsPath=/tmp
UseFanotify=yes
KsvlaMode=no
MachineId=7b5cc0e7-0205-48e1-bf63-347531eef193
StartupTraces=false
MaxInotifyInstances=2048
Locale=invalid
[Watchdog]
ConnectTimeout=20m
MaxVirtualMemory=auto
MaxMemory=70.5
PingInterval=3000
"""
    config_path = create_config(config_dir, "invalid_locale.ini", content)
    validator = ConfigValidator(config_path)
    errors = validator.validate()
    assert "Invalid value for 'Locale' in General: invalid" in errors

def test_invalid_timeout(config_dir):
    content = """
[General]
ScanMemoryLimit=8192
PackageType=rpm
ExecArgMax=20
AdditionalDNSLookup=false
CoreDumps=no
RevealSensitiveInfoInTraces=true
ExecEnvMax=50
MaxInotifyWatches=300000
CoreDumpsPath=/tmp
UseFanotify=yes
KsvlaMode=no
MachineId=7b5cc0e7-0205-48e1-bf63-347531eef193
StartupTraces=false
MaxInotifyInstances=2048
Locale=en_US.UTF-8
[Watchdog]
ConnectTimeout=200m
MaxVirtualMemory=auto
MaxMemory=70.5
PingInterval=3000
"""
    config_path = create_config(config_dir, "invalid_timeout.ini", content)
    validator = ConfigValidator(config_path)
    errors = validator.validate()
    assert "Invalid value for 'ConnectTimeout' in Watchdog: 200m" in errors

def test_invalid_memory(config_dir):
    content = """
[General]
ScanMemoryLimit=8192
PackageType=rpm
ExecArgMax=20
AdditionalDNSLookup=false
CoreDumps=no
RevealSensitiveInfoInTraces=true
ExecEnvMax=50
MaxInotifyWatches=300000
CoreDumpsPath=/tmp
UseFanotify=yes
KsvlaMode=no
MachineId=7b5cc0e7-0205-48e1-bf63-347531eef193
StartupTraces=false
MaxInotifyInstances=2048
Locale=en_US.UTF-8
[Watchdog]
ConnectTimeout=20m
MaxVirtualMemory=invalid
MaxMemory=70.5
PingInterval=3000
"""
    config_path = create_config(config_dir, "invalid_memory.ini", content)
    validator = ConfigValidator(config_path)
    errors = validator.validate()
    assert "Invalid value for 'MaxVirtualMemory' in Watchdog: invalid" in errors

def test_extra_parameter(config_dir):
    content = """
[General]
ScanMemoryLimit=8192
PackageType=rpm
ExecArgMax=20
AdditionalDNSLookup=false
CoreDumps=no
RevealSensitiveInfoInTraces=true
ExecEnvMax=50
MaxInotifyWatches=300000
CoreDumpsPath=/tmp
UseFanotify=yes
KsvlaMode=no
MachineId=7b5cc0e7-0205-48e1-bf63-347531eef193
StartupTraces=false
MaxInotifyInstances=2048
Locale=en_US.UTF-8
UnknownParam=test
[Watchdog]
ConnectTimeout=20m
MaxVirtualMemory=auto
MaxMemory=70.5
PingInterval=3000
"""
    config_path = create_config(config_dir, "extra_param.ini", content)
    validator = ConfigValidator(config_path)
    errors = validator.validate()
    assert "Unexpected parameter 'unknownparam' in General" in errors  # Исправленоssert "Unexpected parameter 'UnknownParam' in General" in errors

def test_empty_config(config_dir):
    content = ""
    config_path = create_config(config_dir, "empty_config.ini", content)
    validator = ConfigValidator(config_path)
    errors = validator.validate()
    assert "Missing 'General' section" in errors
    assert "Missing 'Watchdog' section" in errors

def test_config_path_from_env(config_dir, monkeypatch):
    content = """
[General]
ScanMemoryLimit=8192
PackageType=rpm
ExecArgMax=20
AdditionalDNSLookup=false
CoreDumps=no
RevealSensitiveInfoInTraces=true
ExecEnvMax=50
MaxInotifyWatches=300000
CoreDumpsPath=/tmp
UseFanotify=yes
KsvlaMode=no
MachineId=7b5cc0e7-0205-48e1-bf63-347531eef193
StartupTraces=false
MaxInotifyInstances=2048
Locale=en_US.UTF-8
[Watchdog]
ConnectTimeout=20m
MaxVirtualMemory=auto
MaxMemory=70.5
PingInterval=3000
"""
    config_path = create_config(config_dir, "valid_config.ini", content)
    monkeypatch.setenv("CONFIG_PATH", str(config_path))
    validator = ConfigValidator()
    errors = validator.validate()
    assert not errors