from enum import Enum

class VideoStatusEnum(Enum):
    PENDING_FRAMES = ("Pending Frames", "Awaiting processing")
    QUEUED_FRAMES = ("Queued for Frame Extraction", "Queued for frame extraction")
    PROCESSING_FRAMES = ("Processing Frames", "Frame extraction in progress")
    PENDING_ZIP = ("Pending ZIP", "Awaiting ZIP creation")
    QUEUED_ZIP = ("Queued for ZIP Creation", "Queued for ZIP creation")
    PROCESSING_ZIP = ("Processing ZIP", "ZIP creation in progress")
    COMPLETED = ("Completed", "Processing completed")
    ERROR = ("Error", "An error occurred during processing")
    

    @property
    def status(self):
        return self.value[0]

    @property
    def description(self):
        return self.value[1]

    @classmethod
    def status_and_descriptions(cls):
        return [{"name": member.status, "description": member.description} for member in cls]
    
    @classmethod
    def method_list(cls):
        """
        Retorna todos os status dos métodos do Job Zipper.
        :return: Lista de status dos métodos.
        """
        return [member.status for member in cls]
    
    @classmethod
    def to_dict(cls):
        """
        Retorna um dicionário mapeando os status dos métodos às suas descrições.
        :return: Dicionário com o status como chave e a descrição como valor.
        """
        return {member.status: member.description for member in cls}
    
    def __str__(self) -> str:
        return self.status.upper()
    
    def __repr__(self) -> str:
        return self.status
    
__all__ = ['VideoStatus']
