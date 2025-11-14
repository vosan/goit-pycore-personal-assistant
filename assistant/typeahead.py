from prompt_toolkit.completion import Completer, Completion


class Typeahead(Completer):
    """Simple prefix-based completer.

    Expects `hints` to be an iterable of strings.
    """

    def __init__(self, hints):
        # Normalize to a list of strings to avoid passing Enums around.
        self.hints = [str(h) for h in hints]

    def get_completions(self, document, complete_event):
        """
        Provide completions only for the command token (first word).

        Behavior:
        - At the very start (no text) → suggest all commands.
        - While typing the first token (e.g., "ad") → suggest commands that match the prefix.
        - After a space following the first token (i.e., when entering parameters) → no suggestions.
        - If already on second or later token → no suggestions.
        """

        text = document.text_before_cursor or ""
        tokens = text.split()

        # No tokens yet: suggest all commands (empty prefix)
        if len(tokens) == 0:
            for hint in self.hints:
                yield Completion(hint, start_position=0)
            return

        # Typing the first token: offer prefix-based suggestions unless the user added a trailing space
        if len(tokens) == 1 and not text.endswith(" "):
            word = (document.get_word_before_cursor() or "").lower()
            for hint in self.hints:
                if hint.lower().startswith(word):
                    yield Completion(hint, start_position=-len(word))
            return

        # Otherwise (after first space or beyond first token), do not show command suggestions
        return
