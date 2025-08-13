
# import json

# raw_json = {
#     "PromptInjection": """You are provided with a complete schema, hierarchy, and event definitions for a Plunger Lift Optimization system. Use this knowledge to interpret user queries and generate SQL queries, even if table names are not explicitly mentioned.

# Schema Overview:

# 1. EVENTS (Main anchor linking all event types)
#    Fields: cycle_id, basic_pressure_event, cycle_duration_event, gas_volume_produced_event, plunger_arrival_velocity_event, unexpected_low_casing_pressure, plunger_arrival_status_event, plunger_unsafe_velocity_event, unexpected_low_flow, unexpected_low_cycle_duration, unexpected_high_cycle_duration

# 2. CYCLE_DURATION_EVENTS – Fields: start_time, end_time, total_duration, flow_duration, shutin_duration
# 3. BASIC_PRESSURE_EVENTS – Fields: delta_pt, delta_cp, delta_pl, ph
# 4. GAS_VOLUME_PRODUCED_EVENTS – Fields: gas_volume, cycle_duration_event
# 5. PLUNGER_ARRIVAL_VELOCITY_EVENTS – Fields: arrival_speed
# 6. PLUNGER_UNSAFE_VELOCITY_EVENTS – Fields: velocity_event (FK to PLUNGER_ARRIVAL_VELOCITY_EVENTS)
# 7. PLUNGER_ARRIVAL_STATUS_EVENTS – Fields: non_arrival, unexpected_casing_pressure, unexpected_low_casing_pressure (FK)
# 8. UNEXPECTED_LOW_CASING_PRESSURE_EVENTS – Field: basic_pressure_event (FK to BASIC_PRESSURE_EVENTS)
# 9. UNEXPECTED_LOW_FLOW_EVENTS – Field: gas_volume_produced_event (FK to GAS_VOLUME_PRODUCED_EVENTS)
# 10. UNEXPECTED_LOW_CYCLE_DURATION_EVENTS – Field: cycle_duration_event (FK)
# 11. UNEXPECTED_HIGH_CYCLE_DURATION_EVENTS – Field: cycle_duration_event (FK)

# Event Hierarchy:
# CycleDataEvent → BasicPressureEvent, CycleDurationEvent, GasVolumeProduced, PlungerArrivalVelocity
# CycleAnomalyEvent → PlungerUnsafeVelocity, PlungerArrivalStatus, UnexpectedLowCasingPressure, UnexpectedLowFlow, UnexpectedLowCycleDuration, UnexpectedHighCycleDuration
# PlungerArrivalStatus → UnexpectedLowCasingPressure
# PlungerUnsafeVelocity → PlungerArrivalVelocity
# UnexpectedLowCasingPressure → BasicPressureEvent
# UnexpectedLowFlow → GasVolumeProduced
# UnexpectedLowCycleDuration → CycleDurationEvent
# UnexpectedHighCycleDuration → CycleDurationEvent
# GasVolumeProduced → CycleDurationEvent

# Event Definitions:
# - CycleDataEvent: Top-level container for operational cycle data
# - CycleAnomalyEvent: Top-level container for anomalies
# - BasicPressureEvent: Captures delta_Pt, delta_Cp, delta_Pl, ph (psi)
# - CycleDurationEvent: total_cycle_duration, flow_duration, shutin_duration (seconds)
# - GasVolumeProduced: gas_volume (m³)
# - PlungerArrivalVelocityEvent: arrival_speed (m/s)
# - PlungerArrivalStatus: non_arrival (boolean), UnexpectedLowCasingPressure (boolean)
# - PlungerUnsafeVelocity: Triggered if arrival_speed > safety threshold
# - UnexpectedLowCasingPressure: Triggered if delta_Cp is low
# - UnexpectedLowFlow: Triggered if gas_volume is low
# - UnexpectedLowCycleDuration: Triggered if durations < lower threshold
# - UnexpectedHighCycleDuration: Triggered if durations > upper threshold

# Use this information to answer queries like “show average arrival speed in last 2 days” correctly.
# """
# }

# output_path = "injection.json"
# with open(output_path, "w") as f:
#     json.dump(raw_json, f, indent=2)

