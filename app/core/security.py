import re
import logging

logger = logging.getLogger(__name__)

# Dangerous prompt delimiters and special tokens used across various LLMs
DANGEROUS_DELIMITERS = [
    r"</?user_question>",
    r"</?context>",
    r"</?system>",
    r"</?human>",
    r"</?assistant>",
    r"\[/?INST\]",
    r"<<SYS>>",
    r"<</SYS>>",
    r"<\|im_start\|>",
    r"<\|im_end\|>",
    r"<\|system\|>",
    r"<\|user\|>",
    r"<\|assistant\|>",
]

# Patterns often associated with direct prompt injection / jailbreak attempts
SUSPICIOUS_PROMPT_PATTERNS = [
    r"ignore\s+(?:all\s+)?(?:previous|above)\s+instructions",
    r"disregard\s+(?:all\s+)?(?:previous|prior)\s+instructions",
    r"forget\s+(?:all\s+)?(?:previous|prior)\s+instructions",
    r"you\s+are\s+now\s+in\s+dan\s+mode",
    r"developer\s+override\s+mode",
    r"system\s*:\s*override",
    r"reveal\s+(?:your\s+)?(?:system\s+prompt|instructions)",
]

_DELIMITER_REGEX = re.compile("|".join(DANGEROUS_DELIMITERS), re.IGNORECASE)
_SUSPICIOUS_REGEX = re.compile("|".join(SUSPICIOUS_PROMPT_PATTERNS), re.IGNORECASE)


def sanitize_user_input(text: str) -> str:
    """Sanitize user input to prevent delimiter injection and remove control characters."""
    if not text:
        return ""

    # Remove null bytes and non-printable control characters
    cleaned = "".join(ch for ch in text if ch.isprintable() or ch in ("\n", "\r", "\t"))

    # Neutralize dangerous delimiter tags by replacing angle brackets in matching tags
    cleaned = _DELIMITER_REGEX.sub(lambda m: m.group(0).replace("<", "[").replace(">", "]"), cleaned)

    # Check for suspicious patterns and log a warning for auditing
    if _SUSPICIOUS_REGEX.search(cleaned):
        logger.warning(f"Suspicious prompt injection pattern detected in input: {cleaned[:100]}...")

    return cleaned.strip()
