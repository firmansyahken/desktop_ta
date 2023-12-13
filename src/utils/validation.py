class Validation:
    @staticmethod
    def required(value):
        return not value.strip()

    @staticmethod
    def numeric(value):
        try:
            float(value)
            return True
        except ValueError:
            return False

    @staticmethod
    def char(value):
        return value.isalpha()

    @staticmethod
    def minmax(value, min_length, max_length):
        return min_length <= len(value) <= max_length

# Contoh penggunaan:
validate = Validation()