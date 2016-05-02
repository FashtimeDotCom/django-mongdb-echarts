# coding:utf:8
import requests
__author__ = 'kevin.gao'

"""
import request
requests.packages.urllib3.disable_warnings()
-----
Use this above to ignore the `InsecureRequestWarning`
"""


class SaltStack(object):

    cookies = None
    host = None

    def __init__(self, host, username, password, port='8000', secure=True, eproto='pam'):
        proto = 'https' if secure else 'http'
        self.host = '%s://%s:%s' % (proto, host, port)

        self.login_url = self.host + "/login"
        self.logout_url = self.host + "/logout"
        self.minions_url = self.host + "/minions"
        self.jobs_url = self.host + "/jobs"
        self.run_url = self.host + "/run"
        self.events_url = self.host + "/events"
        self.ws_url = self.host + "/ws"
        self.hook_url = self.host + "/hook"
        self.stats_url = self.host + "/stats"

        r = requests.post(self.login_url, verify=False, data={'username': username,
                                                              'password': password,
                                                              'eauth': eproto})

        if r.status_code == 200:
            self.cookies = r.cookies
        else:
            raise Exception('Error from source %s' % r.text)

    def cmd_run(self, tgt, commond, expr_form='compound', fun='cmd.run'):
        r = requests.post(self.host, verify=False, cookies=self.cookies, data={'tgt': tgt, 
                                                                               'client': 'local',
                                                                               'expr_form': expr_form,
                                                                               'fun': fun,
                                                                               'arg': commond})
        if r.status_code == 200:
            return r.json()['return'][0]
        else:
            raise Exception('Error from source %s' % r.text)
 
    def manage_status(self):
        r = requests.post(self.host, cookies=self.cookies, data={'client': 'runner',
                                                                 'fun': 'manage.status'})
        if r.status_code == 200:
            return r.json()
        else:
            raise Exception('Error from source %s' % r.text)

    def job_info(self, jid="None"):
        try:
            job_url = self.jobs_url + '/' + jid
        except:
            raise Exception('jid error')
        r = requests.get(job_url, verify=False, cookies=self.cookies)
        if r.status_code == 200:
            return r.json()['info'][0]
        else:
            raise Exception('Error from source %s' % r.text)

    def job_result(self, jid="None"):
        try:
            job_url = self.jobs_url + '/' + jid
        except:
            raise Exception('jid error')
        r = requests.get(job_url, verify=False, cookies=self.cookies)
        if r.status_code == 200:
            return r.json()['return'][0]
        else:
            raise Exception('Error from source %s' % r.text)

    def cp_file(self, tgt, from_path, to_path, expr_form='compound'):
        r = requests.post(self.host, verify=False, cookies=self.cookies, data={'tgt': tgt,
                                                                               'client': 'local',
                                                                               'fun': 'cp.get_file',
                                                                               'arg': [from_path, to_path],})
        if r.status_code == 200:
            print type(r.json())
            return r.json()
        else:
            raise Exception('Error from source %s' % r.text)
 
    def get_minion_detail(self, tgt="*", expr_form='compound', client='runner'):
        r = requests.post(self.minions_url, verify=False, data={'tgt': tgt,
                                                  'fun': "status.diskusage"}, cookies=self.cookies)

        if r.status_code == 202:
            return r.json()['return'][0]
        else:
            raise Exception('Error from source %s' % r.text)

    def get_disk_usage(self, tgt, expr_form='compound'):
        pass

    def get_ip_addr(self, tgt, expr_form='compound', client='local'):
        r = requests.post(self.host, verify=False, data={'fun': 'network.interface_ip',
                                                         'tgt': tgt,
                                                         'client': client,
                                                         'expr_form': expr_form,
                                                         'arg': 'eth0'}, cookies=self.cookies)
        if r.status_code == 200:
            return r.json()['return']
        else:
            raise Exception('Error from source %s' % r.text)

    def restart_service(self, tgt, service, expr_form='compound', client='local'):
        """

        :param tgt: target
        :param service: service name
        :param expr_form:
        :param client:
        :return: :raise Exception:
        """
        r = requests.post(self.host, verify=False, data={'fun': 'service.restart',
                                                         'tgt': tgt,
                                                         'client': client,
                                                         'expr_form': expr_form,
                                                         'arg': service}, cookies=self.cookies)

        if r.status_code == 200:
            return r.json()['return']
        else:
            raise Exception('Error from source %s' % r.text)

    def get_roles(self, tgt, expr_form='compound', client='local'):
        """

        :param tgt: target
        :param expr_form: match style
        :param client: local/runner/wheel
        :return: :raise Exception: api error
        """
        r = requests.post(self.host, data={'fun': 'grains.item',
                                           'tgt': tgt,
                                           'client': client,
                                           'expr_form': expr_form,
                                           'arg': 'ipv4'}, cookies=self.cookies)
        if r.status_code == 200:
            return r.json()['return']
        else:
            raise Exception('Error from source %s' % r.text)


def demo():
    print HOST, PORT, USER, PASS, SECURE
    sapi = SaltStack(host=HOST,
                     port=PORT,
                     username=USER,
                     password=PASS,
                     secure=SECURE)
    print sapi.host
    print sapi.cookies
    print sapi.manage_status()


if __name__ == "__main__":
    from placeholders import *
    demo()
