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

    return chart_data_init_dict
