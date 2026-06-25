from enum import Enum


class Category(str, Enum):
    USER_CACHES = "User Caches"
    SYSTEM_LOGS = "System Logs"
    TEMP_FILES = "Temp Files"
    BROWSER_CACHES = "Browser Caches"
    XCODE_ARTIFACTS = "Xcode Artifacts"
    TRASH = "Trash"
    MAIL_DOWNLOADS = "Mail Downloads"
    NODE_CACHE = "Node.js Cache"
    PYTHON_CACHE = "Python Cache"
    DOCKER = "Docker"
    BUILD_CACHE = "Build Cache"
    UNUSED_VENVS = "Unused Venvs"
    HOMEBREW_CACHE = "Homebrew Cache"
    UNUSED_NODE_MODULES = "Unused node_modules"
