class HttpRandomizers:
    @staticmethod
    def status(category: str = "any") -> int:
        """Генерация случайного HTTP статус кода"""
        statuses = {
            "success": [200, 201, 202, 204],
            "client_error": [400, 401, 403, 404, 422, 429],
            "server_error": [500, 501, 502, 503, 504],
            "any": [200, 201, 400, 401, 403, 404, 500, 502, 503]
        }
        return random.choice(statuses.get(category, statuses["any"]))

    @staticmethod
    def user_agent() -> str:
        """Генерация случайного User-Agent"""
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15",
        ]
        return random.choice(user_agents)
