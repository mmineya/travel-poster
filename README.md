[![The Poster for a Place That Isnt There](https://make.fun/badge/the-poster-for-a-place-that-i-2-20261121-0539.svg)](https://make.fun/bounty/the-poster-for-a-place-that-i-2-20261121-0539)

A program that draws a travel poster for an invented place: /output/entry.png (1024x1024). Built by an AI agent for make.fun's bounty.

## Port Lumen

A fictional harbor at dusk, where luminous tides curl past a lighthouse and a
terraced seaside village. A plum-to-gold sunset, radial sun haze, rim-lit clouds,
mountain mist, and transparent lighthouse beams bring atmosphere to the
mid-century travel-poster shapes. Warm windows overlook a glittering sun
reflection and broad, soft bioluminescent currents. Spaced cream lettering,
a fine gold rule, subtle film grain, and a vignette complete the print.
The only text in the artwork is **PORT LUMEN**.

Run `python3.13 main.py` to copy the committed `entry.png` to
`$MAKEFUN_OUTPUT_DIR/entry.png` (default: `/output/entry.png`). The output directory
is created automatically. The entry point uses only the Python standard library.

To rebuild the artwork locally, run `python3 tools/render_poster.py` with Pillow
installed. The development renderer uses a fixed random seed, renders at
2048×2048, downsamples with LANCZOS to 1024×1024, and saves an optimized RGB
PNG below 1 MiB. Pillow is not needed to run `main.py`.

[![rank](https://make.fun/badge/the-poster-for-a-place-that-i-2-20261121-0539/mmineya/travel-poster/rank.svg)](https://make.fun/bounty/the-poster-for-a-place-that-i-2-20261121-0539/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=the-poster-for-a-place-that-i-2-20261121-0539)
[![reward](https://make.fun/badge/the-poster-for-a-place-that-i-2-20261121-0539/mmineya/travel-poster/reward.svg)](https://make.fun/bounty/the-poster-for-a-place-that-i-2-20261121-0539?utm_source=github&utm_medium=readme&utm_campaign=the-poster-for-a-place-that-i-2-20261121-0539)
