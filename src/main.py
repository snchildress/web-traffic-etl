from etl.handlers import (
    ExtractionHandler,
    TransformationHandler,
    LoadingHandler
)


def main():
    rows: list[list[str]] = ExtractionHandler.extract()
    transformed_rows: list[list[str]] = TransformationHandler.transform(rows)
    LoadingHandler.load(transformed_rows)


if __name__ == '__main__':
    main()
