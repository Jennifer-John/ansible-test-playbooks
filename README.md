# ansible-test-playbooks
Generate ansible test playbooks based on template (template/playbook.yml)

Execute playbook to generate test playbooks
  - ansible-playbook tc_gen.yml 

Pre-requisites:
- Populate testcases with failed_when or assert conditions in test-cases.csv file
- Update defaults in 
   - vars/defaults.yml
   - template/connection.yml
