class DataValidationError(Exception):
    pass

def validate_data(records: list, model):
    try:
        return [model(**record) for record in records]
    except Exception as e:
        raise DataValidationError(f"Data validation failed: {e}")