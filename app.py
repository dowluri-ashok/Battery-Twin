import streamlit as st

import pandas as pd

import plotly.graph_objects as go

import hmac

# =========================
# PASSWORD PROTECTION
# =========================

def check_password():
    if st.session_state.get("authenticated", False):
        return True

    st.title("🔐 Battery Twin — Secure Access")
    st.write("Enter the password to access the Battery Digital Twin platform.")

    password = st.text_input(
        "Password",
        type="password",
        key="login_password"
    )

    if st.button("Login", type="primary"):
        if hmac.compare_digest(
            password,
            st.secrets["APP_PASSWORD"]
        ):
            st.session_state["authenticated"] = True
            st.rerun()
        else:
            st.error("❌ Incorrect password")

    return False


if not check_password():
    st.stop()


# ============================================================

# PAGE CONFIGURATION

# ============================================================



st.set_page_config(

    page_title="BatteryTwin",

    page_icon="🔋",

    layout="wide"

)





# ============================================================

# FILE NAMES

# ============================================================



BASELINE_FILE = "Battery_Case_1_1p225A.csv"

DESIGN_A_FILE = "Battery_Case_2_2A.csv"

DESIGN_B_FILE = "Battery_Design_B_Thermal.csv"



VALIDATION_FILE = "Battery_Case_2_2p5A.csv"

OVERCURRENT_FILE = "Battery_Case_3_3A.csv"





# ============================================================

# SAFETY LIMITS

# ============================================================



OVER_CURRENT_LIMIT = 2.5

OVER_VOLTAGE_LIMIT = 4.2

UNDER_VOLTAGE_LIMIT = 3.0

WARNING_TEMPERATURE = 45.0

CRITICAL_TEMPERATURE = 60.0





# ============================================================

# SIDEBAR

# ============================================================



st.sidebar.title("🔋 BatteryTwin")

st.sidebar.caption("Battery Energy System Digital Twin")



page = st.sidebar.radio(

    "Navigate",

    [

        "🏠 Overview",

        "⚙️ Configure",

        "🔋 Digital Twin",

        "⚖️ Design Studio",

        "🛡️ Safety Analysis",

        "🧠 Decision Support",

        "🔗 Traceability"

    ]

)





# ============================================================

# HELPER FUNCTIONS

# ============================================================



@st.cache_data

def load_data(filename):

    return pd.read_csv(filename)





