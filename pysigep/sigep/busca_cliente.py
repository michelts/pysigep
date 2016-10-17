# -*- coding: utf-8 -*-
# #############################################################################
#
# The MIT License (MIT)
#
# Copyright (c) 2016 Michell Stuttgart
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
###############################################################################

import xml.etree.cElementTree as Et

from pysigep.base import RequestBaseSIGEPAuthentication
from pysigep.base import ResponseBase
from pysigep.campos import CampoString


class RequestBuscaCliente(RequestBaseSIGEPAuthentication):

    def __init__(self, id_contrato, id_cartao_postagem, usuario, senha):
        super(RequestBuscaCliente, self).__init__(ResponseSolicitaEtiqueta, usuario, senha)

        self.id_contrato = CampoString('idContrato', valor=id_contrato, obrigatorio=True, tamanho=10)
        self.id_cartao_postagem = CampoString('idCartaoPostagem', valor=id_cartao_postagem, obrigatorio=True, tamanho=10)

    def get_data(self):
        xml = RequestBaseSIGEPAuthentication.HEADER
        xml += '<cli:buscaCliente>'
        xml += self.id_contrato.get_xml()
        xml += self.id_cartao_postagem.get_xml()
        xml += super(RequestBuscaCliente, self).get_data()
        xml += '</cli:buscaCliente>'
        xml += RequestBaseSIGEPAuthentication.FOOTER
        return xml


class ResponseSolicitaEtiqueta(ResponseBase):

    def __init__(self):
        super(ResponseSolicitaEtiqueta, self).__init__()

    def _parse_xml(self, xml):
        for end in Et.fromstring(xml).findall('.//return'):
            self.resposta = {
                'cnpj': end.findtext('cnpj'),
                'servicos': []
            }
            for end2 in end.findall('.//contratos/cartoesPostagem/servicos'):
                self.resposta['servicos'].append({
                    'codigo': end2.findtext('codigo'),
                    'descricao': end2.findtext('descricao'),
                    'id': end2.findtext('id'),
                })
