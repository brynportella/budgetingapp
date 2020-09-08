# users/forms.py
from django import forms
# TODO: Need to figure out models to import
# from .models import CustomUser

spending_choices=[ ('spending1', 'Spending was much less than income'),
                   ('spending2', 'Spending was a little less than income'),
                   ('spending3', 'Spending was about equal to income'),
                   ('spending4', 'Spending was a little more than income'),
                   ('spending5', 'Spending was much more than income'), ]
bill_pay_choices=[ ('billpay1', 'Paid all our bills on time'),
                   ('billpay2', 'Paid nearly all our bills on time'),
                   ('billpay3', 'Paid most of our bills on time'),
                   ('billpay4', 'Paid some of our bills on time'),
                   ('billpay5', 'Paid very few of our bills on time'), ]
savings_coverage_choices=[ ('savingscoverage1', '6 months or more'),
                           ('savingscoverage2', '3 to 5 months'),
                           ('savingscoverage3', '1 to 3 months'),
                           ('savingscoverage4', '1 to 2 weeks'),
                           ('savingscoverage5', 'Less than 1 week'), ]
confidence_choices=[ ('fincon1', 'Very confident'),
                     ('fincon2', 'Moderately confident'),
                     ('fincon3', 'Somewhat confident'),
                     ('fincon4', 'Slightly confident'),
                     ('fincon5', 'Not at all confident'), ]
credit_score_choices=[ ('creditscore1', 'Excellent'),
                       ('creditscore2', 'Very good'),
                       ('creditscore3', 'Good'),
                       ('creditscore4', 'Fair'),
                       ('creditscore5', 'Poor'),
                       ('creditscore6', 'I don\'t know'), ]
debt_choices=[ ('debt1', 'I do not have any debt'),
               ('debt2', 'Have a managble amount of debt'),
               ('debt3', 'Have a bit more debt than is manageable'),
               ('debt4', 'Have far more debt than is manageable'), ]
insurance_choices=[ ('insurance1', 'Very confident'),
                    ('insurance2', 'Moderately confident'),
                    ('insurance3', 'Somewhat confident'),
                    ('insurance4', 'Slightly confident'),
                    ('insurance5', 'Not at all confident'), 
                    ('insurance6', 'No one in my house has insurance') ]
ethnicity_choices=[ ('ethnicity1', 'Caucasian'),
                    ('ethnicity2', 'African American'),
                    ('ethnicity3', 'Latino'),
                    ('ethnicity4', 'Asian'),
                    ('ethnicity5', 'Native American'),
                    ('ethnicity6', 'Middle Eastern'),
                    ('ethnicity7', 'Other'),
                    ('ethnicity8', 'Prefer not to say'), ]

class OnboardingForm(forms.Form):
  # Tab 1: Bank
  bank_name = forms.CharField(label='Bank name', max_length=100)
  bank_account_name = forms.CharField(label='Bank account name', max_length=100)
  bank_account_number = forms.IntegerField(label='Bank account number', min_value=0)
  # Tab 2: Savings goal
  saving_goal_name = forms.CharField(label='Goal name', max_length=100)
  saving_goal_amount = forms.DecimalField(label='Goal amount', min_value=0.0)
  # Tab 3: Spending vs Income
  spending = forms.ChoiceField(choices=spending_choices, widget=forms.RadioSelect)
  # Tab 4: Income Questionnaire
  income_question_pay_period = forms.DecimalField(min_value=0.0)
  income_question_vary = forms.BooleanField(label='Does your income vary?', widget=forms.CheckboxInput, required=False)
  income_question_pay_freq = forms.DecimalField(label='How frequently do you get paid? (in weeks)', min_value=0.0)
  # Tab 5: Bill Paying
  bill_pay = forms.ChoiceField(label='We\'ve', choices=bill_pay_choices, widget=forms.RadioSelect)
  # Tab 6: Essential bills
  bill_rent = forms.DecimalField(label='Rent', min_value=0.0)
  bill_utilities = forms.DecimalField(label='Utilities', min_value=0.0)
  bill_food = forms.DecimalField(label='Food', min_value=0.0)
  bill_health = forms.DecimalField(label='Health', min_value=0.0)
  bill_other = forms.DecimalField(label='Other', min_value=0.0)
  # Tab 7: Savings coverage questionnaire
  savings_coverage = forms.ChoiceField(choices=savings_coverage_choices, widget=forms.RadioSelect)
  # Tab 8: Financial Confidence
  confidence = forms.ChoiceField(choices=confidence_choices, widget=forms.RadioSelect)
  # Tab 9: Debt
  debt = forms.ChoiceField(choices=debt_choices, widget=forms.RadioSelect)
  # Tab 10: Credit Score Estimate
  credit_score = forms.ChoiceField(choices=credit_score_choices, widget=forms.RadioSelect)
  # Tab 11: Insurance Confidence
  insurance = forms.ChoiceField(choices=insurance_choices, widget=forms.RadioSelect)
  # Tab 12: Ethnicity
  ethnicity = forms.MultipleChoiceField(choices=ethnicity_choices, widget=forms.CheckboxSelectMultiple)
  # Tab 13: Veteran
  veteran = forms.BooleanField(label='Are you an active or veteran armed services member? This is for informational purposes only and will not affect SaverLife eligibility', widget=forms.CheckboxInput, required=False)





