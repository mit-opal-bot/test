Feature: Hello world

  Scenario: Hello world
     When we request a page
     Then we should get hello world

  Scenario: Failure
    When we want a test to fail
    Then it does