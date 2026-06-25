"""macOS notification delivery via UserNotifications (pyobjc).

Falls back silently on non-macOS or missing permission — never crashes the app.
"""
from __future__ import annotations

import sys
import uuid


def _can_notify() -> bool:
    return sys.platform == "darwin"


def notify(title: str, body: str, identifier: str | None = None) -> None:
    """Send a macOS banner notification. No-op if permission not granted."""
    if not _can_notify():
        return
    try:
        import objc                                         # noqa: PLC0415
        from Foundation import NSObject                     # noqa: PLC0415
        from UserNotifications import (                     # noqa: PLC0415
            UNUserNotificationCenter,
            UNMutableNotificationContent,
            UNNotificationRequest,
            UNTimeIntervalNotificationTrigger,
        )

        center = UNUserNotificationCenter.currentNotificationCenter()

        content = UNMutableNotificationContent.alloc().init()
        content.setTitle_(title)
        content.setBody_(body)
        content.setSound_(None)

        trigger = UNTimeIntervalNotificationTrigger.triggerWithTimeInterval_repeats_(1, False)
        req_id  = identifier or str(uuid.uuid4())
        request = UNNotificationRequest.requestWithIdentifier_content_trigger_(
            req_id, content, trigger
        )
        center.addNotificationRequest_withCompletionHandler_(request, None)
    except Exception:
        pass


def request_permission() -> None:
    """Request notification permission on first launch (call once on startup)."""
    if not _can_notify():
        return
    try:
        from UserNotifications import (                     # noqa: PLC0415
            UNUserNotificationCenter,
            UNAuthorizationOptionAlert,
            UNAuthorizationOptionSound,
        )
        center = UNUserNotificationCenter.currentNotificationCenter()
        options = UNAuthorizationOptionAlert | UNAuthorizationOptionSound
        center.requestAuthorizationWithOptions_completionHandler_(options, None)
    except Exception:
        pass


def notify_scan_result(freed_gb: float, junk_gb: float) -> None:
    """Send a contextual scan-result notification."""
    if junk_gb < 0.1:
        return
    body = f"{junk_gb:.1f} GB of junk found — tap to review and clean."
    notify("MacCleaner", body, identifier="scan-result")


def notify_disk_pressure(free_pct: float) -> None:
    """Alert when disk is nearly full."""
    body = f"Only {free_pct:.0f}% disk space remaining. Tap to free space now."
    notify("MacCleaner — Low Disk Space ⚠️", body, identifier="disk-pressure")
