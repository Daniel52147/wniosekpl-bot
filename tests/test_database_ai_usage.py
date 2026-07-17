import asyncio

import src.database as database


def test_ai_question_usage_is_recorded_and_deleted(tmp_path, monkeypatch):
    monkeypatch.setattr(database, "DATABASE_PATH", tmp_path / "test.db")

    async def scenario():
        await database.init_db()
        await database.upsert_user(123, "user", "User", "ru")

        assert await database.ai_questions_today(123) == 0

        await database.record_ai_question(123, "Как получить PESEL?", "pesel")

        assert await database.ai_questions_today(123) == 1
        stats = await database.get_stats()
        assert stats["ai_questions"] == 1
        assert stats["ai_questions_7d"] == 1

        await database.delete_user_data(123)
        assert await database.ai_questions_today(123) == 0

    asyncio.run(scenario())
