#!/usr/bin/env python3
# coding: utf8
import pytest

from controller.Controller import Controller
from controller.DocController import DocController

from test.test_functions import *

def make(old_function):
    def new_function(a):
        print(a)
        assert a == 2
        old_function()
    return new_function


class TestDocument:
    @pytest.fixture
    def create_tables(self):
        pass
        Controller.recreate_tables()

    def test_create_documents(self,create_tables):
        print('\033[01m## Creation ##\033[0m')
        make(lambda: DocController.create_document({
            'title': 'title',
            'subject': 'Subject1',
            'type': 'type',
            'description': 'a description',
            'link': '1.gif'
        }))(2)

        # make_test(lambda: DocController.create_document({
        #     'title': 'title',
        #     'subject': 'Subject1',
        #     'type': 'type',
        #     'description': 'a description',
        #     'link': '1.gif'
        # }))("create document","{'visualization': {'quaternionX': None, 'positionY': None, 'quaternionZ': None, 'quaternionY': None, 'quaternionW': None, 'id': 1, 'positionZ': None, 'positionX': None}, 'valid_doc': None, 'id': 1, 'to_validate_doc': {'id_to_validate': 1}, 'metaData': {'title': 'title', 'description': 'a description', 'publicationDate': None, 'originalName': None, 'subject': 'Subject1', 'refDate': None, 'id': 1, 'type': 'type', 'link': '1.gif'}}")
        #
        # DocController.create_document({
        #     'title': 'title',
        #     'subject': 'Subject1',
        #     'type': 'type',
        #     'description': 'a description',
        #     'link': '1.gif'
        # }, "create document","{'visualization': {'quaternionX': None, 'positionY': None, 'quaternionZ': None, 'quaternionY': None, 'quaternionW': None, 'id': 1, 'positionZ': None, 'positionX': None}, 'valid_doc': None, 'id': 1, 'to_validate_doc': {'id_to_validate': 1}, 'metaData': {'title': 'title', 'description': 'a description', 'publicationDate': None, 'originalName': None, 'subject': 'Subject1', 'refDate': None, 'id': 1, 'type': 'type', 'link': '1.gif'}}")
#         make_test(lambda: DocController.create_document({
#             'title': 'title',
#             'subject': 'Subject1',
#             'type': 'type',
#             'description': 'a description',
#             'link': '1.gif'}))(
#              'all needed attributes', False)
#
#         make_test(lambda: DocController.create_document({
#             'title': 'title',
#             'subject': 'Subject2',
#             'type': 'type',
#             'description': 'a description',
#             'link': '2.gif',
#             'refDate': '2019-02-05'
#         }))( 'all needed attributes', False)
#
#         make_test(lambda: DocController.create_document({
#             'title': 'another title',
#             'subject': 'Subject3',
#             'type': 'type',
#             'non_attr': 'non_value',
#             'refDate': '2018-12-03',
#             'description': 'an other description',
#             'link': '3.png'
#         }))( 'needed + nonexistent attributes', False)
#
#         make_test(lambda: DocController.create_document({
#             'title': 'another title'
#         }))( 'needed argument missing', True)
#
#     @staticmethod
#     def read_documents():
#         print('\n\033[01m## Reading ##\033[0m')
#
#         make_test(lambda: DocController.get_documents({}))(
#              'all documents', False)
#
#         make_test(lambda: DocController.get_documents({
#             'keyword': 'description',
#             'refDateStart': '2018-12-03'
#         }))( 'specific documents', False)
#
#         make_test(lambda: DocController.get_document_by_id(1))(
#              'document with existing id', False)
#
#         make_test(lambda: DocController.get_document_by_id(-1))(
#              'document with non existing id', True)
#
#     @staticmethod
#     def update_documents():
#         print('\n\033[01m## Updating ##\033[0m')
#         make_test(lambda: DocController.update_document(1, {
#             'positionX': 12,
#             'description': 'description of a document'
#         }))( 'existing document', False)
#
#         make_test(lambda: DocController.update_document(1, {
#             'positionX': 12,
#             'description': 'another description'
#         }))( 'existing document', False)
#
#         make_test(lambda: DocController.update_document(-1, {
#             'positionX': 12,
#             'description': 'description of a document'
#         }))( 'existing document', True)
#
#     @staticmethod
#     def delete_documents():
#         print('\n\033[01m## Deletion ##\033[0m')
#         make_test(lambda: DocController.delete_documents(2))(
#              'existing document', False)
#
#         make_test(lambda: DocController.delete_documents(2))(
#              'non existing document', True)
#
#
# if __name__ == '__main__':
#     Controller.recreate_tables()
#     TestDocument.create_documents()
#     TestDocument.read_documents()
#     TestDocument.update_documents()
#     TestDocument.read_documents()
#     TestDocument.delete_documents()
#     TestDocument.read_documents()
#     print('\n\n\033[04mSuccess\033[01m: ',
#           TestDocument.nb_tests_succeed, '/',
#           TestDocument.nb_tests, sep='')
