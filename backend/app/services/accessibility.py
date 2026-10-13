"""Reading preferences stored in the existing student profile JSONB column."""

SIZES = frozenset({"compact", "comfortable", "large"})
DEVICES = frozenset({"phone", "tablet", "desktop"})


def reading_preferences(options):
    options = options if isinstance(options, dict) else {}
    size = options.get("text_size")
    overrides = options.get("text_size_by_device")
    overrides = overrides if isinstance(overrides, dict) else {}
    return {
        "text_size": size if isinstance(size, str) and size in SIZES else "comfortable",
        "text_size_by_device": {
            device: size
            for device, size in overrides.items()
            if device in DEVICES and isinstance(size, str) and size in SIZES
        },
    }


def merge_text_size(options, size, device=None):
    # The caller must lock the student profile before reading and merging.
    result = dict(options or {})
    if device is None:
        result["text_size"] = size
    else:
        result["text_size_by_device"] = {
            **reading_preferences(result)["text_size_by_device"],
            device: size,
        }
    return result