def prepare_data(df, max_points=1000):

    """

    Downsample large simulation datasets for faster visualization.

    """

    if len(df) > max_points:

        step = max(1, len(df) // max_points)

        return df.iloc[::step].copy()



    return df.copy()





def calculate_metrics(df):



    final_voltage = df["Voltage"].iloc[-1]



    final_soc = df["SOC"].iloc[-1] * 100



    max_temperature = df["Temperature"].max() - 273.15



    temperature_rise = (

        df["Temperature"].max()

        - df["Temperature"].iloc[0]

    )



    max_current = df["Current"].max()



    average_power = df["Power"].mean()



    max_power_loss = df["PowerLoss"].max()



    fault = int(df["BatteryFault"].max())



    return {

        "Final Voltage (V)": final_voltage,

        "Final SOC (%)": final_soc,

        "Max Temperature (°C)": max_temperature,

        "Temperature Rise (°C)": temperature_rise,

        "Maximum Current (A)": max_current,

        "Average Power (W)": average_power,

        "Max Power Loss (W)": max_power_loss,

        "Fault": fault

    }





# ============================================================

# OVERVIEW

# ============================================================



if page == "🏠 Overview":



    st.title("🔋 BatteryTwin")



    st.subheader(

        "Battery Energy System Digital Twin Platform"

    )



    st.write(

        "A simulation-driven platform for configuring, "

        "monitoring, analyzing and comparing battery "

        "energy-system designs."

    )



    st.divider()



    st.header("🎯 Platform Objective")



    st.write(

        "BatteryTwin helps engineers virtually design, "

        "test, compare and improve battery energy-system "

        "configurations before physical prototyping."

    )



    col1, col2, col3 = st.columns(3)



    with col1:

        st.info(

            "🔧 Configure\n\n"

            "Define battery and operating parameters."

        )



    with col2:

        st.info(

            "📊 Analyze\n\n"

            "Monitor electrical, thermal and safety behaviour."

        )



    with col3:

        st.info(

            "⚖️ Compare\n\n"

            "Evaluate alternative battery designs."

        )



    st.divider()



    st.header("🔄 Digital Twin Workflow")



    st.markdown(

        """

        **Requirements → Configuration → Simulation →

        Monitoring → Safety Analysis → Design Comparison →

        Engineering Recommendation**

        """

    )



    st.divider()



    st.header("🏗️ Current Digital Twin Architecture")



    architecture = pd.DataFrame({

        "Subsystem": [

            "Electrical Model",

            "Thermal Model",

            "BMS Protection",

            "Simulation Data",

            "Analytics",

            "Decision Support"

        ],

        "Implementation": [

            "Simulink Equivalent Circuit Battery",

            "Thermal resistance + thermal capacitance model",

            "Voltage / Current / Temperature / SOC limits",

            "MATLAB/Simulink → CSV",

            "Python + Pandas",

            "BatteryTwin dashboard"

        ]

    })



    st.dataframe(

        architecture,

        use_container_width=True,

        hide_index=True

    )





# ============================================================

# CONFIGURE

# ============================================================



elif page == "⚙️ Configure":



    st.title("⚙️ Battery Configuration")



    st.write(

        "Define the battery operating conditions and "

        "thermal parameters for the Digital Twin."

    )



    st.divider()



    col1, col2 = st.columns(2)



    # --------------------------------------------------------

    # ELECTRICAL PARAMETERS

    # --------------------------------------------------------



    with col1:



        st.subheader("🔋 Electrical Parameters")



        capacity = st.number_input(

            "Battery Capacity (Ah)",

            min_value=0.1,

            value=2.5,

            step=0.1

        )



        current = st.number_input(

            "Discharge Current (A)",

            min_value=0.0,

            value=1.225,

            step=0.1

        )



        initial_soc = st.slider(

            "Initial SOC (%)",

            min_value=0,

            max_value=100,

            value=100

        )



        ambient_temp = st.number_input(

            "Ambient Temperature (°C)",

            value=25.0,

            step=1.0

        )



    # --------------------------------------------------------

    # THERMAL PARAMETERS

    # --------------------------------------------------------



    with col2:



        st.subheader("🌡️ Thermal Parameters")



        rth = st.number_input(

            "Thermal Resistance (K/W)",

            min_value=0.1,

            value=5.0,

            step=0.5

        )



        cth = st.number_input(

            "Thermal Capacitance (J/K)",

            min_value=10.0,

            value=500.0,

            step=50.0

        )



        simulation_time = st.number_input(

            "Simulation Time (s)",

            min_value=10,

            value=3600,

            step=100

        )



    st.divider()



    st.subheader("🛡️ Protection Limits")



    limit_col1, limit_col2, limit_col3, limit_col4 = st.columns(4)



    limit_col1.metric(

        "Over-Current",

        f"{OVER_CURRENT_LIMIT:.1f} A"

    )



    limit_col2.metric(

        "Over-Voltage",

        f"{OVER_VOLTAGE_LIMIT:.1f} V"

    )



    limit_col3.metric(

        "Under-Voltage",

        f"{UNDER_VOLTAGE_LIMIT:.1f} V"

    )



    limit_col4.metric(

        "Critical Temperature",

        f"{CRITICAL_TEMPERATURE:.0f} °C"

    )



    st.divider()



    st.subheader("📋 Current Configuration")



    config_col1, config_col2, config_col3, config_col4 = st.columns(4)



    config_col1.metric(

        "Capacity",

        f"{capacity:.2f} Ah"

    )



    config_col2.metric(

        "Current",

        f"{current:.3f} A"

    )



    config_col3.metric(

        "Initial SOC",

        f"{initial_soc}%"

    )



    config_col4.metric(

        "Ambient",

        f"{ambient_temp:.1f} °C"

    )



    st.divider()



    st.subheader("🌡️ Thermal Configuration")



    thermal_col1, thermal_col2, thermal_col3 = st.columns(3)



    thermal_col1.metric(

        "Thermal Resistance",

        f"{rth:.2f} K/W"

    )



    thermal_col2.metric(

        "Thermal Capacitance",

        f"{cth:.0f} J/K"

    )



    thermal_col3.metric(

        "Simulation Time",

        f"{simulation_time:.0f} s"

    )



    st.success(

        "Configuration ready. These parameters define "

        "the intended operating condition for the Digital Twin."

    )



    st.info(

        "Note: the current prototype visualizes "

        "simulation-derived Simulink datasets. "

        "Changing these fields does not yet launch a new "

        "Simulink simulation automatically."

    )





# ============================================================

# DIGITAL TWIN

# ============================================================



elif page == "🔋 Digital Twin":



    st.title("🔋 Digital Twin")



    st.write(

        "Visualization of battery states generated from "

        "the Simulink battery-energy-system model."

    )



    # --------------------------------------------------------

    # LOAD DATA

    # --------------------------------------------------------



    baseline = load_data(BASELINE_FILE)

    design_a = load_data(DESIGN_A_FILE)

    design_b = load_data(DESIGN_B_FILE)



    baseline_plot = prepare_data(baseline)

    design_a_plot = prepare_data(design_a)

    design_b_plot = prepare_data(design_b)



    design = st.selectbox(

        "Select Digital Twin Configuration",

        [

            "Baseline",

            "Design A",

            "Design B"

        ]

    )



    if design == "Baseline":



        data = baseline_plot



    elif design == "Design A":



        data = design_a_plot



    else:



        data = design_b_plot



    st.divider()



    # --------------------------------------------------------

    # BATTERY STATE

    # --------------------------------------------------------



    st.subheader("🔋 Battery State")



    final_voltage = data["Voltage"].iloc[-1]



    final_soc = data["SOC"].iloc[-1] * 100



    max_temperature = (

        data["Temperature"].max() - 273.15

    )



    max_current = data["Current"].max()



    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)



    with metric_col1:

        st.metric(

            "Voltage",

            f"{final_voltage:.2f} V"

        )



    with metric_col2:

        st.metric(

            "SOC",

            f"{final_soc:.1f}%"

        )



    with metric_col3:

        st.metric(

            "Maximum Temperature",

            f"{max_temperature:.2f} °C"

        )



    with metric_col4:

        st.metric(

            "Maximum Current",

            f"{max_current:.2f} A"

        )



    st.divider()



    # --------------------------------------------------------

    # VOLTAGE

    # --------------------------------------------------------



    st.subheader("🔋 Battery Voltage")



    voltage_plot = data.set_index("Time")[["Voltage"]]



    st.line_chart(voltage_plot)



    # --------------------------------------------------------

    # SOC

    # --------------------------------------------------------



    st.subheader("📈 State of Charge")



    soc_plot = data.set_index("Time")[["SOC"]].copy()



    soc_plot["SOC"] = soc_plot["SOC"] * 100



    st.line_chart(soc_plot)



    # --------------------------------------------------------

    # TEMPERATURE

    # --------------------------------------------------------



    st.subheader("🌡️ Battery Temperature")



    temperature_plot = data.set_index("Time")[["Temperature"]].copy()



    temperature_plot["Temperature"] = (

        temperature_plot["Temperature"] - 273.15

    )



    temperature_plot.columns = ["Temperature (°C)"]



    st.line_chart(temperature_plot)



    # --------------------------------------------------------

    # POWER

    # --------------------------------------------------------



    st.subheader("⚡ Battery Power")



    power_plot = data.set_index("Time")[["Power"]]



    st.line_chart(power_plot)



    st.divider()



    # --------------------------------------------------------

    # SAFETY STATUS

    # --------------------------------------------------------



    st.subheader("🛡️ Digital Twin Safety Status")



    fault = int(data["BatteryFault"].max())



    if fault == 1:



        st.error(

            "🔴 BATTERY FAULT DETECTED"

        )



    else:



        st.success(

            "🟢 Battery operating within protection limits"

        )



    # Current safety check

    if max_current > OVER_CURRENT_LIMIT:



        st.warning(

            f"⚠️ Over-current limit exceeded "

            f"({max_current:.2f} A > "

            f"{OVER_CURRENT_LIMIT:.2f} A)."

        )



    # Voltage safety checks

    if data["Voltage"].max() > OVER_VOLTAGE_LIMIT:



        st.warning(

            "⚠️ Over-voltage limit exceeded."

        )



    if data["Voltage"].min() < UNDER_VOLTAGE_LIMIT:



        st.warning(

            "⚠️ Under-voltage limit exceeded."

        )



    # Temperature safety checks

    if max_temperature > CRITICAL_TEMPERATURE:



        st.error(

            "🔥 Critical temperature limit exceeded."

        )



    elif max_temperature > WARNING_TEMPERATURE:



        st.warning(

            "⚠️ Temperature warning limit exceeded."

        )





