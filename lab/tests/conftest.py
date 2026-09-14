# Present so that pytest puts lab/tests on sys.path (its default `prepend`
# import mode does that for a conftest's directory), which is what lets the
# test modules `from labkit import ...`. lab/check.py inserts the same path by
# hand, so a reader without pytest gets the identical imports.
