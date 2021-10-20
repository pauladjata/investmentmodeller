import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from rich import print

st.set_page_config(layout="wide")

# constants

CASH_RETURN = 0.005


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

    selection = st.radio('Select the period you make regular contributions', [
        'weekly', 'monthly', 'yearly'])

    return selection


def investment_amount_widget(contribution_period):

    string_ = f"Select your regular contribution amount for each {contribution_period} ($)"

    selection = st.slider(
        string_, min_value=0, max_value=2000, value=100, step=10, format="$%d per " + contribution_period)

    return selection


def get_interest_rate_to_be_used(selection):

    for k, v in invest_strat_dict.items():

        if v['type'] in selection:

            return v['return']


def create_chart_data_init(n, initial_investment_amount, periodic_investment_amount, applied_interest_rate, n_periods_per_year):

    chart_data_init_dict = {}

    total_funds_invested = 0

    final_ending_principal = 0

    for i in range(0, n):

        chart_data_init_dict.setdefault(i, [])

        if i == 0:

            starting_principal = initial_investment_amount

            periodic_investment = 0

            total_funds_invested = total_funds_invested + \
                initial_investment_amount + periodic_investment

        else:

            starting_principal = chart_data_init_dict[i-1]['ending_principal']

            periodic_investment = periodic_investment_amount

            total_funds_invested = total_funds_invested + periodic_investment

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

        final_ending_principal = ending_principal

    # create data for dataframe

    chart_data_dict = {}
    compressed_dict = {}
    counter_ = 0

    for i in range(0, n + 1):

        chart_data_dict.setdefault(i, [])

        if i == 0:

            chart_data_dict[i] = initial_investment_amount

        else:

            chart_data_dict[i] = chart_data_init_dict[i-1]['ending_principal']

        # compressed_dict

    for i in range(0, n + 1):

        if i == 0:

            compressed_dict.setdefault(counter_, [])
            compressed_dict[counter_] = initial_investment_amount

        elif i % n_periods_per_year == 0:

            counter_ += 1

            compressed_dict.setdefault(counter_, [])
            compressed_dict[counter_] = chart_data_init_dict[i -
                                                             1]['ending_principal']

    return chart_data_dict, total_funds_invested, final_ending_principal, compressed_dict


st.header('Investment Modelling')

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

col1, col2, col3 = st.columns(3)
col4, col5, col6 = st.columns(3)

period_convert_dict = {
    'weekly': 'week',
    'monthly': 'month',
    'yearly': 'year'
}


with col1:
    st.subheader("Investment strategy")
    invest_strat_chosen = invest_strat_chosen_widget(invest_strat_choices_dict)


with col2:
    st.subheader("Investment horizon")
    investment_horizon = investment_horizon_widget()

with col3:
    st.subheader("Initial investment amount")
    initial_investment_amount = initial_investment_amount_widget()

with col4:
    st.subheader("Regular contribution period")
    investment_period = investment_period_widget()


with col5:
    st.subheader("Regular contribution amount for each period")
    periodic_investment_amount = investment_amount_widget(
        period_convert_dict[investment_period])


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

n_periods_per_year = period_n_dict[investment_period]

applied_interest_rate = interest_rate / n_periods_per_year

n = investment_horizon * n_periods_per_year

# create data for investment
x = create_chart_data_init(
    n, initial_investment_amount, periodic_investment_amount, applied_interest_rate, n_periods_per_year)

chart_data_dict = x[0]
total_funds_invested = x[1]
final_principal = x[2]
compressed_return_data_dict = x[3]

your_investment_return_string = f"Your Investment {(interest_rate * 100):.2f}%"

chart_data_df = pd.DataFrame.from_dict(
    compressed_return_data_dict, orient='index', columns=[your_investment_return_string])

# create data for cash
applied_interest_rate = CASH_RETURN / n_periods_per_year

y = create_chart_data_init(
    n, initial_investment_amount, periodic_investment_amount, applied_interest_rate, n_periods_per_year)
chart_data_CASH_dict = y[0]
final_principal_CASH = y[2]
compressed_return_CASH_data_dict = y[3]

cash_return_string = f"Cash return {(CASH_RETURN * 100):.2f}%"

chart_data_CASH_df = pd.DataFrame.from_dict(
    compressed_return_CASH_data_dict, orient='index', columns=[cash_return_string])

all_chart_data = pd.concat([chart_data_CASH_df, chart_data_df], axis=1)


return_over_funds_invested = final_principal - total_funds_invested
return_over_cash = final_principal - final_principal_CASH

print(all_chart_data)
print(f"total_funds_invested: {total_funds_invested:,}")
print(f"final_principal: {final_principal:,.2f}")
print(f"return_over_funds_invested: {return_over_funds_invested:,.2f}")
print(f"return_over_cash: {return_over_cash:,.2f}")
print(compressed_return_data_dict)

st.subheader("Your investment returns")
string_1 = f"your total funds invested: ${total_funds_invested:,}"
string_2 = f"your total funds returned: ${final_principal:,.2f}"
string_3 = f"your returns over funds invested: ${return_over_funds_invested:,.2f}"
st.write(f"Your returns: {string_1} || {string_2} || {string_3}")

string_4 = f"total cash returns: ${final_principal_CASH:,.2f}"
string_5 = f"total cash returns over your funds invested: ${(final_principal_CASH - total_funds_invested):,.2f}"
string_6 = f"your returns over total cash returns: ${(return_over_cash):,.2f}"
st.write(
    f"Your returns compared to cash: {string_4} || {string_5} || {string_6}")

st.line_chart(all_chart_data)
