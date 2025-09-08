from abc import ABC, abstractmethod
from typing import Any, Dict, List


class BaseAnalyzer(ABC):
    """Abstract base class for all analysis modules."""

    def __init__(self, data: List[Dict[str, Any]]):
        """
        Initialize the analyzer with cleaned data.

        Args:
            data (List[Dict[str, Any]]): A list of data records,
                                        where each record is a dictionary.
        """
        self.data = data

    @abstractmethod
    def analyze(self) -> Any:
        """
        Perform the analysis and return structured results.

        Returns:
            Any: Structured analysis results, typically as a Pydantic model.
        """
        raise NotImplementedError

    def get_metadata(self) -> Dict[str, Any]:
        """
        Get metadata about the analysis.

        Returns:
            Dict[str, Any]: A dictionary containing metadata.
        """
        return {"analyzer": self.__class__.__name__, "num_records": len(self.data)}