# output_path

import json
raw_json = {
"PromptInjection":""" The following is a detailed schema and event hierarchy for a Plunger Lift Optimization system. Use this structure to generate SQL queries based on user input. Table names, fields, and relationships are included below.\n\nSchema Overview:\n\n1. EVENTS (Main relational anchor)\n   - Links all event types by storing their primary keys.\n   - Fields: cycle_id, basic_pressure_event, cycle_duration_event, gas_volume_produced_event, plunger_arrival_velocity_event, unexpected_low_casing_pressure, plunger_arrival_status_event, plunger_unsafe_velocity_event, unexpected_low_flow, unexpected_low_cycle_duration, unexpected_high_cycle_duration\n\n2. CYCLE_DURATION_EVENTS\n   - Fields: start_time, end_time, total_duration, flow_duration, shutin_duration\n   - Represents CycleDurationEvent (core metric)\n\n3. BASIC_PRESSURE_EVENTS\n   - Fields: delta_pt, delta_cp, delta_pl, ph\n   - Represents BasicPressureEvent (core metric)\n\n4. GAS_VOLUME_PRODUCED_EVENTS\n   - Fields: gas_volume, cycle_duration_event\n   - Represents GasVolumeProduced event (core metric)\n\n5. PLUNGER_ARRIVAL_VELOCITY_EVENTS\n   - Fields: arrival_speed\n   - Represents PlungerArrivalVelocityEvent\n\n6. PLUNGER_UNSAFE_VELOCITY_EVENTS\n   - Fields: velocity_event (FK to PLUNGER_ARRIVAL_VELOCITY_EVENTS)\n   - Triggered when arrival_speed > safety threshold\n\n7. PLUNGER_ARRIVAL_STATUS_EVENTS\n   - Fields: non_arrival, unexpected_casing_pressure, unexpected_low_casing_pressure (FK)\n   - Represents PlungerArrivalStatus\n\n8. UNEXPECTED_LOW_CASING_PRESSURE_EVENTS\n   - Field: basic_pressure_event (FK to BASIC_PRESSURE_EVENTS)\n   - Triggered when delta_cp is too low\n\n9. UNEXPECTED_LOW_FLOW_EVENTS\n   - Field: gas_volume_produced_event (FK to GAS_VOLUME_PRODUCED_EVENTS)\n   - Triggered when gas_volume is low\n\n10. UNEXPECTED_LOW_CYCLE_DURATION_EVENTS\n    - Field: cycle_duration_event (FK)\n    - Triggered when total/flow/shutin_duration is too short\n\n11. UNEXPECTED_HIGH_CYCLE_DURATION_EVENTS\n    - Field: cycle_duration_event (FK)\n    - Triggered when total/flow/shutin_duration is too long\n\n\nHierarchical Relationships (for reasoning):\n\n- CycleDataEvent →\n  - BasicPressureEvent (BASIC_PRESSURE_EVENTS)\n  - CycleDurationEvent (CYCLE_DURATION_EVENTS)\n  - GasVolumeProduced (GAS_VOLUME_PRODUCED_EVENTS)\n  - PlungerArrivalVelocity (PLUNGER_ARRIVAL_VELOCITY_EVENTS)\n\n- CycleAnomalyEvent →\n  - PlungerUnsafeVelocity (PLUNGER_UNSAFE_VELOCITY_EVENTS)\n  - PlungerArrivalStatus (PLUNGER_ARRIVAL_STATUS_EVENTS)\n  - UnexpectedLowCasingPressure (UNEXPECTED_LOW_CASING_PRESSURE_EVENTS)\n  - UnexpectedLowFlow (UNEXPECTED_LOW_FLOW_EVENTS)\n  - UnexpectedLowCycleDuration (UNEXPECTED_LOW_CYCLE_DURATION_EVENTS)\n  - UnexpectedHighCycleDuration (UNEXPECTED_HIGH_CYCLE_DURATION_EVENTS)\n\n- PlungerArrivalStatus → UnexpectedLowCasingPressure\n- PlungerUnsafeVelocity → PlungerArrivalVelocity\n- UnexpectedLowCasingPressure → BasicPressureEvent\n- UnexpectedLowFlow → GasVolumeProduced\n- UnexpectedLowCycleDuration → CycleDurationEvent\n- UnexpectedHighCycleDuration → CycleDurationEvent\n- GasVolumeProduced → CycleDurationEvent\n\nUse this knowledge to resolve user prompts like \"show average arrival speed in last 2 days\" even when table names are not explicitly mentioned.""",

"PromptInjection1":""" Here is the hierarchical structure of the events, showing the parent-child relationships based on the provided data.
Plunger Lift Event Hierarchy

    CycleDataEvent (Parent)

        BasicPressureEvent (Child)

        CycleDurationEvent (Child)

        GasVolumeProduced (Child)

        PlungerArrivalVelocity (Child, referred to as velocityEvent)

    CycleAnomalyEvent (Parent)

        PlungerUnsafeVelocity (Child)

        PlungerArrivalStatus (Child, specifically the plungerNonArrival attribute)

        UnexpectedLowCasingPressure (Child)

        UnexpectedLowFlow (Child)

        UnexpectedLowCycleDuration (Child)

        UnexpectedHighCycleDuration (Child)

    PlungerArrivalStatus (Parent)

        UnexpectedLowCasingPressure (Child, as a diagnostic sub-condition)

    PlungerUnsafeVelocity (Parent)

        PlungerArrivalVelocity (Child, as it uses the arrival_speed from this event)

    UnexpectedLowCasingPressure (Parent)

        BasicPressureEvent (Child, as it uses delta_Cp from this event)

    UnexpectedLowFlow (Parent)

        GasVolumeProduced (Child, as it uses the gas_volume from this event)

    UnexpectedLowCycleDuration (Parent)

        CycleDurationEvent (Child, as it uses the duration variables from this event)

    UnexpectedHighCycleDuration (Parent)

        CycleDurationEvent (Child, as it uses the duration variables from this event)

    GasVolumeProduced (Parent)

        CycleDurationEvent (Child, as it uses flow_duration from this event)""",
"event_details":"""

Event Schema Definition

Below are the detailed definitions for each event type.

1. High-Level Composite Events

These events aggregate data from multiple sub-events to provide a holistic view of the cycle.

Event Name: CycleDataEvent

Description: A comprehensive, top-level event that encapsulates the complete operational snapshot of one full plunger lift cycle. It serves as a container for all granular data and sub-events, enabling a unified analysis of the cycle's dynamics and efficiency.

Event Type: Composite Container

Constituent Events:

BasicPressureEvent

CycleDurationEvent

GasVolumeProduced

PlungerArrivalVelocityEvent

Event Name: CycleAnomalyEvent

Description: A high-level alert event triggered when any critical failure, inefficiency, or safety violation occurs during a cycle. It acts as a wrapper, signaling that a cycle has deviated from expected operational behavior and requires review or intervention.

Event Type: Composite Anomaly

Constituent Events (Triggers):

PlungerNonArrival

PlungerUnsafeVelocity

UnexpectedLowCasingPressure

UnexpectedLowFlow

UnexpectedLowCycleDuration

UnexpectedHighCycleDuration

2. Core Operational Metric Events

These events capture the fundamental performance metrics of the cycle.

Event Name: BasicPressureEvent

Description: Captures the key pressure changes that drive the plunger lift cycle. It is essential for evaluating lift readiness, pressure buildup, and the overall hydraulic behavior of the well.

Event Type: Core Metric

Variables:

Variable: delta_Pt

Calculation: Pt_final - Pt_init

Description: The net change in tubing pressure during the cycle.

Units: psi

Variable: delta_Cp

Calculation: Cp_final - Cp_init

Description: The net change in casing pressure, which provides the lifting energy.

Units: psi

Variable: delta_Pl

Calculation: Pl_final - Pl_init

Description: The net change in sales line pressure.

Units: psi

Variable: ph

Calculation: 0.433 * SG * hl

Description: The hydrostatic pressure exerted by the liquid column (hl) in the tubing, based on its specific gravity (SG).

Units: psi

Event Name: CycleDurationEvent

Description: Defines the key time durations of a complete plunger cycle. These segments are crucial for assessing shut-in strategy, lift frequency, and operational efficiency.

Event Type: Core Metric

Variables:

Variable: total_cycle_duration

Calculation: end_time - start_time

Description: The total duration of one complete cycle from start to finish.

Units: seconds

Variable: flow_duration

Calculation: Time when flow rate > 0 (calculated as timestamp of last non-zero flow minus timestamp of first non-zero flow).

Description: The total time the well was open and producing gas.

Units: seconds

Variable: shutin_duration

Calculation: Time when flow rate = 0 (calculated as timestamp of last zero flow minus timestamp of first zero flow).

Description: The total time the well was closed to build pressure.

Units: seconds

Event Name: GasVolumeProduced

Description: Calculates the total gas volume produced during a single cycle. This is a primary indicator of the cycle's productivity.

Event Type: Core Metric

Variables:

Variable: gas_volume

Calculation: flow_rate * flow_duration

Description: The total volume of gas extracted during the cycle's flow period.

Units: cubic meter

3. Plunger Status and Safety Events

These events track the plunger's physical behavior and related safety conditions.

Event Name: PlungerArrivalVelocityEvent

Description: Measures the velocity at which the plunger arrives at the wellhead. It is a critical metric for both performance and safety, reflecting the dynamic energy of the lift.

Event Type: Status & Safety Metric

Variables:

Variable: arrival_speed

Description: The measured velocity of the plunger upon arrival at the surface.

Units: m/s

Event Name: PlungerArrivalStatus

Description: Determines whether the plunger successfully arrived at the surface and provides diagnostic context for failures.

Event Type: Status

Variables:

Variable: non_arrival

Description: A boolean flag where true indicates the plunger did not make it to the surface, and false indicates a successful arrival.

Units: boolean

Variable: UnexpectedLowCasingPressure

Description: A diagnostic boolean flag indicating if a non-arrival was accompanied by insufficient casing pressure.

Units: boolean

Event Name: PlungerUnsafeVelocity

Description: A safety event triggered when the plunger's arrival velocity exceeds a predefined safety threshold, indicating potentially damaging impact forces or aggressive flow conditions.

Event Type: Safety Anomaly

Trigger Condition: arrival_speed > predefined_safety_threshold

Source Variable: PlungerArrivalVelocityEvent.arrival_speed

4. Specific Anomaly Events

These events are triggered when specific operational metrics deviate from their expected thresholds.

Event Name: UnexpectedLowCasingPressure

Description: Identifies abnormally low pressure buildup in the casing, which can result in insufficient force to lift the plunger. This points to issues like gas depletion, leaks, or valve malfunctions.

Event Type: Performance Anomaly

Trigger Condition: BasicPressureEvent.delta_Cp is significantly lower than a predefined system threshold.

Event Name: UnexpectedLowFlow

Description: Raised when the gas volume produced during a cycle is significantly lower than expected. It highlights underperformance, possible early plunger fallback, or poor liquid unloading.

Event Type: Performance Anomaly

Trigger Condition: GasVolumeProduced.gas_volume is below a pre-calculated benchmark.

Event Name: UnexpectedLowCycleDuration

Description: Flags abnormally short cycles, suggesting issues like premature venting, shallow slug formation, or mistimed plunger launches. This helps identify inefficient runtimes.

Event Type: Performance Anomaly

Trigger Condition: Durations from CycleDurationEvent (total, flow, or shut-in) fall below defined lower thresholds.

Event Name: UnexpectedHighCycleDuration

Description: Highlights cycles that exceed acceptable time limits. This can indicate poor liquid unloading, sluggish arrival, or excessive shut-in, signaling a need to rebalance the cycle strategy.

Event Type: Performance Anomaly

Trigger Condition: Durations from CycleDurationEvent (total, flow, or shut-in) are greater than defined upper thresholds."""
}

# Save the properly formatted JSON to file
output_path = "injection.json"
with open(output_path, "w") as f:
    json.dump(raw_json, f, indent=2)

output_path