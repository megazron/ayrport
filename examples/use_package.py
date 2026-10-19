"""Plain Python using the Ayrport package airport_lib/."""

import ayrport  # noqa: F401  (lets Python import .ayr files)

from airport_lib import bag_fee, format_code

print("fee for a 30 kg bag:", bag_fee(30))
print("flight code:", format_code("ay", 42))
