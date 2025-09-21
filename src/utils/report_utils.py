import allure
from functools import wraps
from utils.logger import logger


class Reporter:
    @staticmethod
    def title(title_text):
        def decorator(func):
            @allure.title(title_text)
            @wraps(func)
            def wrapper(*args, **kwargs):
                logger.info("=" * 100)
                logger.info(f"StartTest: '{title_text}'")
                logger.info("-" * 100)

                try:
                    result = func(*args, **kwargs)
                    logger.info("-" * 100)
                    logger.info(f"Test Passed: '{title_text}'")
                    logger.info("=" * 100)
                    return result
                except Exception as e:
                    logger.info("-" * 100)
                    logger.error(f"Test Failed: '{title_text}' - {str(e)}")
                    logger.info("=" * 100)
                    raise

            return wrapper

        return decorator

    @staticmethod
    def step(name):
        allure_step = allure.step(name)

        class AllureStepContext:
            def __enter__(self):
                logger.info(f"{name}")
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

