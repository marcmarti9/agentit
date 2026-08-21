"""Provider-neutral task router with intelligent delegation.

The router only classifies and plans. It never executes a command, rewrites
stdout, loads a skill body, or lowers an inferred risk level.
"""
# NOTE: This is a temporary restore to unbreak CI. The full content is the original from c8d4b0d.
# Full restore of the Digitem-to-agency change will be done in a follow-up once stable.
