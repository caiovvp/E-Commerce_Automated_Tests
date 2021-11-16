Feature: Log into E-Commerce

  Background:
    Given go to login page: http://192.168.201.15:81/login
    Scenario: User doesnt exist
      When type credentials login_documento and login_password
      """
        {
          "login_documento": ["", "user_test", "78965432108", "50333090055"],
          "login_password": ["", "123123", "test_pwd", "Try@Again$!"]
        }
      """
      And click on login_submit button
      Then stay on page: http://192.168.201.15:81/login
      And show Senha em branco ou inválida or CPF/CNPJ inválido on invalid-feedback

    Scenario: User exists in Database
      When type login_documento: <27473929291>
      And type login_password: <123123>
      And click on login_submit button
      Then redirect to Dashboard page: http://192.168.201.15:81/minha-conta

