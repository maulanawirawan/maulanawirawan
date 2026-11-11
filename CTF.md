# secai // capture the flag

Three flags are hidden on my GitHub profile. Same rule as everything else
here: **proof, not claims**. Don't tell me you found them. Prove it, without
giving them away.

Each flag looks like `secai{...}` and sits inside one of the animated SVGs on
the [profile](https://github.com/maulanawirawan). Nothing is behind a login
and nothing needs a scanner: `view-source`, or opening the raw `.svg`, is the
whole toolkit. Each flag is wrapped in a different classic encoding.

## The three stages

| # | where it hides | encoding |
|---|----------------|----------|
| 1 | the board that scans me | base64 |
| 2 | the evidence ladder | hex |
| 3 | the terminal's house rules | rot13 |

## How to submit

**Never post a flag.** Post a proof for each one instead:

```
sha256("<your-github-username>:<flag>")
```

Use your username in lowercase. A proof only works for the account that posts
it, so it gives nothing away in a public issue, and copying someone else's
gets you `0/3`.

bash, macOS, WSL:

```bash
printf '%s' 'yourname:secai{...}' | sha256sum
```

PowerShell:

```powershell
$s = 'yourname:secai{...}'
-join ([Security.Cryptography.SHA256]::Create().ComputeHash([Text.Encoding]::UTF8.GetBytes($s)) | ForEach-Object { $_.ToString('x2') })
```

Then open an issue with the **CTF submission** template
([new issue](https://github.com/maulanawirawan/maulanawirawan/issues/new?template=ctf.yml))
and paste the three digests, one per line.

A bot usually checks the proofs within a minute. Partial answers get a
scorecard. Three out of three signs you into the [Hall of Fame](HALL-OF-FAME.md)
and closes the issue.

## Check a flag before you submit

The SHA-256 of each flag is public, so you can confirm your decoding locally
with `printf '%s' 'secai{...}' | sha256sum`:

```
stage 1  f23dc01e4f20832aaba9ed91f96a71cf85d418930befc2568d57fddc342bcf01
stage 2  0d3df49bf50b735cadab7c0f59c214e0d581893f027ecdf016b66179534ace8b
stage 3  40e4455a767b4063209c316e4426fceb34097be702b36976d08618033780cee0
```

## Fair play

- Authorized target: **this profile only**. The flags are in these SVGs, so
  don't poke at anything else.
- No brute force.
- The verifier is open source: [`.github/scripts/ctf_verify.py`](.github/scripts/ctf_verify.py).
  It decodes the flags from the SVGs, checks them against the hashes above,
  and fails closed if they ever stop matching.

*Stuck on stage 1? It's a comment in the dashboard SVG, and it ends with `=`.*
