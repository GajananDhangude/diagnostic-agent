from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Literal
from enum import Enum


class SeverityLevel(str, Enum):
    LOW = "Low"
    MODERATE = "Moderate"
    HIGH = "High"
    CRITICAL = "Critical"



class IssueType(str, Enum):
    DAMPNESS = "Dampness"
    SEEPAGE = "Seepage"
    LEAKAGE = "Leakage"
    CRACKS = "Cracks"
    HOLLOW_TILES = "Hollow Tiles"
    EFFLORESCENCE = "Efflorescence"
    WATER_STAINS = "Water Stains"



class IssueObservation(BaseModel):
    """A single observed issue with full context"""
    issue_type: IssueType = Field(description="Type of issue observed")
    location: str = Field(description="Specific location (e.g., 'skirting level', 'ceiling', 'external wall')")
    description: str = Field(description="Detailed description of what was observed")
    severity: Optional[SeverityLevel] = Field(None, description="Severity of this specific issue")
    
    @field_validator('description')
    @classmethod
    def description_not_empty(cls, v):
        if not v or len(v.strip()) < 10:
            raise ValueError("Description must be at least 10 characters")
        return v



class ThermalReading(BaseModel):
    """Temperature data from thermal imaging"""
    area: str = Field(description="Area where reading was taken")
    hotspot_celsius: float = Field(description="Hotspot temperature in Celsius", ge=0, le=100)
    coldspot_celsius: float = Field(description="Coldspot temperature in Celsius", ge=0, le=100)
    temperature_difference: float = Field(description="Difference between hotspot and coldspot")
    image_reference: Optional[str] = Field(None, description="Reference to thermal image number")
    
    @field_validator('temperature_difference')
    @classmethod
    def validate_temp_diff(cls, v, info):
        # Auto-calculate if not provided
        if 'hotspot_celsius' in info.data and 'coldspot_celsius' in info.data:
            expected = info.data['hotspot_celsius'] - info.data['coldspot_celsius']
            if abs(v - expected) > 0.1:
                raise ValueError(f"Temperature difference mismatch: {v} vs {expected}")
        return v

class AreaObservation(BaseModel):
    """All observations for a specific area"""
    area_name: str = Field(description="Name of the area (e.g., 'Hall', 'Master Bedroom')")
    issues: List[IssueObservation] = Field(description="List of issues observed in this area")
    thermal_data: Optional[ThermalReading] = Field(None, description="Thermal imaging data for this area if available")
    overall_condition: Optional[str] = Field(None, description="Overall assessment of this area")


class RootCauseAnalysis(BaseModel):
    """Root cause analysis with evidence"""
    probable_cause: str = Field(description="The probable root cause")
    supporting_evidence: List[str] = Field(description="Evidence from observations that support this cause")
    confidence: Literal["High", "Medium", "Low"] = Field(description="Confidence level in this analysis")



class SeverityAssessment(BaseModel):
    """Overall severity assessment with reasoning"""
    level: SeverityLevel = Field(description="Overall severity level")
    reasoning: str = Field(description="Detailed explanation of why this severity was assigned", min_length=50)
    risk_factors: List[str] = Field(description="Specific risk factors identified")
    urgency_score: int = Field(description="Urgency score from 1-10", ge=1, le=10)


class RecommendedActions(BaseModel):
    """Categorized recommendations"""
    immediate: List[str] = Field(description="Actions needed within 1 week", min_items=1)
    short_term: List[str] = Field(description="Actions within 1-3 months", min_items=1)
    long_term: List[str] = Field(description="Preventive measures for future", min_items=1)


class DDRReport(BaseModel):
    """Complete Detailed Diagnostic Report"""
    
    # Property Information
    property_type: str = Field(description="Type of property (e.g., 'Flat', 'House')")
    floors: int = Field(description="Number of floors", ge=1)
    flat_number: Optional[str] = Field(None, description="Flat/unit number if applicable")
    inspection_date: str = Field(description="Date of inspection (DD.MM.YYYY or YYYY-MM-DD)")
    inspector_names: str = Field(description="Names of inspectors")
    
    # Executive Summary
    property_issue_summary: str = Field(
        description="2-3 sentence executive summary of main findings",
    )
    
    # Detailed Observations
    area_wise_observations: List[AreaObservation] = Field(
        description="Detailed observations grouped by area",
        min_items=1
    )
    
    # Analysis
    root_cause_analysis: List[RootCauseAnalysis] = Field(
        description="Root cause analysis with evidence",
        min_items=1
    )
    
    severity_assessment: SeverityAssessment = Field(
        description="Overall severity assessment"
    )
    
    # Recommendations
    recommended_actions: RecommendedActions = Field(
        description="Categorized action plan"
    )
    
    # Additional Information
    additional_notes: List[str] = Field(
        default=[],
        description="Any additional observations or context"
    )
    
    missing_information: List[str] = Field(
        default=[],
        description="Explicitly list any data that was 'Not Available' or unclear"
    )
    
    @field_validator('area_wise_observations')
    @classmethod
    def validate_areas(cls, v):
        if len(v) == 0:
            raise ValueError("Must have at least one area observation")
        # Check for duplicate areas
        area_names = [obs.area_name for obs in v]
        if len(area_names) != len(set(area_names)):
            raise ValueError("Duplicate area names found")
        return v