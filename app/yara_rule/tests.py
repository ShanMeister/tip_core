from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch
from elasticsearch_dsl import Search
from django.http import JsonResponse
from .use_case import YaraRuleUseCase


class YaraRuleViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('view')

    @patch('yara_rule.use_case.YaraRuleUseCase.fetch_all_yara_rules')
    def test_get_all_yara_rules_success(self, mock_fetch_all_yara_rules):
        # 模拟返回值
        mock_fetch_all_yara_rules.return_value = [
            {'_source': {'id': '1', 'name': 'sample-rule-1',
                         'rule_content': 'A testing rule #1'}, 'created_date': '2023-05-21T14:20:30.123456',
             'modify_date': '2024-05-21T18:03:16.100939'},
            {'_source': {'id': '2', 'name': 'sample-rule-2',
                         'rule_content': 'A testing rule #2'}, 'created_date': '2023-05-21T14:20:30.123456',
             'modify_date': '2024-05-21T18:02:09.734157'}
        ]

        response = self.client.get(self.url)

        # 检查状态码
        self.assertEqual(response.status_code, 200)

        # 检查返回的数据
        self.assertEqual(response.json(), [
            {'_source': {'id': '1', 'name': 'sample-rule-1',
                         'rule_content': 'A testing rule #1'}, 'created_date': '2023-05-21T14:20:30.123456', 'modify_date': '2024-05-21T18:03:16.100939'},
            {'_source': {'id': '2', 'name': 'sample-rule-2',
                         'rule_content': 'A testing rule #2'}, 'created_date': '2023-05-21T14:20:30.123456', 'modify_date': '2024-05-21T18:02:09.734157'}
        ])

    @patch('yara_rule.use_case.YaraRuleUseCase.fetch_all_yara_rules')
    def test_get_all_yara_rules_failure(self, mock_fetch_all_yara_rules):
        # 模拟抛出异常
        mock_fetch_all_yara_rules.side_effect = Exception("Something went wrong")

        response = self.client.get(self.url)

        # 检查状态码
        self.assertEqual(response.status_code, 400)

        # 检查错误信息
        self.assertEqual(response.json(), {'error': 'Something went wrong'})