# ============================================================

# DESIGN STUDIO

# ============================================================



elif page == "⚖️ Design Studio":



    st.title("⚖️ Design Studio")



    st.write(

        "Compare battery-energy-system configurations "

        "using simulation-derived electrical and "

        "thermal performance."

    )



    st.divider()



    # --------------------------------------------------------

    # LOAD DESIGN DATA

    # --------------------------------------------------------



    baseline = load_data(BASELINE_FILE)

    design_a = load_data(DESIGN_A_FILE)

    design_b = load_data(DESIGN_B_FILE)



    # --------------------------------------------------------

    # DESIGN DICTIONARY

    # --------------------------------------------------------



    designs = {

        "Baseline": baseline,

        "Design A": design_a,

        "Design B": design_b

    }



    # --------------------------------------------------------

    # CALCULATE METRICS

    # --------------------------------------------------------



    results = []



    for name, df in designs.items():



        metrics = calculate_metrics(df)



        results.append({

            "Design": name,

            "Final Voltage (V)": metrics["Final Voltage (V)"],

            "Final SOC (%)": metrics["Final SOC (%)"],

            "Max Temperature (°C)": metrics["Max Temperature (°C)"],

            "Temperature Rise (°C)": metrics["Temperature Rise (°C)"],

            "Maximum Current (A)": metrics["Maximum Current (A)"],

            "Average Power (W)": metrics["Average Power (W)"],

            "Max Power Loss (W)": metrics["Max Power Loss (W)"],

            "Fault": metrics["Fault"]

        })



    comparison = pd.DataFrame(results)



    # --------------------------------------------------------

    # COMPARISON TABLE

    # --------------------------------------------------------



    st.subheader("📊 Design Comparison")



    display_table = comparison.copy()



    display_table["Final Voltage (V)"] = (

        display_table["Final Voltage (V)"].round(3)

    )



    display_table["Final SOC (%)"] = (

        display_table["Final SOC (%)"].round(1)

    )



    display_table["Max Temperature (°C)"] = (

        display_table["Max Temperature (°C)"].round(3)

    )



    display_table["Temperature Rise (°C)"] = (

        display_table["Temperature Rise (°C)"].round(3)

    )



    display_table["Maximum Current (A)"] = (

        display_table["Maximum Current (A)"].round(3)

    )



    display_table["Average Power (W)"] = (

        display_table["Average Power (W)"].round(3)

    )



    display_table["Max Power Loss (W)"] = (

        display_table["Max Power Loss (W)"].round(4)

    )



    st.dataframe(

        display_table,

        use_container_width=True,

        hide_index=True

    )



    st.divider()



    # --------------------------------------------------------

    # POWER COMPARISON

    # --------------------------------------------------------



    st.subheader("⚡ Average Power Comparison")



    power_chart = comparison.set_index("Design")[

        ["Average Power (W)"]

    ]



    st.bar_chart(power_chart)



    # --------------------------------------------------------

    # THERMAL COMPARISON

    # --------------------------------------------------------



    st.subheader("🌡️ Thermal Comparison")



    thermal_chart = comparison.set_index("Design")[

        [

            "Max Temperature (°C)",

            "Temperature Rise (°C)"

        ]

    ]



    st.bar_chart(thermal_chart)



    # --------------------------------------------------------

    # ENGINEERING INTERPRETATION

    # --------------------------------------------------------



    st.divider()



    st.subheader("🔎 Engineering Interpretation")



    baseline_temp = comparison.loc[

        comparison["Design"] == "Baseline",

        "Temperature Rise (°C)"

    ].iloc[0]



    design_b_temp = comparison.loc[

        comparison["Design"] == "Design B",

        "Temperature Rise (°C)"

    ].iloc[0]



    design_a_power = comparison.loc[

        comparison["Design"] == "Design A",

        "Average Power (W)"

    ].iloc[0]



    baseline_power = comparison.loc[

        comparison["Design"] == "Baseline",

        "Average Power (W)"

    ].iloc[0]



    # Avoid division by zero

    if baseline_temp != 0:



        thermal_reduction = (

            (baseline_temp - design_b_temp)

            / baseline_temp

            * 100

        )



    else:



        thermal_reduction = 0



    if baseline_power != 0:



        power_increase = (

            (design_a_power - baseline_power)

            / baseline_power

            * 100

        )



    else:



        power_increase = 0



    col1, col2 = st.columns(2)



    with col1:



        st.metric(

            "Design A Power Increase",

            f"{power_increase:.1f}%"

        )



        st.write(

            "Design A operates at a higher current, "

            "which increases average power output. "

            "However, the higher current also causes "

            "greater battery stress and a lower final SOC."

        )



    with col2:



        st.metric(

            "Design B Thermal Reduction",

            f"{thermal_reduction:.1f}%"

        )



        st.write(

            "Design B improves thermal behaviour through "

            "enhanced cooling while maintaining the same "

            "electrical operating condition as the baseline."

        )



    st.divider()



    # --------------------------------------------------------

    # RECOMMENDATION

    # --------------------------------------------------------



    st.subheader("🏆 Preliminary Design Recommendation")



    st.success(

        "Design B is preferred when thermal management "

        "and safe operation are the primary objectives. "

        "Design A is useful when higher short-term power "

        "delivery is prioritized, but its higher current "

        "increases battery stress."

    )





