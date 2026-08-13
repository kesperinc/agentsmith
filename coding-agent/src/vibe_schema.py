# -*- coding: utf-8 -*-
"""
Agent Smith - Vibe Coding Schema Module
Intent-Driven Autonomous Code Generation Data Schemas
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum


class VibeStatus(Enum):
    PENDING = "PENDING"
    PARSING_INTENT = "PARSING_INTENT"
    GENERATING = "GENERATING"
    SANDBOX_TESTING = "SANDBOX_TESTING"
    CORRECTING = "CORRECTING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"


@dataclass
class VibeGeneratedFile:
    file_path: str
    content: str
    language: str
    is_tested: bool = False
    test_passed: bool = True
    error_log: Optional[str] = None


@dataclass
class VibeIntent:
    user_prompt: str
    domain: str
    framework: str
    target_files: List[str] = field(default_factory=list)
    description: str = ""


@dataclass
class VibeResult:
    session_id: str
    intent: VibeIntent
    status: VibeStatus
    generated_files: List[VibeGeneratedFile] = field(default_factory=list)
    correction_count: int = 0
    message: str = ""
