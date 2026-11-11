# secai // capture the flag

Three flags are hidden on my GitHub profile. Same rule as everything else
here: **proof, not claims** — don't tell me you found them, prove it.

Each flag looks like `secai{...}` and is tucked inside one of the animated
SVGs you can already see on the [profile](https://github.com/maulanawirawan).
Nothing is behind a login, nothing needs a scanner. `view-source`, or just
open the raw `.svg`, is the whole toolkit. Each flag is wrapped in a
different classic encoding — part of the puzzle is noticing which.

## The three stages

| # | where it hides | encoding |
|---|----------------|----------|
| 1 | the board that scans me | base64 |
| 2 | the evidence ladder | hex |
| 3 | the terminal's house rules | rot13 |

## How to submit

1. Decode all three flags.
2. Open an issue with the **CTF submission** template ([new issue](https://github.com/maulanawirawan/maulanawirawan/issues/new?template=ctf.yml)).
3. Paste the three decoded `secai{...}` flags, one per line.

A bot checks your answers **by SHA-256** — the plaintext flags live nowhere
in this repo, only their hashes (below), so the game is provably fair and
you can't grep your way to a win. If all three verify, it signs you into the
[Hall of Fame](HALL-OF-FAME.md) and closes the issue. Partial answers get a
scorecard so you know how many you've got.

## Fair play

- No brute force. The hashes are SHA-256; that's the point.
- Authorized target: **this profile only**. The flags are in these SVGs —
  don't go poking at anything else.
- The verifier is open: [`.github/scripts/ctf_verify.py`](.github/scripts/ctf_verify.py).

## Answer hashes (SHA-256)

```
stage 1  f23dc01e4f20832aaba9ed91f96a71cf85d418930befc2568d57fddc342bcf01
stage 2  0d3df49bf50b735cadab7c0f59c214e0d581893f027ecdf016b66179534ace8b
stage 3  40e4455a767b4063209c316e4426fceb34097be702b36976d08618033780cee0
```

*Hint, if you're stuck on stage 1: it's a comment in the dashboard SVG, and
it ends with `=`.*