# ============================================================

# SAFETY ANALYSIS

# ============================================================



elif page == "🛡️ Safety Analysis":



    st.title("🛡️ Safety Analysis")



    st.write(

        "Validation of battery protection logic using "

        "simulation cases representing normal and "

        "over-current operation."

    )



    st.divider()



    # --------------------------------------------------------

    # SAFETY LIMITS

    # --------------------------------------------------------



    st.subheader("🛡️ Defined Protection Limits")



    col1, col2, col3, col4 = st.columns(4)



    col1.metric(

        "Over-Current Limit",

        "2.5 A"

    )



    col2.metric(

        "Over-Voltage Limit",

        "4.2 V"

    )



    col3.metric(

        "Under-Voltage Limit",

        "3.0 V"

    )



    col4.metric(

        "Critical Temperature",

        "60 °C"

    )



    st.divider()



    # --------------------------------------------------------

    # LOAD VALIDATION CASES

    # --------------------------------------------------------



    case_normal = load_data(

        VALIDATION_FILE

    )



    case_overcurrent = load_data(

        OVERCURRENT_FILE

    )



    # --------------------------------------------------------

    # VALIDATION RESULTS

    # --------------------------------------------------------



    normal_fault = int(

        case_normal["BatteryFault"].max()

    )



    overcurrent_fault = int(

        case_overcurrent["BatteryFault"].max()

    )



    normal_current = case_normal["Current"].max()



    overcurrent_current = case_overcurrent["Current"].max()



    summary = pd.DataFrame({



        "Test Case": [

            "2.5 A Validation",

            "3.0 A Over-Current"

        ],



        "Maximum Current (A)": [

            normal_current,

            overcurrent_current

        ],



        "Battery Fault": [

            normal_fault,

            overcurrent_fault

        ],



        "Expected Result": [

            "No over-current fault",

            "Over-current fault"

        ]

    })



    st.subheader("🧪 Safety Validation Cases")



    st.dataframe(

        summary,

        use_container_width=True,

        hide_index=True

    )



    st.divider()



    # --------------------------------------------------------

    # PROTECTION LOGIC RESULT

    # --------------------------------------------------------



    st.subheader("🔍 Protection Logic Result")



    if normal_fault == 0:



        st.success(

            "🟢 2.5 A validation case: "

            "Battery operates without a protection fault."

        )



    else:



        st.error(

            "🔴 2.5 A validation case: "

            "Unexpected battery fault detected."

        )



    if overcurrent_fault == 1:



        st.error(

            "🔴 3.0 A over-current case: "

            "Over-current protection correctly triggered."

        )



    else:



        st.warning(

            "⚠️ 3.0 A over-current case did not trigger "

            "the expected protection fault."

        )



    st.divider()



    # --------------------------------------------------------

    # CURRENT VALIDATION GRAPH

    # --------------------------------------------------------



    st.subheader("📈 Current Validation")



    fig_validation = go.Figure()



    fig_validation.add_trace(

        go.Scatter(

            x=case_normal["Time"],

            y=case_normal["Current"],

            mode="lines",

            name="2.5 A Validation"

        )

    )



    fig_validation.add_trace(

        go.Scatter(

            x=case_overcurrent["Time"],

            y=case_overcurrent["Current"],

            mode="lines",

            name="3.0 A Over-Current"

        )

    )



    fig_validation.add_hline(

        y=OVER_CURRENT_LIMIT,

        line_dash="dash",

        annotation_text="Over-current Limit"

    )



    fig_validation.update_layout(

        title="Current Protection Validation",

        xaxis_title="Time (s)",

        yaxis_title="Current (A)",

        height=450

    )



    st.plotly_chart(

        fig_validation,

        use_container_width=True

    )



    st.divider()



    # --------------------------------------------------------

    # SAFETY CONCLUSION

    # --------------------------------------------------------



    st.subheader("✅ Safety Conclusion")



    st.write(

        """

        The Digital Twin protection logic was validated

        using simulation-derived operating cases.



        The 2.5 A case represents operation at the defined

        current protection threshold, while the 3.0 A case

        intentionally exceeds the 2.5 A limit.



        The over-current case successfully produces a

        battery fault, demonstrating that the Digital Twin

        can identify unsafe operating conditions before

        physical testing.

        """

    )





