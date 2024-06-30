class TestPhrase:
    def test_short_phrase(self):
        limit = 15
        print("Enter a phrase shorter than 15 characters")
        phrase = input("Set a phrase: ")
        assert len(phrase) < limit, f"The entered phrase is greater than or equal to {limit} characters"
