import allure
from functools import wraps


class Reporter:
    @staticmethod
    def case(title: str, c_id: int | None = None):
        """
        Декоратор, который:
        - выставляет красивое название теста (allure.title)
        - при переданном case_id добавляет привязку к кейсу в TestOps (allure.id)

        Пример:
            @Reporter.case("Получение обращения Email", case_id=123)
            def test_retrieve_appeal_create_from_email(...): ...
        """

        def decorator(func):
            if c_id is not None:
                func_with_meta = allure.id(int(c_id))(func)
            else:
                func_with_meta = func

            func_with_meta = allure.title(title)(func_with_meta)

            @wraps(func)
            def wrapper(*args, **kwargs):
                print("=" * 100)
                print(
                    f"TEST NAME: '{title}'"
                    + (f" (id={c_id})" if c_id is not None else "")
                )
                print("-" * 100)
                try:
                    result = func_with_meta(*args, **kwargs)
                    print("-" * 100)
                    print(f"Test Passed: '{title}'")
                    print("=" * 100)
                    return result
                except Exception as e:
                    print("-" * 100)
                    print(f"Test Failed: '{title}' - {str(e)}")
                    print("=" * 100)
                    raise

            return wrapper

        return decorator

    @staticmethod
    def hierarchy(epic, feature, story, suite=None):
        """
        Декоратор для создания иерархии тестов, объединяя все декораторы

        :param epic: Название Epic
        :param feature: Название Feature
        :param story: Название Story
        :param suite: Название Suite (опционально, по умолчанию пустая строка)
        """

        def decorator(func_or_class):
            func_or_class = allure.epic(epic)(func_or_class)
            func_or_class = allure.feature(feature)(func_or_class)
            func_or_class = allure.story(story)(func_or_class)

            suite_value = suite if suite is not None else ""
            func_or_class = allure.suite(suite_value)(func_or_class)

            return func_or_class

        return decorator

    @staticmethod
    def step(name):
        allure_step = allure.step(name)

        class AllureStepContext:
            def __enter__(self):
                print(f"{name}")
                allure_step.__enter__()
                return self

            def __exit__(self, exc_type, exc_val, exc_tb):
                return allure_step.__exit__(exc_type, exc_val, exc_tb)

        return AllureStepContext()

    description = allure.description
    feature = allure.feature
    story = allure.story
    epic = allure.epic
    severity = allure.severity
    tag = allure.tag
    link = allure.link
    issue = allure.issue
    testcase = allure.testcase
    suite = allure.suite
    sub_suite = allure.sub_suite
    parent_suite = allure.parent_suite
    label = allure.label
    id = allure.id

    attach = allure.attach
    attach_file = allure.attach.file
    dynamic = allure.dynamic

    @staticmethod
    def message(message_text):
        allure.attach(
            message_text, "Информация", attachment_type=allure.attachment_type.TEXT
        )

    @staticmethod
    def attach_bytes(content, name=None, attachment_type=None):
        if attachment_type:
            allure.attach(content, name=name, attachment_type=attachment_type)
        else:
            allure.attach(content, name=name)
