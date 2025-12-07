# Data Model for Module 2 & 3 Implementation

## Module Structure

### Module 2: Digital Twin & Simulation
- **Type**: EducationalModule
- **Fields**:
  - id: string (unique identifier)
  - title: string (Module 2: Digital Twin & Simulation)
  - description: string (Physics-based simulations using Gazebo + Unity)
  - weeks: number (Weeks 6-7)
  - chapters: Chapter[]
  - prerequisites: string[] (ROS 2 fundamentals)

### Module 3: NVIDIA Isaac Sim
- **Type**: EducationalModule
- **Fields**:
  - id: string (unique identifier)
  - title: string (Module 3: NVIDIA Isaac Sim)
  - description: string (GPU-accelerated simulation, perception pipelines)
  - weeks: number (Weeks 8-10)
  - chapters: Chapter[]
  - prerequisites: string[] (Module 1-2 completion, GPU access)

## Chapter Structure

### Chapter
- **Type**: EducationalChapter
- **Fields**:
  - id: string (unique identifier)
  - title: string (chapter title)
  - description: string (brief overview)
  - topics: Topic[]
  - lab: Lab
  - learning_objectives: string[]
  - prerequisites: string[]

## Topic Structure

### Topic
- **Type**: EducationalTopic
- **Fields**:
  - id: string (unique identifier)
  - title: string (topic title)
  - content: string (educational content)
  - examples: Example[]
  - external_resources: string[]

## Lab Structure

### Lab
- **Type**: EducationalLab
- **Fields**:
  - id: string (unique identifier)
  - title: string (lab title)
  - objectives: string[]
  - prerequisites: string[]
  - steps: LabStep[]
  - expected_outputs: string[]
  - verification_checks: string[]
  - troubleshooting: string[]

## Lab Step Structure

### LabStep
- **Type**: LabStep
- **Fields**:
  - id: string (step number)
  - description: string (what to do)
  - command: string (terminal command if applicable)
  - expected_result: string (what should happen)

## Example Asset Structure

### ExampleAsset
- **Type**: ExampleAsset
- **Fields**:
  - id: string (unique identifier)
  - name: string (file name)
  - type: string (urdf, sdf, usd, json, py, etc.)
  - purpose: string (what the asset demonstrates)
  - path: string (location in static/code/)

## Asset Relationships

- EducationalModule contains many EducationalChapter
- EducationalChapter contains many EducationalTopic
- EducationalChapter has one EducationalLab
- EducationalLab contains many LabStep
- EducationalModule has many ExampleAsset (stored in static/code/)

## Validation Rules

- Module title must be unique
- Chapter IDs must be unique within a module
- Lab steps must have clear expected results
- Example assets must be < 100KB
- All external resource links must be valid
- Learning objectives must be measurable
- Prerequisites must be clearly stated