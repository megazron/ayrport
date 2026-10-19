# Ayrport examples

Run any of them with `ayr <file>` from this folder.

## Start here

| File | What it shows |
|---|---|
| [`hello.ayr`](hello.ayr) | `pa` and `checkin`: your first program (asks your name) |
| [`basics.ayr`](basics.ayr) | the whole language on one page |
| [`fizzbuzz.ayr`](fizzbuzz.ayr) | `belt`, `check` / `alt` / `div` on one line each |

## Airport programs

| File | What it shows |
|---|---|
| [`departures_board.ayr`](departures_board.ayr) | a departures board: a `terminal` (class), counters, sorting with `kiosk`, aligned f-strings |
| [`check_in_desk.ayr`](check_in_desk.ayr) | an interactive check-in desk: `checkin`, `screen` / `flagged` for bad input, bag fees |
| [`baggage_claim.ayr`](baggage_claim.ayr) | a baggage carousel: `drop` (generators), `skip`, `leave` |
| [`security_line.ayr`](security_line.ayr) | airport security: custom errors, `flag`, `flagged`, `customs`, `xray` |
| [`boarding_queue.ayr`](boarding_queue.ayr) | boarding by group: `shuttle` over a queue, `load ... from collections` |
| [`seat_map.ayr`](seat_map.ayr) | booking seats on a seat map, rejecting bad bookings |
| [`route_planner.ayr`](route_planner.ayr) | shortest route between airports (Dijkstra's algorithm) |
| [`delay_stats.ayr`](delay_stats.ayr) | a week of delays as a text chart: comprehensions, `statistics` |
| [`airline_fleet.ayr`](airline_fleet.ayr) | inheritance: `terminal Jumbo(Aircraft)`, `super().arrive(...)` |
| [`fleet.ayr`](fleet.ayr) | an overbooked flight: classes and errors together |
| [`lost_and_found.ayr`](lost_and_found.ayr) | saving and loading JSON with `gate open(...)` |
| [`files.ayr`](files.ayr) | writing and reading a text file with `gate` |
| [`countdown_to_takeoff.ayr`](countdown_to_takeoff.ayr) | `wait` between steps; `ayr countdown_to_takeoff.ayr 1` for a slow countdown |

## Several files

| File | What it shows |
|---|---|
| [`airport_lib/`](airport_lib) | an Ayrport **package**: a folder with `__init__.ayr`, `fees.ayr`, `codes.ayr` |
| [`use_package.ayr`](use_package.ayr) | Ayrport loading that package with `load` |
| [`use_package.py`](use_package.py) | plain **Python** importing the same Ayrport package |
| [`flightdeck.ayr`](flightdeck.ayr) + [`embed.py`](embed.py) | Python importing an `.ayr` module and running Ayrport from a string |

See the Python any example turns into with `ayr build <file>`.
