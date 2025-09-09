from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseFeatureExtractor(ABC):
    """
    Abstract base class for all feature extractors.
    """
    def __init__(self, data: Dict[str, List[Dict[str, Any]]]):
        self.data = data

    @abstractmethod
    def extract_features(self) -> Dict[str, Any]:
        """
        Extracts features from the data and returns them as a dictionary.
        """
        raise NotImplementedError

    def get_metadata(self) -> Dict[str, Any]:
        """
        Returns metadata about the feature extraction process.
        """
        # This can be expanded to include more details
        return {
            "feature_extractor": self.__class__.__name__
        }
