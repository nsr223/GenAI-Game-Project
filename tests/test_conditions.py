import pytest

from game.conditions import ConditionError, evaluate, iter_references


class Ctx:
    def __init__(self, flags=(), collected=(), reviewed=(), claims=(), cabins=(), world=None, present=()):
        self.flags, self.collected, self.reviewed = set(flags), set(collected), set(reviewed)
        self.claims, self.cabins, self.world, self.present = set(claims), set(cabins), world or {}, set(present)

    def flag(self, name): return name in self.flags
    def has_collected(self, e): return e in self.collected
    def has_reviewed(self, e): return e in self.reviewed
    def has_claim(self, s, t): return (s, t) in self.claims
    def cabin_authorized(self, c): return c in self.cabins
    def world_value(self, k): return self.world.get(k)
    def npc_present(self, n): return n in self.present


@pytest.mark.parametrize("cond", [None, {}, [], "always"])
def test_trivially_true(cond):
    assert evaluate(cond, Ctx())


def test_flags_and_groups():
    ctx = Ctx(flags={"a"})
    assert evaluate("a", ctx)
    assert not evaluate("b", ctx)
    assert evaluate({"any_of": ["a", "b"]}, ctx)
    assert not evaluate({"all_of": ["a", "b"]}, ctx)
    assert evaluate({"not": "b"}, ctx)
    assert not evaluate(["a", "b"], ctx)


def test_leaf_conditions():
    ctx = Ctx(
        collected={"EV-09"}, reviewed={"EV-10"}, claims={("maya_chen", "t")},
        cabins={"cabin_elena"}, world={"weather": "severe"}, present={"olivia_hart"},
    )
    assert evaluate({"evidence_collected": "EV-09"}, ctx)
    assert not evaluate({"evidence_reviewed": "EV-09"}, ctx)
    assert evaluate({"evidence_reviewed": "EV-10"}, ctx)
    assert evaluate({"claim_recorded": {"speaker": "maya_chen", "topic": "t"}}, ctx)
    assert evaluate({"cabin_authorized": "cabin_elena"}, ctx)
    assert evaluate({"world_equals": {"weather": "severe"}}, ctx)
    assert evaluate({"npc_present": "olivia_hart"}, ctx)


def test_malformed_conditions_raise():
    with pytest.raises(ConditionError):
        evaluate({"bogus": 1}, Ctx())
    with pytest.raises(ConditionError):
        evaluate({"a": 1, "b": 2}, Ctx())
    with pytest.raises(ConditionError):
        evaluate({"claim_recorded": {"speaker": "x"}}, Ctx())


def test_iter_references():
    refs = set(iter_references({"all_of": ["f", {"evidence_reviewed": "EV-09"}, {"not": {"cabin_authorized": "c"}}]}))
    assert refs == {("flag", "f"), ("evidence", "EV-09"), ("cabin", "c")}
