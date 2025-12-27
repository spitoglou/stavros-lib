"""Tests for probability utilities."""

import pytest

from stavroslib.probability import (
    convert_dec_to_prob,
    convert_frac_to_dec,
    convert_frac_to_prob,
    convert_prob_to_dec,
    cumulative_binomial_probabilities,
    exact_binomial_probability,
)


class TestOddsConversion:
    """Test odds conversion functions."""

    def test_convert_dec_to_prob(self):
        """Test decimal odds to probability conversion."""
        assert convert_dec_to_prob(2.0) == 0.5
        assert convert_dec_to_prob(4.0) == 0.25
        assert convert_dec_to_prob(2.5) == 0.4
        assert convert_dec_to_prob(1.5) == 0.6667

    def test_convert_prob_to_dec(self):
        """Test probability to decimal odds conversion."""
        assert convert_prob_to_dec(0.5) == 2.0
        assert convert_prob_to_dec(0.25) == 4.0
        assert convert_prob_to_dec(0.2) == 5.0
        assert convert_prob_to_dec(0.1) == 10.0

    def test_convert_frac_to_prob(self):
        """Test fractional odds to probability conversion."""
        assert convert_frac_to_prob(1, 1) == 0.5  # Even odds
        assert convert_frac_to_prob(3, 1) == 0.25  # 3/1 odds
        assert convert_frac_to_prob(1, 4) == 0.8  # 1/4 odds
        assert convert_frac_to_prob(5, 2) == 0.2857  # 5/2 odds

    def test_convert_frac_to_dec(self):
        """Test fractional odds to decimal conversion."""
        assert convert_frac_to_dec(1, 1) == 2.0  # Even odds
        assert convert_frac_to_dec(3, 1) == 4.0  # 3/1 odds
        assert convert_frac_to_dec(5, 2) == 3.5  # 5/2 odds

    def test_roundtrip_conversions(self):
        """Test that conversion roundtrips work correctly."""
        # Dec -> Prob -> Dec
        dec = 2.5
        prob = convert_dec_to_prob(dec)
        dec_back = convert_prob_to_dec(prob)
        assert dec_back == dec

        # Frac -> Prob -> Dec matches Frac -> Dec
        frac_to_dec_direct = convert_frac_to_dec(3, 1)
        frac_to_prob = convert_frac_to_prob(3, 1)
        prob_to_dec = convert_prob_to_dec(frac_to_prob)
        assert frac_to_dec_direct == prob_to_dec


class TestBinomialProbability:
    """Test binomial probability functions."""

    def test_exact_binomial_probability_fair_coin(self):
        """Test exact binomial probability with fair coin."""
        # 10 flips, exactly 5 heads, p=0.5
        prob = exact_binomial_probability(10, 5, 0.5)
        assert 0.24 < prob < 0.25  # ~0.246

    def test_exact_binomial_probability_edge_cases(self):
        """Test exact binomial probability edge cases."""
        # 0 successes
        prob = exact_binomial_probability(10, 0, 0.5)
        assert 0.0009 < prob < 0.001  # ~0.00098

        # All successes
        prob = exact_binomial_probability(10, 10, 0.5)
        assert 0.0009 < prob < 0.001  # ~0.00098

        # Certain success
        prob = exact_binomial_probability(5, 5, 1.0)
        assert prob == 1.0

        # Impossible success
        prob = exact_binomial_probability(5, 5, 0.0)
        assert prob == 0.0

    def test_exact_binomial_probability_asymmetric(self):
        """Test exact binomial probability with asymmetric probability."""
        # 10 trials, 1 success, p=0.33
        prob = exact_binomial_probability(10, 1, 0.33)
        assert 0.08 < prob < 0.10

    def test_cumulative_binomial_probabilities_fair_coin(self):
        """Test cumulative binomial probabilities with fair coin."""
        # 10 flips, k=5, p=0.5
        lt, lte, gt, gte = cumulative_binomial_probabilities(10, 5, 0.5)

        # Check that probabilities sum correctly
        assert abs((lt + gte) - 1.0) < 0.0001
        assert abs((lte + gt) - 1.0) < 0.0001

        # For fair coin, should be symmetric around k=5
        assert abs(lt - gt) < 0.0001

    def test_cumulative_binomial_probabilities_values(self):
        """Test cumulative binomial probabilities return correct values."""
        lt, lte, gt, gte = cumulative_binomial_probabilities(10, 3, 0.2)

        # P(X < 3) should be less than P(X <= 3)
        assert lt < lte

        # P(X > 3) should be less than P(X >= 3)
        assert gt < gte

        # All probabilities should be between 0 and 1
        assert 0 <= lt <= 1
        assert 0 <= lte <= 1
        assert 0 <= gt <= 1
        assert 0 <= gte <= 1

    def test_cumulative_binomial_probabilities_extreme_k(self):
        """Test cumulative binomial probabilities with extreme k values."""
        # k = 0
        lt, lte, gt, gte = cumulative_binomial_probabilities(10, 0, 0.5)
        assert lt == 0.0  # Nothing less than 0
        assert gte == 1.0  # Everything >= 0

        # k = n
        lt, lte, gt, gte = cumulative_binomial_probabilities(10, 10, 0.5)
        assert gt == 0.0  # Nothing greater than n
        assert lte == 1.0  # Everything <= n

    def test_cumulative_binomial_probability_sums(self):
        """Test that cumulative probabilities sum correctly."""
        n, k, p = 20, 10, 0.4
        lt, lte, gt, gte = cumulative_binomial_probabilities(n, k, p)

        # P(X < k) + P(X >= k) = 1
        assert abs((lt + gte) - 1.0) < 1e-10

        # P(X <= k) + P(X > k) = 1
        assert abs((lte + gt) - 1.0) < 1e-10

        # P(X <= k) = P(X < k) + P(X = k)
        exact_k = exact_binomial_probability(n, k, p)
        assert abs((lt + exact_k) - lte) < 1e-10
