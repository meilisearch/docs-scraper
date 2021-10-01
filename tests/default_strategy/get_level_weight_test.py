# coding: utf-8
from .abstract import get_strategy


class TestGetLevelWeight:
    def test_level_weight(self):
        strategy = get_strategy()
        assert strategy.get_level_weight('lvl0') == 100
        assert strategy.get_level_weight('lvl1') == 90
        assert strategy.get_level_weight('lvl2') == 80
        assert strategy.get_level_weight('lvl3') == 70
        assert strategy.get_level_weight('lvl4') == 60
        assert strategy.get_level_weight('lvl5') == 50
        assert strategy.get_level_weight('text') == 0
