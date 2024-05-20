from docxtpl import DocxTemplate
import re
from docx import Document as WordDocument
import json
from uuid import UUID
from fastapi import Depends, HTTPException
from app.repos.document_repo import DocumentRepository as DocumentRepo
from app.schemas.document import Document

# # # Функция получения и записи информации об атрибутах docx шаблона
# def get_report_attributes(docx_path: str):
#     reports = {}

#     reports_guid = str(uuid.uuid4())
#     file_name = extract_filename(docx_path)

#     reports[reports_guid] = {
#         'id': reports_guid,
#         'file_name': file_name[0],
#         'file_extension': file_name[1]
#     }


#     with open('report_attributes_settings.json', 'w', encoding='utf-8') as json_file:
#         json.dump(reports, json_file, ensure_ascii=False, indent=4)

#     return reports_guid


# def extract_filename(file_path):
#     # Регулярное выражение для выделения имени файла с расширением
#     pattern_file_name = re.compile(r'[^\\/]+(?=\.[^.\\/]+$)')
#     pattern_file_extension = re.compile(r'([^.\\/]+$)')
#     match_file_extension = pattern_file_extension.search(file_path)
#     match_file_name = pattern_file_name.search(file_path)
#     if match_file_name and match_file_extension:
#         return match_file_name.group(0), match_file_extension.group(0)
#     else:
#         return None

def get_report_file(file_id: str, data: str):
    with open('report_attributes_settings.json', 'r', encoding='utf-8') as json_file:
        file_dict = json.load(json_file)

    file = file_dict[file_id]
    file_name = f"{file['file_name']}.{file['file_extension']}"

    doc = WordDocument(file_name)
    config = dict()

    pattern = re.compile(r'\{\{(.*?)\}\}')

    braced_texts = []
    for index, param in enumerate(doc.paragraphs):
        matches = pattern.findall(param.text)
        braced_texts.extend(matches)

    config = {
        'task_message': data
    }

    doc_pattern = DocxTemplate(file_name)

    doc_pattern.render(config)

    doc_pattern.save("new_report.docx")


class DocumentService:
    document_repo: DocumentRepo

    def __init__(self, document_repo: DocumentRepo = Depends(DocumentRepo)) -> None:
        self.document_repo = document_repo

    def get_documents(self) -> list[Document]:
        return self.document_repo.get_documents()

    def get_document_by_id(self, id: int) -> Document:
        return self.document_repo.get_document(id)

    def create_document(self, document: Document) -> Document:
        return self.document_repo.create_document(document)

    def update_document(self, id: int, document: Document) -> Document:
        return self.document_repo.update_document(id, document)

    def delete_document(self, id: int) -> None:
        self.document_repo.delete_document(id)

    def generate_word_document_from_schema(self, id: int) -> str:
        document = self.document_repo.get_document_by_id(id)
        #get_report_file()
        return WordDocument(f'{document.title}.docx')
        
    def generate_word_document_from_schema(self, document: Document) -> str:
        #get_report_file(get_report_attributes("report_maket.docx"), data)
        return WordDocument(f'{document.title}.docx')



# if __name__ == '__main__':
#     data = 'Отчёт по щенкам'
#     get_report_file(get_report_attributes("report_maket.docx"), data)
