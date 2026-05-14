# Trim Long Inclusions

Added `# mccole:name` / `# mccole:/name` marks to five server files so that
`%inc` shortcodes in lessons only show the new or relevant code rather than the
full file. Updated the corresponding `%inc` lines in each lesson's `index.md`.

## Files modified

- `dynamic/server_detail.py`: marks `make-row`, `index`, `detail-fragment`
- `dynamic/index.md`: split single inclusion into three marked inclusions
- `forms/server_upload.py`: marks `csv-dataclass`, `upload-form`, `upload-csv`, `make-app`
- `forms/index.md`: split single inclusion into four marked inclusions
- `testclient/server_pw.py`: mark `make-app` only (file is identical to forms server)
- `testclient/index.md`: replaced full inclusion with `make-app` mark
- `logging/server_stream.py`: marks `logging-setup`, `detail-handler`, `add-handler`
- `logging/index.md`: split inclusion into three marked inclusions
- `logging/server_rotate.py`: marks `configure-logging`, `upload-csv`
- `logging/index.md`: split second inclusion into two marked inclusions
