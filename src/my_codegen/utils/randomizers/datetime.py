class DateTimeRandomizers:
    @staticmethod
    def datetime_obj(start_year: int = 2020, end_year: int = 2025) -> datetime.datetime:
        """Генерация случайной даты и времени"""
        start_date = datetime.datetime(start_year, 1, 1)
        end_date = datetime.datetime(end_year, 12, 31)

        time_between = end_date - start_date
        days_between = time_between.days
        random_days = random.randrange(days_between)

        random_date = start_date + datetime.timedelta(days=random_days)

        # Добавляем случайное время
        random_time = datetime.timedelta(
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59),
            seconds=random.randint(0, 59)
        )

        return random_date + random_time

    @staticmethod
    def iso_datetime() -> str:
        """Генерация случайной даты в ISO формате"""
        dt = DateTimeRandomizers.datetime_obj()
        return dt.isoformat() + "Z"

    @staticmethod
    def timestamp() -> int:
        """Генерация случайного Unix timestamp"""
        dt = DateTimeRandomizers.datetime_obj()
        return int(dt.timestamp())
