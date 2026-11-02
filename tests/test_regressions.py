"""Regression suite: no real keys, cloud requests or device changes."""
import asyncio
import copy
import json
import os
from pathlib import Path
import sys
import unittest
from unittest.mock import patch, AsyncMock

import httpx
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'app'))
from core.ha_client import HAClient

class AuthTests(unittest.IsolatedAsyncioTestCase):
    async def test_environment_credential_and_exact_proxy_path(self):
        with patch.dict(os.environ, {'SUPERVISOR_TOKEN': 'synthetic-test-credential'}, clear=True):
            ha = HAClient()
        def handler(req):
            self.assertEqual(str(req.url), 'http://supervisor/core/api/states')
            self.assertEqual(req.headers['Authorization'], 'Bearer synthetic-test-credential')
            return httpx.Response(200, json=[{'entity_id':'light.office','state':'off'}])
        await ha.client.aclose()
        ha.client = httpx.AsyncClient(base_url=ha.ha_url, headers={'Authorization':'Bearer '+ha.cred}, transport=httpx.MockTransport(handler))
        self.assertEqual((await ha.get_states())[0]['entity_id'], 'light.office')
        await ha.close()

    async def test_s6_file_fallback(self):
        with patch.dict(os.environ, {}, clear=True), patch('core.ha_client.Path.is_file', return_value=True), patch('core.ha_client.Path.read_text', return_value='synthetic-s6-credential' + chr(10)):
            ha = HAClient()
        self.assertEqual(ha.cred, 'synthetic-s6-credential')
        await ha.close()

    async def test_missing_credential_fails_before_request(self):
        with patch.dict(os.environ, {}, clear=True), patch('core.ha_client.Path.is_file', return_value=False):
            with self.assertRaisesRegex(RuntimeError, 'Supervisor credential unavailable'):
                HAClient()

    async def test_service_payload_and_auth(self):
        with patch.dict(os.environ, {'SUPERVISOR_TOKEN':'synthetic-test-credential'}, clear=True):
            ha=HAClient()
        def handler(req):
            self.assertEqual(req.url.path, '/core/api/services/light/turn_on')
            self.assertEqual(json.loads(req.content), {'entity_id':'light.office'})
            self.assertEqual(req.headers['Authorization'],'Bearer synthetic-test-credential')
            return httpx.Response(200,json=[])
        await ha.client.aclose()
        ha.client=httpx.AsyncClient(base_url=ha.ha_url,headers={'Authorization':'Bearer '+ha.cred},transport=httpx.MockTransport(handler))
        await ha.call_service('light','turn_on','light.office')
        await ha.close()

class FlowTests(unittest.IsolatedAsyncioTestCase):
    async def test_multi_tool_round_then_service_then_final(self):
        import main
        from api.chat import chat_completion, ChatRequest
        from core.mcp import MCPToolRegistry, ToolParameter
        registry=MCPToolRegistry()
        events=[]
        @registry.register('search','Search',[ToolParameter(name='query',type='string',description='Query')])
        async def search(query):
            events.append(query)
            return [{'entity_id':'light.office','friendly_name':'Plafoniera Birou'}]
        @registry.register('turn_on','Turn on',[])
        async def turn_on():
            events.append('service')
            return {'success':True}
        def call(id,name,args):
            return {'id':id,'type':'function','function':{'name':name,'arguments':json.dumps(args)}}
        responses=[
            {'role':'assistant','content':None,'reasoning_content':'find devices','tool_calls':[call('a','search',{'query':'Birou'}),call('b','search',{'query':'Plafoniera'})]},
            {'role':'assistant','content':None,'tool_calls':[call('c','turn_on',{})]},
            {'role':'assistant','content':'Am executat comanda.'}
        ]
        calls=[]
        async def complete(**kwargs):
            calls.append(copy.deepcopy(kwargs))
            return {'choices':[{'message':responses[len(calls)-1]}]}
        from types import SimpleNamespace
        main.app.state.config={'system_prompt':'test','temperature':0.7,'max_tokens':256}
        main.app.state.mcp=registry
        main.app.state.xiaomi=SimpleNamespace(chat_completion=complete, model='test',api_base='https://example.invalid')
        result=await chat_completion(ChatRequest(messages=[{'role':'user','content':'Pornește lumina'}]))
        self.assertEqual(events,['Birou','Plafoniera','service'])
        self.assertEqual(result.message.content,'Am executat comanda.')
        msgs=calls[1]['messages']
        self.assertEqual([m['role'] for m in msgs],['system','user','assistant','tool','tool'])
        self.assertEqual(msgs[2]['reasoning_content'],'find devices')
        self.assertEqual(len(msgs[2]['tool_calls']),2)
        self.assertIsInstance(json.loads(msgs[3]['content']),list)
        self.assertIsNotNone(calls[2]['tools'])

class PackagingTests(unittest.TestCase):
    def test_s6_startup_contract(self):
        root=Path(__file__).resolve().parents[1]
        self.assertTrue((root/'scripts/run.sh').read_text().startswith('#!/command/with-contenv bash'))
        self.assertIn('CMD ["/scripts/run.sh"]',(root/'Dockerfile').read_text())

    def test_release_has_matching_changelog(self):
        import yaml
        root=Path(__file__).resolve().parents[1]
        config=yaml.safe_load((root/'config.yaml').read_text())
        self.assertIn('## ['+config['version']+']',(root/'CHANGELOG.md').read_text())
        self.assertTrue(config['homeassistant_api'])

    def test_config_does_not_log_environment(self):
        root=Path(__file__).resolve().parents[1]
        self.assertNotIn('dict(os.environ)',(root/'app/core/config.py').read_text())

if __name__=='__main__':
    unittest.main(verbosity=2)
