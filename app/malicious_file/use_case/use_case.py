from app.malicious_file.repository import MaliciousFileRepository
from app.malicious_file.use_case.dto.delete_file_dto import DeleteFileDto


class MaliciousFileUseCase:

    def __init__(self, repository: MaliciousFileRepository):
        self.malicious_file_repository_object = repository

    def fetch_all_files(self):
        return self.malicious_file_repository_object.get_all_files()

    def save_file(self, data):
        hash = data.get('file_hash')
        name = data.get('file_name')
        tag = data.get('file_tag')
        self.malicious_file_repository_object.save_file(hash, name, tag)

    def delete_file(self, delete_dto: DeleteFileDto):
        self.malicious_file_repository_object.delete_file(delete_dto)

    def get_file_name(self):
        return self.malicious_file_repository_object.get_all_name()

    def get_paging(self, name_search):
        return self.malicious_file_repository_object.get_paging(name_search)