# ============================================================

# DECISION SUPPORT

# ============================================================



elif page == "🧠 Decision Support":



    st.title("🧠 Decision Support")



    st.write(

        "Engineering recommendation based on the "

        "simulation-derived design comparison."

    )



    st.divider()



    baseline = load_data(BASELINE_FILE)

    design_a = load_data(DESIGN_A_FILE)

    design_b = load_data(DESIGN_B_FILE)



    baseline_metrics = calculate_metrics(baseline)

    design_a_metrics = calculate_metrics(design_a)

    design_b_metrics = calculate_metrics(design_b)



    # --------------------------------------------------------

    # KEY VALUES

    # --------------------------------------------------------



    thermal_reduction = 0



    if baseline_metrics["Temperature Rise (°C)"] != 0:



        thermal_reduction = (

            (

                baseline_metrics["Temperature Rise (°C)"]

                - design_b_metrics["Temperature Rise (°C)"]

            )

            / baseline_metrics["Temperature Rise (°C)"]

            * 100

        )



    power_increase = 0



    if baseline_metrics["Average Power (W)"] != 0:



        power_increase = (

            (

                design_a_metrics["Average Power (W)"]

                - baseline_metrics["Average Power (W)"]

            )

            / baseline_metrics["Average Power (W)"]

            * 100

        )



    # --------------------------------------------------------

    # DECISION SUMMARY

    # --------------------------------------------------------



    st.subheader("📌 Engineering Decision Summary")



    col1, col2, col3 = st.columns(3)



    col1.metric(

        "Baseline Power",

        f"{baseline_metrics['Average Power (W)']:.2f} W"

    )



    col2.metric(

        "Design A Power Increase",

        f"{power_increase:.1f}%"

    )



    col3.metric(

        "Design B Thermal Reduction",

        f"{thermal_reduction:.1f}%"

    )



    st.divider()



    # --------------------------------------------------------

    # RECOMMENDATION

    # --------------------------------------------------------



    st.subheader("🏆 Recommended Design")



    st.success(

        "DESIGN B — Preferred for a balanced battery "

        "energy-system configuration when thermal behaviour "

        "and safe operation are prioritized."

    )



    st.write(

        """

        Design B maintains the baseline electrical operating

        condition while improving thermal behaviour through

        enhanced cooling.



        Design A provides higher short-term power because it

        operates at a higher discharge current. However,

        this comes with higher thermal stress and a lower

        remaining SOC after the same simulation duration.



        Therefore, Design B provides the more balanced

        engineering solution for the current case study.

        """

    )



    st.divider()



    # --------------------------------------------------------

    # TRADE-OFF TABLE

    # --------------------------------------------------------



    st.subheader("⚖️ Design Trade-Off")



    decision_table = pd.DataFrame({



        "Design": [

            "Baseline",

            "Design A",

            "Design B"

        ],



        "Primary Advantage": [

            "Reference configuration",

            "Higher power delivery",

            "Improved thermal behaviour"

        ],



        "Main Trade-Off": [

            "Reference performance",

            "Higher current and thermal stress",

            "Requires enhanced cooling"

        ],



        "Recommended Use": [

            "Reference",

            "High-power operation",

            "Balanced / thermal-focused design"

        ]

    })



    st.dataframe(

        decision_table,

        use_container_width=True,

        hide_index=True

    )



    st.divider()



    st.info(

        "Next engineering step: connect the configuration "

        "parameters directly to the Simulink model so that "

        "BatteryTwin can automatically generate simulation "

        "results for user-defined designs."

    )

