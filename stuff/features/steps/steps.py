from behave import *
import requests

@when("we request a page")
def step_impl(context):
    url = "http://app:5000/"
    context.response = requests.get(url)


@then("we should get hello world")
def step_impl(context):
    assert context.response.content == b"Hello World!", context.response.content
    
@When("we want a test to fail")
def step_impl(context):
    pass

@then("it does")
def step_impl(context):
    assert False == True
