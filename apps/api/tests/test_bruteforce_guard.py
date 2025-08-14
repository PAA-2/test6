from app.core.security_hardening.brute_force_guard import BruteForceGuard
import fakeredis


def test_bruteforce_guard_blocks_after_limit():
    r = fakeredis.FakeRedis()
    guard = BruteForceGuard(redis=r, limit=2, ban_minutes=1)
    assert guard.allow("1.1.1.1", "a@example.com")
    assert guard.allow("1.1.1.1", "a@example.com")
    assert not guard.allow("1.1.1.1", "a@example.com")
    assert not guard.allow("1.1.1.1", "a@example.com")
