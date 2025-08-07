import json

# Original content with multiline and unescaped quotes
raw_json = {

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
