# Probability Utilities

## Purpose
Provide utilities for converting between odds formats and calculating binomial probabilities for statistical analysis.

## Requirements

### Requirement: Odds Conversion
The system SHALL provide functions to convert between different odds formats (decimal, probability, fractional).

#### Scenario: Convert decimal odds to probability
- **WHEN** user calls `convert_dec_to_prob(2.5)`
- **THEN** function returns `0.4` (rounded to 4 decimal places)

#### Scenario: Convert probability to decimal odds
- **WHEN** user calls `convert_prob_to_dec(0.25)`
- **THEN** function returns `4.0`

#### Scenario: Convert fractional odds to probability
- **WHEN** user calls `convert_frac_to_prob(3, 1)`
- **THEN** function returns probability equivalent to 3/1 odds

#### Scenario: Convert fractional odds to decimal
- **WHEN** user calls `convert_frac_to_dec(5, 2)`
- **THEN** function returns decimal equivalent of 5/2 fractional odds

### Requirement: Binomial Probability Calculations
The system SHALL provide functions to calculate exact and cumulative binomial probabilities.

#### Scenario: Calculate exact binomial probability
- **WHEN** user calls `exact_binomial_probability(10, 3, 0.5)`
- **THEN** function returns P(X = 3) for X ~ Binomial(10, 0.5)

#### Scenario: Calculate cumulative binomial probabilities
- **WHEN** user calls `cumulative_binomial_probabilities(10, 5, 0.3)`
- **THEN** function returns tuple (P(X < 5), P(X <= 5), P(X > 5), P(X >= 5))

### Requirement: Type Safety
The system SHALL use proper type hints for all probability functions.

#### Scenario: Function signatures with type hints
- **WHEN** developer uses IDE with type checking
- **THEN** all parameters and return types are clearly specified
