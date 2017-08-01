#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import requests
import json
import xml.etree.ElementTree as ElementTree
from javax.servlet.http import HttpServlet

class ImpactServlet(HttpServlet):
    def doGet(self, request, response):
        self.doPost(request, response)

    def doPost(self, request, response):
        serviceToQuery = request.getParameter("service")

        if serviceToQuery == "scopus":
            service = Scopus(request)
        elif serviceToQuery == "wos":
            service = WebOfScience(request)
        else:
            response.sendError(response.SC_NOT_IMPLEMENTED,
                               "Incorrect service '{0}'.".format(serviceToQuery))
            return

        response.setContentType("application/json")
        response.setCharacterEncoding("UTF-8")
        response.getWriter().println(service.query())


class ImpactService(object):
    def __init__(self, request):
        raise NotImplementedError()

    def query(self):
        raise NotImplementedError()


class Scopus(ImpactService):
    QUERY_URL = "https://api.elsevier.com/content/search/scopus?query=doi(" + '{1}' + ")&apiKey={0}&httpAccept=application/json"
    API_KEY = "YOUR-API-KEY"    
    
    def __init__(self, request):
        self.doi = request.getParameter("doi")

    def query(self):
        response = requests.get(self.QUERY_URL.format(self.API_KEY, self.doi))
        return response.text


class WebOfScience(ImpactService):
    QUERY_URL = "http://gateway.webofknowledge.com/gateway/Gateway.cgi"
    QUERY_DOC = """<?xml version="1.0" encoding="UTF-8"?>
<request xmlns="http://www.isinet.com/xrpc42">
    <fn name="LinksAMR.retrieve">
        <list>
            <map>
                <val name="username">your-username</val>
                <val name="password">your-password</val>
            </map>
            <map>
                <list name="WOS">
                    <val>timesCited</val>
                    <val>citingArticlesURL</val>
                </list>
            </map>
            <map>
                <map name="cite_1">
                    <val name="doi">{0}</val>
                </map>
            </map>
        </list>
    </fn>
</request>
"""
    TIMES_CITED_XPATH = ".//wos:map[@name='cite_1']/wos:map[@name='WOS']/wos:val[@name='timesCited']"
    LINKBACK_XPATH = ".//wos:map[@name='cite_1']/wos:map[@name='WOS']/wos:val[@name='citingArticlesURL']"

    def __init__(self, request):
        self.doi = request.getParameter("doi")

    def query(self):
        wosResponse = requests.post(self.QUERY_URL, data=self.QUERY_DOC.format(self.doi))
        return self.buildJsonResponse(wosResponse.text)

    def buildJsonResponse(self, wosXmlResponse):
        root = ElementTree.fromstring(wosXmlResponse)
        namespaces = {"wos": "http://www.isinet.com/xrpc42"}
        timesCited = root.findtext(self.TIMES_CITED_XPATH, namespaces=namespaces)
        linkBack = root.findtext(self.LINKBACK_XPATH, namespaces=namespaces)

        responseData = {}
        responseData["citationCount"] = timesCited
        responseData["linkBack"] = linkBack
        return json.dumps(responseData)
