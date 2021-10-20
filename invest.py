import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
from rich import print

st.set_page_config(layout="wide")


def invest_strat_chosen_widget(dict):

    selection = st.radio('Select your investment strategy', [
                         dict[0], dict[1], dict[2]])

    return selection


def initial_investment_amount_widget():

    selection = st.slider('Select your initial investment amount ($)',
                          min_value=0, max_value=100000, value=5000, step=1000, format="$%d")

    return selection


def investment_horizon_widget():

    selection = st.slider(
        'Select your investment horizon (years)', min_value=1, max_value=25, value=10, format="%d years")

    return selection


def investment_period_widget():

    selection = st.radio('Select your investment period', [
        'weekly', 'monthly', 'yearly'])

    return selection


def investment_amount_widget():

    selection = st.slider(
        'Select your investment amount for each period ($)', min_value=0, max_value=2000, value=100, step=10, format="$%d")

    return selection


def get_interest_rate_to_be_used(selection):

    for k, v in invest_strat_dict.items():

        if v['type'] in selection:

            return v['return']


def create_chart_data_init(n, initial_investment_amount, periodic_investment_amount, applied_interest_rate):

    chart_data_init_dict = {}

    for i in range(0, n):

        chart_data_init_dict.setdefault(i, [])

        if i == 0:

            starting_principal = initial_investment_amount

            periodic_investment = 0

        else:

            starting_principal = chart_data_init_dict[i-1]['ending_principal']

            periodic_investment = periodic_investment_amount

        sub_principal_pre_interest = starting_principal + periodic_investment

        interest_for_period = sub_principal_pre_interest * applied_interest_rate

        ending_principal = sub_principal_pre_interest + interest_for_period

        chart_data_init_dict[i] = {
            'starting_principal': starting_principal,
            'periodic_investment': periodic_investment,
            'sub_principal_pre_interest': sub_principal_pre_interest,
            'interest': interest_for_period,
            'ending_principal': ending_principal
        }

    # create data for dataframe

    chart_data_dict = {}

    for i in range(0, n + 1):

        chart_data_dict.setdefault(i, [])

        if i == 0:

            chart_data_dict[i] = initial_investment_amount

        else:

            chart_data_dict[i] = chart_data_init_dict[i-1]['ending_principal']

    return chart_data_dict


CASH_RETURN = 0.005

st.title('Investment Modelling')

invest_strat_dict = {
    0: {
        'type': 'Conservative',
        'return': 0.04
    },
    1: {
        'type': 'Moderate',
        'return': 0.06,
    },
    2: {
        'type': 'Aggressive',
        'return': 0.09
    },

}


invest_strat_choices_dict = {}


for k, v in invest_strat_dict.items():

    return_ = v['return'] * 100

    string = f"{v['type']}: {return_:.2f}%"

    invest_strat_choices_dict.setdefault(k, [])
    invest_strat_choices_dict[k] = string

# create columns

col1, col2 = st.columns(2)

with col1:
    st.header("Investment strategy")
    invest_strat_chosen = invest_strat_chosen_widget(invest_strat_choices_dict)


with col2:
    st.header("Investment horizon")
    investment_horizon = investment_horizon_widget()

col3, col4 = st.columns(2)

with col3:
    st.header("Investment period")
    investment_period = investment_period_widget()


with col4:
    st.header("Investment amount for each period")
    periodic_investment_amount = investment_amount_widget()

col5, col6 = st.columns(2)

with col5:
    st.header("Initial investment amount")
    initial_investment_amount = initial_investment_amount_widget()

# create data for chart
# assumptions:
# for the first period, only the initial amount is added
# if there is a periodic amount, this is added at the start of the second period

# the interest rate is applied at the end of the period


period_n_dict = {
    'weekly': 52,
    'monthly': 12,
    'yearly': 1
}

# get interest rate to be used

interest_rate = get_interest_rate_to_be_used(invest_strat_chosen)

applied_interest_rate = interest_rate / period_n_dict[investment_period]

n = investment_horizon * period_n_dict[investment_period]


chart_data_dict = create_chart_data_init(
    n, initial_investment_amount, periodic_investment_amount, applied_interest_rate)


chart_data = pd.DataFrame.from_dict(
    chart_data_dict, orient='index', columns=['Your Investment'])


st.line_chart(chart_data)
