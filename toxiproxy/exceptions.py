# coding: utf-8

# Custom exceptions to match the exceptions used in the Ruby wrapper
ProxyExists = type("ProxyExists", (Exception,), {})
NotFound = type("NotFound", (Exception,), {})
InvalidToxic = type("InvalidToxic", (Exception,), {})
