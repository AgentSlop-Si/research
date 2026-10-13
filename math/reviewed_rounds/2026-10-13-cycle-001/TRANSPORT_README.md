# Historical checkpoint transport

This directory preserves the previously sealed 22-file historical checkpoint. It does not represent the latest live Google Sheets state or the later research results from 13 October 2026.

The original `archives/prefix_p13.zip` is stored losslessly as two ordered binary parts because its base64 request exceeded the connector's 16 MiB request limit. No original scientific bytes were changed. The original package manifest remains unchanged and applies after reassembly.

From this checkpoint directory, reconstruct the original archive with:

```sh
cat archives/prefix_p13.zip.part-001 archives/prefix_p13.zip.part-002 > archives/prefix_p13.zip
sha256sum archives/prefix_p13.zip
```

The reconstructed file must contain 14,087,042 bytes and have SHA-256 `94e5b0e9af113911817a53c3b9d7a617ae38ca79abd9bbba4e7efb808d526c27`.

Part checksums:

| File | Bytes | SHA-256 |
|---|---:|---|
| prefix_p13.zip.part-001 | 7,864,320 | e042710e6444e13ff1a34885bb06b3dff846e0d996581a1b32d69f1752da4c9a |
| prefix_p13.zip.part-002 | 6,222,722 | dd053791c8a6c81b3ffa3aa1596b120d77f8f05a0d79e4fd675cbf8e3dc9dd7b |

The other 21 original files are stored directly. This is a private archival commit, not a public release, a new scientific review, or a claim that the entire research project is finished.
