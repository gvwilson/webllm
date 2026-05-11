# Logging Lesson

Date: 2026-05-11 16:18 UTC

## Decisions Made

1. configure_logging() function (not __main__)
2. FileHandler introduced first, then RotatingFileHandler
3. Lesson placed after testclient, before finale
4. One exercise writes logs to the sightings SQLite database

## Files Created

- logging/index.md
- logging/server_log.py (StreamHandler milestone)
- logging/server_logging.py (RotatingFileHandler + try/except final)
- logging/utils.py, style.css, run.sh, sample.log

## Files Modified

- README.md (added Logging lesson)
- glossary/index.md (log-handler, log-level, logger)
- bibliography/index.md (python-logging2025)
- _extras/links.md (python-logging)
