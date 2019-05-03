#!/usr/bin/env python3
# coding: utf8
import pytest
import sqlalchemy.orm

from controller.Controller import Controller
from controller.DocController import DocController


class TestDocument:
    def test_create_documents_1(self):
        Controller.recreate_tables()
        print("Create a valid document")
        expected_response = {
            'id': 1,
            'metaData': {
                'title': 'title',
                'type': 'type',
                'description': 'a description',
                'link': '1.gif',
                'subject': 'Subject1',
                'originalName': None,
                'id': 1,
                'refDate': None,
                'publicationDate': None},
            'visualization': {
                'quaternionW': None,
                'quaternionX': None,
                'positionY': None,
                'quaternionY': None,
                'quaternionZ': None,
                'positionX': None,
                'positionZ': None,
                'id': 1}}

        assert expected_response == DocController.create_document({
            'title': 'title',
            'subject': 'Subject1',
            'type': 'type',
            'description': 'a description',
            'link': '1.gif'
        })

    def test_create_documents_2(self):
        print("needed + nonexistent attributes")
        expected_response = {
            'id': 2,
            'metaData': {
                'title': 'title2',
                'type': 'type2',
                'description': 'another description',
                'link': '2.gif',
                'subject': 'Subject2',
                'originalName': None,
                'id': 2,
                'refDate': None,
                'publicationDate': None},
            'visualization': {
                'quaternionW': None,
                'quaternionX': None,
                'positionY': None,
                'quaternionY': None,
                'quaternionZ': None,
                'positionX': None,
                'positionZ': None,
                'id': 2}}
        assert expected_response == DocController.create_document({
            'title': 'title2',
            'subject': 'Subject2',
            'type': 'type2',
            'non_attr': 'non_value',
            'description': 'another description',
            'link': '2.gif'
        })

    def test_read_documents_1(self):
        print("all documents")
        expected_response = 2
        assert expected_response == len(DocController.get_documents({}))

    def test_read_documents_2(self):
        print("specific documents")
        expected_response = [{
            'id': 2,
            'metaData': {
                'title': 'title2',
                'type': 'type2',
                'description': 'another description',
                'link': '2.gif',
                'subject': 'Subject2',
                'originalName': None,
                'id': 2,
                'refDate': None,
                'publicationDate': None},
            'visualization': {
                'quaternionW': None,
                'quaternionX': None,
                'positionY': None,
                'quaternionY': None,
                'quaternionZ': None,
                'positionX': None,
                'positionZ': None,
                'id': 2}}]
        assert expected_response == DocController.get_documents({
            'type': 'type2'
        })

    def test_read_documents_3(self):
        print("document with existing id")
        expected_response = {
            'id': 1,
            'metaData': {
                'title': 'title',
                'type': 'type',
                'description': 'a description',
                'link': '1.gif',
                'subject': 'Subject1',
                'originalName': None,
                'id': 1,
                'refDate': None,
                'publicationDate': None},
            'visualization': {
                'quaternionW': None,
                'quaternionX': None,
                'positionY': None,
                'quaternionY': None,
                'quaternionZ': None,
                'positionX': None,
                'positionZ': None,
                'id': 1}}
        assert expected_response == DocController.get_document_by_id(1)

    def test_read_documents_4(self):
        print("document with non existing id")
        with pytest.raises(sqlalchemy.orm.exc.NoResultFound):
            DocController.get_document_by_id(5)

    def test_update_documents_1(self):
        print("existing document")
        expected_response = {
            'id': 1,
            'metaData': {
                'title': 'title',
                'type': 'type',
                'description': 'description of a document',
                'link': '1.gif',
                'subject': 'Subject1',
                'originalName': None,
                'id': 1,
                'refDate': None,
                'publicationDate': None},
            'visualization': {
                'quaternionW': None,
                'quaternionX': None,
                'positionY': None,
                'quaternionY': None,
                'quaternionZ': None,
                'positionX': 12,
                'positionZ': None,
                'id': 1}}

        assert expected_response == DocController.update_document(1, {
            'positionX': 12,
            'description': 'description of a document'
        })

    def test_update_documents_2(self):
        print("non existing document")
        with pytest.raises(sqlalchemy.orm.exc.NoResultFound):
            DocController.update_document(-1, {
                'positionX': 12,
                'description': 'description of a document'})

    def test_delete_documents_1(self):
        print("non existing document")
        with pytest.raises(sqlalchemy.orm.exc.NoResultFound):
            DocController.delete_documents(4)


if __name__ == "__main__":
    TestDocument().test_create_documents_1()
    TestDocument().test_create_documents_2()
    TestDocument().test_delete_documents_1()
