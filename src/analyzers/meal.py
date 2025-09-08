from typing import List, Dict, Any
from collections import defaultdict, Counter
from src.analyzers.base import BaseAnalyzer
from src.analysis_models.results import (
    MealEntry, MealDaySummary, MealAnalysisResult, PatternDetection
)

class MealAnalyzer(BaseAnalyzer):
    """
    Analyzer for meal data: breakdown, frequency, ratings, patterns.
    """

    def analyze(self) -> MealAnalysisResult:
        # Group meals by date
        meals_by_date = defaultdict(list)
        for d in self.data:
            date = d.get("timestamp", "")[:10]  # Assume ISO format, take YYYY-MM-DD
            entry = MealEntry(
                timestamp=d.get("timestamp"),
                dish=d.get("dish"),
                rating=d.get("rating"),
                customizations=d.get("customizations", [])
            )
            meals_by_date[date].append(entry)

        daily_summaries = []
        all_ratings = []
        all_customizations = []

        for date, meals in meals_by_date.items():
            ratings = [m.rating for m in meals if m.rating is not None]
            all_ratings.extend(ratings)
            for m in meals:
                if m.customizations:
                    all_customizations.extend(m.customizations)
            rating_dist = dict(Counter(str(r) for r in ratings))
            daily_summaries.append(MealDaySummary(
                date=date,
                meals=meals,
                meal_count=len(meals),
                rating_distribution=rating_dist
            ))

        # Pattern detection
        patterns = []
        if all_ratings:
            avg_rating = sum(all_ratings) / len(all_ratings)
            if avg_rating < 3:
                patterns.append("Overall low meal ratings")
            elif avg_rating > 4.5:
                patterns.append("Consistently high meal ratings")
        if all_customizations:
            most_common = Counter(all_customizations).most_common(1)
            if most_common:
                patterns.append(f"Most common customization: {most_common[0][0]}")

        overall_patterns = PatternDetection(patterns=patterns)

        return MealAnalysisResult(
            daily_summaries=daily_summaries,
            overall_patterns=overall_patterns,
            metadata=self.get_metadata()
        )