if page == "🔗 Traceability":



    st.title("🔗 Traceability")



    st.write(

             "Traceability of requirements, engineering parameters, "

            "models, simulation cases, validation results, and "

            "design decisions."

            )



st.divider()



# --------------------------------------------------------

# REQUIREMENTS

# --------------------------------------------------------



st.subheader("📋 Engineering Requirements")



requirements = pd.DataFrame({



    "Requirement": [

        "Electrical operating range",

        "Current protection",

        "Thermal management",

        "Battery monitoring",

        "Design comparison",

        "Safety validation"

    ],



    "Target / Definition": [

        "3.0–4.2 V",

        "Maximum current = 2.5 A",

        "Limit battery temperature rise",

        "Voltage, current, SOC and temperature",

        "Compare Baseline, Design A and Design B",

        "Validate protection response"

    ]

})



st.dataframe(

    requirements,

    use_container_width=True,

    hide_index=True

)



st.divider()



# --------------------------------------------------------

# REQUIREMENT → MODEL → RESULT

# --------------------------------------------------------



st.subheader("🔄 Requirement → Model → Result")



traceability = pd.DataFrame({



    "Engineering Aspect": [

        "Electrical behaviour",

        "Thermal behaviour",

        "Battery protection",

        "Battery state monitoring",

        "Design optimisation"

    ],



    "Model / Logic": [

        "Equivalent Circuit Battery",

        "Thermal RC model",

        "BMS protection logic",

        "Voltage / Current / SOC / Temperature signals",

        "Baseline vs Design A vs Design B"

    ],



    "Simulation Evidence": [

        "Battery voltage and SOC response",

        "Temperature rise and power loss",

        "BatteryFault signal",

        "Simulation CSV data",

        "Design comparison metrics"

    ],



    "Engineering Decision": [

        "Evaluate operating performance",

        "Evaluate cooling effectiveness",

        "Identify unsafe current conditions",

        "Monitor battery state",

        "Select preferred configuration"

    ]

})



