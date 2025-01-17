lexical_errors = {}
syntax_errors = {}


def report_lexical_error(error_line, dumped_text, error_message):
    if len(dumped_text) > 7:
        dumped_text = dumped_text[:7] + '...'
    if lexical_errors.get(error_line) is None:
        lexical_errors[error_line] = []
    lexical_errors[error_line].append((dumped_text, error_message))


def report_syntax_error(error_line, error_message):
    if syntax_errors.get(error_line) is None:
        syntax_errors[error_line] = []
    syntax_errors[error_line].append(error_message)
