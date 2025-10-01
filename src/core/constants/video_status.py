from enum import Enum

class VideoStatusEnum(Enum):
    PENDING_FRAMES = (0, "Pending Frames", "Awaiting processing")
    QUEUED_FRAMES = (1, "Queued for Frame Extraction", "Queued for frame extraction")
    PROCESSING_FRAMES = (2, "Processing Frames", "Frame extraction in progress")
    PENDING_ZIP = (3, "Pending ZIP", "Awaiting ZIP creation")
    QUEUED_ZIP = (4, "Queued for ZIP Creation", "Queued for ZIP creation")
    PROCESSING_ZIP = (5, "Processing ZIP", "ZIP creation in progress")
    COMPLETED = (6, "Completed", "Processing completed")
    ERROR = (7, "Error", "An error occurred during processing")
    REJECTED = (8, "Rejected", "Video rejected due to content policy violations")

    @property
    def order(self):
        return self.value[0]

    @property
    def status(self):
        return self.value[1]

    @property
    def description(self):
        return self.value[2]

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
    
    @classmethod
    def get_by_status(cls, status: str):
        """
        Retorna o membro do enum correspondente ao status fornecido.
        :param status: O status a ser procurado.
        :return: O membro do enum VideoStatusEnum.
        :raises ValueError: Se nenhum status correspondente for encontrado.
        """
        for member in cls:
            if member.status == status:
                return member
        raise ValueError(f"No matching status for '{status}'")
    
    def __str__(self) -> str:
        return self.status.upper()
    
    def __repr__(self) -> str:
        return self.status
    
__all__ = ['VideoStatusEnum']
