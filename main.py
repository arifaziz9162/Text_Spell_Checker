from spellchecker import SpellChecker as PySpellChecker
import logging

# file_handler and stream_handler setup
logger = logging.getLogger("Spell_Checker_Logger")
logger.setLevel(logging.DEBUG)

if logger.hasHandlers():
    logger.handlers.clear()

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(formatter)

file_handler = logging.FileHandler("spell_checker.log")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

logger.addHandler(stream_handler)
logger.addHandler(file_handler)

class SpellCheckError(Exception):
    """Base exception for spell checking errors."""
    pass

class WordCorrectionError(SpellCheckError):
    """Raised when a single word correction fails."""
    def __init__(self, message="Word correction failed."):
        super().__init__(message)

class TextSpellChecker:
    def __init__(self):
        try:
            self.spell = PySpellChecker()
        except Exception as e:
            logger.critical("Failed to initialize PySpellChecker.", exc_info=True)
            raise SpellCheckError("SpellChecker initialization failed.")

    def correct_word_case(self, original, corrected):
        if original.istitle():
            return corrected.title()
        elif original.isupper():
            return corrected.upper()
        else:
            return corrected

    def correct_text(self, text):
        words = text.split()
        corrected_words = []

        for word in words:
            try:
                corrected = self.spell.correction(word.lower())

                if corrected is None:
                    raise WordCorrectionError()

                if corrected == word.lower():
                    corrected_words.append(word)
                else:
                    logger.info(f"Correction '{word}' to '{corrected}'")
                    corrected_words.append(self.correct_word_case(word, corrected))

            except WordCorrectionError as we:
                logger.warning(str(we), exc_info=True)
                corrected_words.append(word)

            except Exception as e:
                logger.error(f"Failed to correct word '{word}'", exc_info=True)
                corrected_words.append(word)

        return ' '.join(corrected_words)

    def run(self):
        print("\n----- Text Spell Checker -----")
        print("Type 'exit' to quit.\n")
        while True:
            try:
                text = input("Enter text to check (or type 'exit' to quit) = ").strip()
                if text.lower() == "exit":
                    logger.info("Program exited by user.")
                    break

                corrected_text = self.correct_text(text)
                print(f"Corrected Text: {corrected_text}")
                logger.info(f"Corrected Text: {corrected_text}")

            except KeyboardInterrupt:
                logger.info("Program interrupted by user.")
                print("\nProgram interrupted. Exiting...")
                break

            except Exception as e:
                logger.critical("Unexpected error in main loop.", exc_info=True)
                print("An unexpected error occurred. Please check logs.")

if __name__ == "__main__":
    try:
        TextSpellChecker().run()
    except SpellCheckError:
        print("Failed to start the Spell Checker. Please check the logs.")
