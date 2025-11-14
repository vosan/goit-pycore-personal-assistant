from prompt_toolkit.completion import Completer, Completion


class Typeahead(Completer):
    """Simple prefix-based completer.

    Expects `hints` to be an iterable of strings.
    """

    def __init__(self, hints):
        # Normalize to a list of strings to avoid passing Enums around.
        self.hints = [str(h) for h in hints]

    def get_completions(self, document, complete_event):
        word = (document.get_word_before_cursor() or "").lower()
        for hint in self.hints:
            if hint.lower().startswith(word):
                # Provide the plain text (not Enum) to prompt_toolkit
                yield Completion(hint, start_position=-len(word))
