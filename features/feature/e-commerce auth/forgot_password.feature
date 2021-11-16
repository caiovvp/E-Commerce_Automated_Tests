Feature: Recover password when you forget it

  Background:
    Given go to login page: http://192.168.201.15:81/login
    When click on /esqueci-minha-senha button

    Scenario: CPF and email are empty
      When type doc: < >
      And type email: < >
      And click on btn-primary button
      Then show CPF/CNPJ não pode estar em branco or CPF/CNPJ inválido on invalid-feedback

    Scenario: CPF and email dont exist
      When type credentials doc and email
      """
        {
          "doc": ["123", "12345678910", "75678237055"],
          "email": ["suporte02connect.com", "suporte02@connect", "suporte02@connect.com.vc"]
        }
      """
      And click on btn-primary button
      Then show CPF/CNPJ inválido or Email inválido on invalid-feedback
      And stay on page: http://192.168.201.15:81/esqueci-minha-senha

    Scenario: CPF and email exist
      When type doc: <27473929291>
      And type email: <suporte02@connect.com.vc>
      And click on btn-primary button
#      Then *EMAIL VERIFICATION NOT WORKING YET*
