from app.yara_rule.repository import YaraRuleRepository


class YaraRuleUseCase:

    def __init__(self, repository: YaraRuleRepository):
        self.yara_repository_object = repository

    def fetch_all_yara_rules(self):
        return self.yara_repository_object.get_all_yara_rules()

    def save_yara_rule(self, data):
        name = data.get('name')
        tag = data.get('tag')
        rule_content = data.get('rule_content')
        return self.yara_repository_object.save_yara_rule(name, tag, rule_content)

    def delete_yara_rule(self, rule_id):
        self.yara_repository_object.delete_yara_rule(rule_id)

    def get_rule_name(self):
        return self.yara_repository_object.get_all_name()

    def get_paging(self, name_search):
        return self.yara_repository_object.get_paging(name_search)

