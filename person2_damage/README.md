# Person 2 — OpenQuake Fragility and Damage Analysis

## Overview

This folder contains the implementation, experimental data, and visualization scripts for the building fragility and damage analysis component of our earthquake simulation project.

The initial implementation uses OpenQuake's Nepal Scenario Damage demonstration as a proof of concept to understand how earthquake ground shaking, building exposure data, and fragility curves are combined to estimate structural damage.

## IMPORTANT ##
Before Doing any testing Makes sure to read the OpenQuake Read-Only Array Bug Fix

## Current Implementation

**1. Fragility Model Visualization**

The `plot_fragility.py` script extracts fragility functions from OpenQuake's supplied NRML/XML model and visualizes the probability of exceeding different damage states at various Peak Ground Acceleration (PGA) values.

**2. Scenario Damage Calculation**

OpenQuake was used to perform two linked calculations:

- Hazard Calculation #4 — Generates earthquake ground-motion fields.
- Risk Calculation #5 — Uses those ground-motion fields, exposure data, and fragility curves to estimate building damage.

Both calculations were completed using OpenQuake Engine 3.26.2.

**3. Damage Distribution Visualization**

The `plot_damage.py` script processes exported OpenQuake aggregated risk statistics and generates:

- Expected damage-state counts by realization.
- Percentage distributions across damage states.
- Reusable CSV data for further analysis.

**4. Stored Calculation Data**

The successful hazard and risk HDF5 calculation files are preserved as reference outputs, allowing team members to inspect the experiment without repeating the complete simulation.

These files are not standalone substitutes for installing OpenQuake or preparing new scenario inputs.

## Relevance to Tokyo Earthquake Simulation

The Nepal demonstration provides a reference workflow for the planned Tokyo earthquake simulation.

The same general methodology can be adapted using Tokyo-specific earthquake shaking, building inventories, and scientifically suitable Japanese fragility models.

**Important:** The Nepal damage statistics and fragility curves must not be treated as validated Tokyo damage predictions.

## Future Work

- Perform sensitivity analysis by modifying one fragility assumption.
- Compare original and modified damage distributions.
- Identify and evaluate Japanese building fragility studies.
- Integrate Tokyo building inventories with the hazard results from Person 1.
- Generate building damage statistics suitable for Tokyo map visualization.

## Simulation Reproducibility

The archived calculations were generated using OpenQuake Engine 3.26.2. The original scenario configuration is located in `demos/risk/ScenarioDamage/`.

Calculation IDs are local identifiers from the original OpenQuake environment and may differ on other computers.

The calculation archive should be accompanied by its source configuration, dependency versions, and documentation of any local engine modifications.

