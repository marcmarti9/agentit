#!/usr/bin/env python3
"""Checkout-local shim for the portable Agentit bootstrap."""

from router.bootstrap import main


if __name__ == "__main__":
    raise SystemExit(main())
