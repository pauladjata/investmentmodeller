import streamlit as st
import streamlit.components.v1 as components
import pandas as pd

st.set_page_config(layout="wide")

# constants

CASH_RETURN = 0.005
initial_investment_amount = 1000
investment_period = 'monthly'
periodic_investment_amount = 100
sub_heading_string_1 = f"If, say, you start with an initial investment amount of ${initial_investment_amount:,} and make regular contributions of ${periodic_investment_amount} every month, "
sub_heading_string_2 = f"the chart below provides a theoretical indication of how an investment could perform depending on the investment strategy and horizon selected."

sub_heading_string = sub_heading_string_1 + sub_heading_string_2


def invest_strat_chosen_widget(dict):

    selection = st.radio('Select your investment strategy', [
                         dict[0], dict[1], dict[2]])

    return selection


def investment_horizon_widget():

    selection = st.slider(
        'Select your investment horizon (years)', min_value=1, max_value=25, value=10, format="%d years")

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
            'ending_principal': ending_principal,
            'total_funds_invested': total_funds_invested
        }

        final_ending_principal = ending_principal

    # create data for dataframe

    chart_data_dict = {}
    compressed_investment_dict = {}
    compressed_funds_employed_dict = {}
    counter_ = 0

    for i in range(0, n + 1):

        chart_data_dict.setdefault(i, [])

        if i == 0:

            chart_data_dict[i] = initial_investment_amount

        else:

            chart_data_dict[i] = chart_data_init_dict[i-1]['ending_principal']

    for i in range(0, n + 1):

        compressed_investment_dict.setdefault(counter_, [])
        compressed_funds_employed_dict.setdefault(counter_, [])

        if i == 0:

            compressed_investment_dict[counter_] = initial_investment_amount
            compressed_funds_employed_dict[counter_] = initial_investment_amount

        elif i % n_periods_per_year == 0:

            counter_ += 1

            compressed_investment_dict[counter_] = chart_data_init_dict[i -
                                                                        1]['ending_principal']
            compressed_funds_employed_dict[counter_] = chart_data_init_dict[i -
                                                                            1]['total_funds_invested']

    return chart_data_dict, total_funds_invested, final_ending_principal, compressed_investment_dict, compressed_funds_employed_dict


st.header('The magic of compounding')

st.write(sub_heading_string)

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
        'type': 'Growth',
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
compressed_funds_employed_data_dict = x[4]

your_investment_return_string = f"Your Investment {(interest_rate * 100):.2f}%"
your_funds_employed_string = f"Your Contributions ${total_funds_invested:,}"

# investment strategy return data
chart_data_df = pd.DataFrame.from_dict(
    compressed_return_data_dict, orient='index', columns=[your_investment_return_string])

# investment strategy return data
funds_employed_df = pd.DataFrame.from_dict(
    compressed_funds_employed_data_dict, orient='index', columns=[your_funds_employed_string])

# create data for cash
applied_interest_rate = CASH_RETURN / n_periods_per_year

y = create_chart_data_init(
    n, initial_investment_amount, periodic_investment_amount, applied_interest_rate, n_periods_per_year)
chart_data_CASH_dict = y[0]
final_principal_CASH = y[2]
compressed_return_CASH_data_dict = y[3]

cash_return_string = f"Cash Return {(CASH_RETURN * 100):.2f}%"

chart_data_CASH_df = pd.DataFrame.from_dict(
    compressed_return_CASH_data_dict, orient='index', columns=[cash_return_string])

all_chart_data = pd.concat(
    [funds_employed_df, chart_data_CASH_df, chart_data_df], axis=1)


return_over_funds_invested = final_principal - total_funds_invested
return_over_cash = final_principal - final_principal_CASH

output_string = f"Your investment returns: turn ${total_funds_invested:,} into ${final_principal:,.2f} after {investment_horizon} years"


st.subheader(output_string)
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