st.dataframe(

    traceability,

    use_container_width=True,

    hide_index=True

)



st.divider()



# --------------------------------------------------------

# VALIDATION EVIDENCE

# --------------------------------------------------------



st.subheader("🧪 Validation Evidence")



col1, col2 = st.columns(2)



with col1:



    st.success(

        "🟢 Normal operation validated\n\n"

        "2.5 A case operates without a battery fault."

    )



with col2:



    st.error(

        "🔴 Protection response validated\n\n"

        "3.0 A case exceeds the 2.5 A limit and "

        "triggers the battery fault."

    )



st.divider()



# --------------------------------------------------------

# DESIGN DECISION

# --------------------------------------------------------



st.subheader("🏆 Traceable Design Decision")



st.info(

    "Design B is recommended for the current case study "

    "because the simulation results show improved thermal "

    "behaviour while maintaining the baseline electrical "

    "operating condition."

)



st.write(

    "Decision basis: electrical performance, thermal "

    "response, protection validation, and design "

    "trade-offs."

)



st.divider()



# --------------------------------------------------------

# DATA FLOW

# --------------------------------------------------------



st.subheader("🔗 Digital Twin Data Flow")



st.code(

    """

Requirements

 ↓

Battery Parameters

 ↓

MATLAB / Simulink Model

 ↓

Electrical + Thermal + BMS Simulation

 ↓

Simulation Results

 ↓

CSV Data

 ↓

BatteryTwin Analytics

 ↓

Design Comparison

 ↓

Safety Validation

 ↓

Engineering Recommendation

    """,

    language="text"

)
