from behave import *
import requests

@when("we request a page") # pylint: disable=undefined-variable
def step_impl(context): # pylint: disable=function-redefined
    url = "http://app:5000/"
    context.response = requests.get(url)


@then("we should get hello world") # pylint: disable=undefined-variable
def step_impl(context): # pylint: disable=function-redefined
    assert context.response.content == b"Hello World!", context.response.content
    
@When("we want a test to fail") # pylint: disable=undefined-variable
def step_impl(context): # pylint: disable=function-redefined
    assert False == True

@When("we want a test to succeed") # pylint: disable=undefined-variable
def step_impl(context):
    assert True == True
