"""Use Ayrport from plain Python."""

import ayrport          # importing ayrport lets Python import .ayr files

import flightdeck       # this is flightdeck.ayr

print(flightdeck.eta(5600))                   # 6.59
print(flightdeck.callsign("ay", 7))          # AY007
print(flightdeck.Runway("27L", 3900).fits(3000))  # True

# run Ayrport code from a string and get its variables back
ns = ayrport.run("""
counter greet(who):
    depart f"Welcome aboard, {who}"
msg = greet("Python")
""")
print(ns["msg"])

# see the Python an Ayrport snippet compiles to
print(ayrport.transpile('gate fuel < 10: pa "low fuel"'))
