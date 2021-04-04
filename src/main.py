from etl.handlers import ExtractionHandler, TransformationHandler


def main():
    rows: list[list[str]] = ExtractionHandler.extract()
    TransformationHandler.transform(rows)


if __name__ == '__main__':
    main()
