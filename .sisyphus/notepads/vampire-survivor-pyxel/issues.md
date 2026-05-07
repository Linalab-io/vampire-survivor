# Issues

(No issues yet)

## Final QA - 2026-05-07
- Known issue still present and observed in code: `draw_playing` always uses `SPR_KNIGHT`, so selected character sprite is not reflected during gameplay.
- `validate_script` still reports known warnings for `math.sin/cos` and one `blt()` without `colkey`; accepted as non-blocking per F3 context.
